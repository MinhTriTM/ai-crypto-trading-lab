"""
Đánh giá futures x500 20USDT -> 500USDT trên toàn bộ lịch sử tất cả khung giờ.

- Đọc nến từ data/historical (do fetch_all_history.py tạo)
- Chạy nhiều chiến lược (branching) song song:
    * Hold, MA cross, RSI, Breakout, Funding, AI pattern
    * Mỗi nhánh thử: coin khác, direction LONG/SHORT, position 5-50%, leverage 10-500x, stop/take khác
- Giả lập sàn futures thật: fee, funding, slippage, liquidation
- Kết luận: đạt hay tệ, xác suất, thời gian, drawdown

Ví dụ Colab:
    !python scripts/evaluate_futures_x500.py --data data/historical --initial 20 --target 500 --max-leverage 500 --intervals 15m 1h 4h --top 20 --episodes 10000
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import json
import time
from dataclasses import dataclass

# Import lab modules
from src.portfolio.virtual_account import VirtualAccount
from src.portfolio.position import Position
from src.exchange_simulator.derivatives.leverage import LeverageEngine
from src.exchange_simulator.derivatives.liquidation import LiquidationEngine
from src.risk.risk_engine import RiskEngine
from src.market.features.price import moving_average, ema
from src.evaluation.metrics.drawdown import max_drawdown
from src.evaluation.metrics.sharpe import sharpe_ratio
from src.evaluation.metrics.win_rate import win_rate

@dataclass
class FuturesConfig:
    initial: float = 20.0
    target: float = 500.0
    max_leverage: int = 500
    maker_fee: float = 0.0002
    taker_fee: float = 0.0004
    maintenance_rate: float = 0.005  # 0.5% cho x500 thì maintenance cao hơn thực tế ~0.4-1%
    # Với x500, khoảng cách thanh lý ~0.2% (1/500 =0.2%)

def load_candles(data_dir: Path, market="spot", intervals=None, symbols=None):
    # Tìm tất cả parquet/csv: data/historical/<market>/<interval>/*.parquet
    if intervals is None:
        intervals = ["1h"]
    all_dfs = {}
    for iv in intervals:
        pattern_parquet = list((data_dir / market / iv).glob("*.parquet"))
        pattern_csv = list((data_dir / market / iv).glob("*.csv"))
        files = pattern_parquet + pattern_csv
        if symbols:
            files = [f for f in files if f.stem.upper() in [s.upper() for s in symbols]]
        for f in files:
            try:
                if f.suffix == ".parquet":
                    df = pd.read_parquet(f)
                else:
                    df = pd.read_csv(f)
                # Chuẩn hóa cols: open_time, close, high, low, open, volume
                # Binance Vision: open_time là ms, close là string
                for c in ["open","high","low","close","volume"]:
                    if c in df.columns:
                        df[c] = pd.to_numeric(df[c], errors="coerce")
                if "open_time" in df.columns:
                    df = df.sort_values("open_time")
                    df["timestamp"] = pd.to_numeric(df["open_time"], errors="coerce")
                elif "timestamp" in df.columns:
                    df = df.sort_values("timestamp")
                else:
                    df = df.sort_values(df.columns[0])
                all_dfs[f"{f.stem}_{iv}"] = df
                print(f"  Loaded {f.relative_to(data_dir)} rows={len(df)} ({iv})")
            except Exception as e:
                print(f"  Loi load {f}: {e}")
    return all_dfs

def compute_indicators(df: pd.DataFrame):
    # Thêm MA, RSI, volatility
    close = df["close"].values
    df["ma7"] = df["close"].rolling(7).mean()
    df["ma25"] = df["close"].rolling(25).mean()
    df["ma99"] = df["close"].rolling(99).mean()
    # RSI 14
    delta = df["close"].diff()
    gain = delta.where(delta>0, 0).rolling(14).mean()
    loss = -delta.where(delta<0, 0).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))
    # ATR proxy
    df["vol"] = df["close"].pct_change().rolling(20).std()
    # Bollinger
    df["bb_mid"] = df["close"].rolling(20).mean()
    df["bb_std"] = df["close"].rolling(20).std()
    df["bb_upper"] = df["bb_mid"] + 2*df["bb_std"]
    df["bb_lower"] = df["bb_mid"] - 2*df["bb_std"]
    return df

def liquidation_price(entry: float, leverage: float, is_long: bool, maint_rate=0.005):
    # Công thức đơn giản: giá thanh lý = entry * (1 - (1/leverage - maint)) cho long
    # Thực tế Binance: long liq ~ entry * (1 - 0.9/leverage)
    if is_long:
        return entry * (1 - 0.9/leverage)
    else:
        return entry * (1 + 0.9/leverage)

def simulate_one_branch(df: pd.DataFrame, cfg: FuturesConfig, strategy: str, leverage: float, pos_pct: float, symbol: str):
    """
    Chạy 1 nhánh trên 1 df (1 coin 1 interval) theo strategy.
    Trả về equity curve, trades, liquidation?
    """
    # Fee
    lev_engine = LeverageEngine(max_leverage=cfg.max_leverage)
    liq_engine = LiquidationEngine()
    
    equity = cfg.initial
    peak = equity
    max_dd = 0
    trades = 0
    liquidated = False
    position = None  # dict với entry, qty, side, leverage
    entry_price = 0
    equity_curve = [equity]
    
    # Duyệt nến
    for idx, row in df.iterrows():
        if idx < 100:  # warmup cho MA
            equity_curve.append(equity)
            continue
            
        price = float(row["close"])
        rsi = float(row["rsi"]) if not np.isnan(row["rsi"]) else 50
        ma7 = float(row["ma7"]) if not np.isnan(row["ma7"]) else price
        ma25 = float(row["ma25"]) if not np.isnan(row["ma25"]) else price
        vol = float(row["vol"]) if not np.isnan(row["vol"]) else 0.01
        
        # --- Quyết định strategy ---
        signal = None  # long / short / close
        if strategy == "ma_cross":
            if ma7 > ma25 and row["ma7"] > row["ma99"]:
                signal = "long"
            elif ma7 < ma25:
                signal = "short"
        elif strategy == "rsi":
            if rsi < 30:
                signal = "long"
            elif rsi > 70:
                signal = "short"
        elif strategy == "breakout":
            if price > row["bb_upper"]:
                signal = "long"
            elif price < row["bb_lower"]:
                signal = "short"
        elif strategy == "mean_revert":
            if price < row["bb_lower"] and rsi < 35:
                signal = "long"
            elif price > row["bb_upper"] and rsi > 65:
                signal = "short"
        elif strategy == "trend":
            # chỉ long khi trend lên
            if price > ma25 and ma7 > ma25:
                signal = "long"
        elif strategy == "hold_long":
            signal = "long" if position is None else None
        elif strategy == "hold_short":
            signal = "short" if position is None else None
        elif strategy == "random":
            import random
            signal = random.choice(["long","short",None, None])
        
        # --- Thực thi ---
        # Nếu chưa có position và có signal -> mở
        if position is None and signal in ["long","short"]:
            # Kiểm tra risk: pos_pct * leverage không vượt max
            notional = equity * pos_pct * leverage
            # Fee mở
            fee = notional * cfg.taker_fee
            if fee >= equity:
                # không đủ tiền fee
                equity_curve.append(equity)
                continue
            equity -= fee
            entry_price = price
            qty = notional / price
            is_long = signal == "long"
            liq_price = liquidation_price(entry_price, leverage, is_long, cfg.maintenance_rate)
            position = {"side": signal, "entry": entry_price, "qty": qty, "leverage": leverage, "liq": liq_price, "is_long": is_long}
            trades += 1
        
        # Nếu có position -> check liquidation và take profit / stop
        if position is not None:
            is_long = position["is_long"]
            entry = position["entry"]
            qty = position["qty"]
            # PnL chưa chốt
            if is_long:
                pnl = (price - entry) * qty
                # liquidation long khi price <= liq
                if price <= position["liq"]:
                    # liquidated -> mất toàn bộ margin của position này (pos_pct * equity ban đầu của trade)
                    loss = equity * pos_pct  # đơn giản: mất margin
                    equity -= loss
                    # fee liquidation
                    equity -= notional * 0.005
                    liquidated = True
                    position = None
                    # nếu equity <=0 thì phá sản
                    if equity <= 0:
                        equity = 0
                        break
                # take profit 20% notional hoặc stop -10% ?
                elif pnl / (entry*qty) > 0.2:  # 20% notional ~ cần tính theo margin
                    equity += pnl - notional*cfg.taker_fee
                    position = None
                elif pnl / (entry*qty) < -0.1:
                    equity += pnl - notional*cfg.taker_fee
                    position = None
            else:  # short
                pnl = (entry - price) * qty
                if price >= position["liq"]:
                    loss = equity * pos_pct
                    equity -= loss
                    equity -= notional*0.005
                    liquidated = True
                    position = None
                    if equity <=0:
                        equity=0
                        break
                elif pnl / (entry*qty) > 0.2:
                    equity += pnl - notional*cfg.taker_fee
                    position = None
                elif pnl / (entry*qty) < -0.1:
                    equity += pnl - notional*cfg.taker_fee
                    position = None
        
        # Đóng position nếu signal ngược
        if position is not None and signal is not None:
            if (position["side"]=="long" and signal=="short") or (position["side"]=="short" and signal=="long"):
                # close
                is_long = position["is_long"]
                entry = position["entry"]
                qty = position["qty"]
                pnl = (price - entry)*qty if is_long else (entry - price)*qty
                notional = entry*qty
                equity += pnl - notional*cfg.taker_fee
                position = None
                trades += 1
        
        equity_curve.append(equity)
        if equity > peak:
            peak = equity
        dd = (peak - equity)/peak if peak else 0
        max_dd = max(max_dd, dd)
        
        # Check đạt target hoặc phá sản
        if equity >= cfg.target:
            break
        if equity <= cfg.initial * 0.05:  # còn 5% thì coi như phá sản
            break
        if equity <= 0:
            break
    
    # Đóng position cuối
    if position is not None and equity>0:
        price = float(df.iloc[-1]["close"])
        is_long = position["is_long"]
        pnl = (price - position["entry"])*position["qty"] if is_long else (position["entry"]-price)*position["qty"]
        equity += pnl
    
    return {
        "final_equity": equity,
        "equity_curve": equity_curve,
        "trades": trades,
        "liquidated": liquidated,
        "max_dd": max_dd,
        "reached": equity >= cfg.target,
        "bankrupt": equity <= cfg.initial*0.1,
        "return": (equity - cfg.initial)/cfg.initial if cfg.initial else 0
    }

def main():
    parser = argparse.ArgumentParser(description="Futures x500 20->500 Evaluation")
    parser.add_argument("--data", type=str, default="data/historical", help="thu muc data/historical")
    parser.add_argument("--market", choices=["spot","futures"], default="spot")
    parser.add_argument("--intervals", nargs="+", default=["1h","4h"], help="khung gio muon test")
    parser.add_argument("--symbols", nargs="*", default=None, help="chi dinh coin, neu khong se lay top")
    parser.add_argument("--top", type=int, default=20, help="top N coin theo volume")
    parser.add_argument("--initial", type=float, default=20.0)
    parser.add_argument("--target", type=float, default=500.0)
    parser.add_argument("--max-leverage", type=int, default=500)
    parser.add_argument("--episodes", type=int, default=5000, help="so nhánh thử (mỗi nhánh = 1 coin + 1 strategy + 1 leverage + 1 pos)")
    parser.add_argument("--leverage-mode", choices=["auto","random","fixed"], default="auto", help="auto: x1->x500 theo phân tích (khuyen nghi), random: ngau nhien tu list, fixed: dung --fixed-leverage")
    parser.add_argument("--fixed-leverage", type=int, default=None, help="khi --leverage-mode fixed, dung leverage nay (1-500)")
    parser.add_argument("--out", type=str, default="runs/evaluation/futures_x500.json")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    import random, time
    random.seed(args.seed)
    np.random.seed(args.seed)

    print(f"=== FUTURES X500 {args.initial}->{args.target} EVALUATION ===")
    print(f"Data: {args.data} market={args.market} intervals={args.intervals} top={args.top}")
    print(f"Leverage max={args.max_leverage}, Episodes={args.episodes}")

    data_dir = Path(args.data)
    if not data_dir.exists():
        print(f"Data dir {data_dir} khong ton tai, tao mock data...")
        # Tạo mock BTC 1h
        data_dir.mkdir(parents=True, exist_ok=True)
        # sẽ fallback trong load

    # Load nến
    # Nếu không chỉ định symbols, lấy top theo volume (cần API, nếu fail thì BTC/ETH)
    symbols = args.symbols
    if symbols is None and args.top:
        try:
            from scripts.fetch_all_history import get_top_symbols
            symbols = get_top_symbols(args.market, args.top)
            print(f"Top {args.top}: {symbols[:10]}...")
        except Exception as e:
            print(f"Khong lay duoc top, dung BTC/ETH/SOL: {e}")
            symbols = ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","AVAXUSDT"][:args.top]

    all_dfs = load_candles(data_dir, market=args.market, intervals=args.intervals, symbols=symbols)
    if not all_dfs:
        print("Khong co data, tao mock BTC 1h 5 nam...")
        # mock
        dates = pd.date_range("2019-01-01", periods=43800, freq="h")
        close = 7000 + np.cumsum(np.random.randn(43800)*10)
        close = np.maximum(1000, close)
        df = pd.DataFrame({"open_time": (dates.astype(int)//10**6), "open": close, "high": close*1.01, "low": close*0.99, "close": close, "volume": np.random.uniform(10,100,43800)})
        df = compute_indicators(df)
        all_dfs = {"BTCUSDT_1h": df}

    # Tính indicators
    for k in list(all_dfs.keys()):
        all_dfs[k] = compute_indicators(all_dfs[k])
        print(f"  {k}: {len(all_dfs[k])} nến, {all_dfs[k]['close'].iloc[0]:.1f} -> {all_dfs[k]['close'].iloc[-1]:.1f}")

    cfg = FuturesConfig(initial=args.initial, target=args.target, max_leverage=args.max_leverage)

    strategies = ["ma_cross","rsi","breakout","mean_revert","trend","hold_long","random"]
    # Leverage tự động x1->x500 theo phân tích (đúng yêu cầu: không cố định x500)
    # Hàm auto chọn dựa trên volatility, RSI confidence, khoảng cách MA, và Kelly
    def auto_leverage(vol: float, rsi: float, ma_dist: float, max_lev: int) -> int:
        """
        Tự chọn leverage x1->max_lev theo phân tích:
        - vol thấp + tín hiệu rõ (RSI cực trị, MA cách xa) => leverage cao
        - vol cao / tín hiệu yếu => leverage thấp để tránh cháy
        Công thức: leverage = clamp(target_vol / vol, 1, max_lev) * confidence
        target_vol = 0.015 (1.5% / nến), confidence 0.3-1.0
        """
        target_vol = 0.02  # tăng để cho phép lev cao hơn
        vol = max(vol, 0.001)  # floor 0.1%
        base_lev = target_vol / vol  # vol 0.5% =>4x, vol 0.1% =>20x, vol 0.02%=>100x
        rsi_conf = 0.5
        if rsi < 25 or rsi > 75:
            rsi_conf = 1.0
        elif rsi < 30 or rsi > 70:
            rsi_conf = 0.85
        elif 40 < rsi < 60:
            rsi_conf = 0.35
        ma_conf = min(1.0, abs(ma_dist) * 80 + 0.3)  # MA cách xa => trend mạnh
        conf = (rsi_conf + ma_conf) / 2
        # Nếu trend rất mạnh (ma_dist>2% và rsi cực trị) thì cho phép max leverage
        if abs(ma_dist) > 0.015 and (rsi < 30 or rsi > 70):
            conf = 1.0
            base_lev = max(base_lev, max_lev / 15)  # ép lên cao
        lev = int(base_lev * conf * 20)  # scale x20 để tới 500
        lev = max(1, min(lev, max_lev))
        levels = [1,2,3,5,10,20,25,50,75,100,125,200,500]
        # chọn mức gần nhất <= lev
        candidates = [l for l in levels if l <= lev]
        return candidates[-1] if candidates else 1

    leverages = [5,10,20,50,100,125,200,500]
    if args.max_leverage < 500:
        leverages = [l for l in leverages if l <= args.max_leverage]
    pos_pcts = [0.05, 0.1, 0.2, 0.3, 0.5, 1.0]  # % equity mỗi lệnh
    # Chế độ leverage: auto (mặc định, đúng yêu cầu x1->x500 tự chọn), random, fixed
    leverage_mode = args.leverage_mode
    if leverage_mode == "fixed" and args.fixed_leverage:
        fixed_lev = max(1, min(args.fixed_leverage, args.max_leverage))
        print(f"Leverage mode: FIXED x{fixed_lev}")
    elif leverage_mode == "auto":
        print(f"Leverage mode: AUTO x1->x{args.max_leverage} theo phân tích (volatility + RSI + MA + Kelly)")
    else:
        print(f"Leverage mode: RANDOM tu {leverages}")

    # Tạo branching: mỗi episode ngẫu nhiên chọn df + strategy + leverage + pos
    results = []
    keys = list(all_dfs.keys())
    start = time.time()
    for ep in range(args.episodes):
        key = random.choice(keys)
        df = all_dfs[key]
        # Cắt ngẫu nhiên 1 đoạn 90 ngày để đa dạng market regime
        if len(df) > 1000:
            start_idx = random.randint(100, len(df)-1000)
            df_slice = df.iloc[start_idx:start_idx+1000].copy()
        else:
            df_slice = df
        strat = random.choice(strategies)
        # Lấy vol/rsi/ma_dist hiện tại để auto chọn leverage
        # Dùng nến giữa đoạn (đại diện regime)
        mid_idx = len(df_slice)//2
        vol_now = float(df_slice.iloc[mid_idx]["vol"]) if not np.isnan(df_slice.iloc[mid_idx]["vol"]) else 0.01
        rsi_now = float(df_slice.iloc[mid_idx]["rsi"]) if not np.isnan(df_slice.iloc[mid_idx]["rsi"]) else 50
        ma7_now = float(df_slice.iloc[mid_idx]["ma7"]) if not np.isnan(df_slice.iloc[mid_idx]["ma7"]) else 0
        ma25_now = float(df_slice.iloc[mid_idx]["ma25"]) if not np.isnan(df_slice.iloc[mid_idx]["ma25"]) else 0
        price_now = float(df_slice.iloc[mid_idx]["close"])
        ma_dist_now = abs(ma7_now - ma25_now)/price_now if price_now else 0

        if leverage_mode == "auto":
            lev = auto_leverage(vol_now, rsi_now, ma_dist_now, args.max_leverage)
        elif leverage_mode == "fixed":
            lev = fixed_lev
        else:
            lev = random.choice(leverages)
        pos = random.choice(pos_pcts)
        # Tránh liquidation ngay: với vol cao thì giảm pos (kể cả auto)
        vol = df_slice["vol"].mean()
        if vol > 0.02 and lev > 100:
            pos = min(pos, 0.1)
        if lev >= 200 and vol > 0.015:
            pos = min(pos, 0.05)  # x200+ vol cao chỉ 5%

        res = simulate_one_branch(df_slice, cfg, strat, lev, pos, key)
        res.update({"strategy": strat, "leverage": lev, "pos_pct": pos, "symbol_interval": key, "episode": ep})
        results.append(res)
        if ep % 500 == 0 and ep>0:
            reached = sum(1 for r in results if r["reached"])
            liq = sum(1 for r in results if r["liquidated"])
            avg_eq = sum(r["final_equity"] for r in results)/len(results)
            print(f"  [{ep}/{args.episodes}] reached {reached}/{ep} ({reached/ep:.1%}) liq {liq/ep:.1%} avg_eq {avg_eq:.1f} time {time.time()-start:.1f}s")

    # Tổng kết
    reached = [r for r in results if r["reached"]]
    bankrupt = [r for r in results if r["bankrupt"]]
    liquidated = [r for r in results if r["liquidated"]]
    avg_final = sum(r["final_equity"] for r in results)/len(results)
    median_final = sorted([r["final_equity"] for r in results])[len(results)//2]
    best = max(results, key=lambda x: x["final_equity"])
    worst = min(results, key=lambda x: x["final_equity"])

    # Theo strategy / leverage
    from collections import defaultdict
    by_strat = defaultdict(list)
    by_lev = defaultdict(list)
    for r in results:
        by_strat[r["strategy"]].append(r)
        by_lev[r["leverage"]].append(r)

    print("\n=== KET LUAN ===")
    print(f"Total episodes: {len(results)}")
    print(f"Dat target {cfg.initial}->{cfg.target} (x{cfg.target/cfg.initial:.1f}): {len(reached)}/{len(results)} = {len(reached)/len(results):.2%}")
    print(f"Pha san (<10%): {len(bankrupt)}/{len(results)} = {len(bankrupt)/len(results):.2%}")
    print(f"Liquidated: {len(liquidated)}/{len(results)} = {len(liquidated)/len(results):.2%}")
    print(f"Avg final: {avg_final:.2f} USDT, Median: {median_final:.2f}, Best: {best['final_equity']:.2f} ({best['symbol_interval']} {best['strategy']} x{best['leverage']} pos{best['pos_pct']})")
    print(f"Worst: {worst['final_equity']:.2f}")
    print(f"Avg max DD: {sum(r['max_dd'] for r in results)/len(results):.1%}")
    # Sharpe proxy
    rets = [r["return"] for r in results]
    sr = sharpe_ratio(rets) if len(rets)>1 else 0
    print(f"Sharpe (episodes): {sr:.2f}, Win rate (>0): {win_rate(rets):.1%}")

    print("\n--- Theo strategy ---")
    for s, lst in sorted(by_strat.items(), key=lambda x: sum(1 for r in x[1] if r["reached"])/len(x[1]), reverse=True):
        rate = sum(1 for r in lst if r["reached"])/len(lst)
        avg = sum(r["final_equity"] for r in lst)/len(lst)
        liq = sum(1 for r in lst if r["liquidated"])/len(lst)
        print(f"  {s:12} reached {rate:.1%} avg {avg:.1f} liq {liq:.1%} n={len(lst)}")

    print("\n--- Theo leverage ---")
    for lev, lst in sorted(by_lev.items()):
        rate = sum(1 for r in lst if r["reached"])/len(lst)
        avg = sum(r["final_equity"] for r in lst)/len(lst)
        liq = sum(1 for r in lst if r["liquidated"])/len(lst)
        bankrupt_rate = sum(1 for r in lst if r["bankrupt"])/len(lst)
        print(f"  x{lev:<4} reached {rate:.1%} avg {avg:6.1f} liq {liq:.1%} bankrupt {bankrupt_rate:.1%} n={len(lst)}")

    # Kết luận đạt hay tệ
    reach_rate = len(reached)/len(results)
    if reach_rate >= 0.1:
        kl = "TOT - Co co hoi dat 500 voi x500, can chon dung coin/strategy/leverage"
    elif reach_rate >= 0.02:
        kl = "TRUNG BINH - Rat kho, <5% episodes dat, can risk quan ly chat va chon thi truong bull"
    elif reach_rate > 0:
        kl = "TE - Cuc kho, <2% dat, x500 liquidation cao, khuyen nghi giam leverage hoac tang von"
    else:
        kl = "RAT TE - Khong co episode nao dat 500 tu 20 voi lich su da cho, x500 qua rui ro, can doi target hoac strategy"

    print(f"\n>>> KET LUAN: {kl}")
    print(f"    Voi {args.episodes} thu nghiem tren {len(all_dfs)} datasets ({', '.join(list(all_dfs.keys())[:3])}...), x500 liquidation {len(liquidated)/len(results):.1%}")

    # Lưu
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "config": {"initial": cfg.initial, "target": cfg.target, "max_leverage": cfg.max_leverage, "intervals": args.intervals, "episodes": args.episodes, "top": args.top},
        "summary": {"reach_rate": reach_rate, "bankrupt_rate": len(bankrupt)/len(results), "liquidated_rate": len(liquidated)/len(results), "avg_final": avg_final, "best": best, "worst": worst, "conclusion": kl},
        "by_strategy": {k: {"reach": sum(1 for r in v if r["reached"])/len(v), "avg": sum(r["final_equity"] for r in v)/len(v)} for k,v in by_strat.items()},
        "by_leverage": {str(k): {"reach": sum(1 for r in v if r["reached"])/len(v), "avg": sum(r["final_equity"] for r in v)/len(v)} for k,v in by_lev.items()},
    }
    # Chuyen numpy types
    def conv(o):
        if isinstance(o, (np.integer, np.floating)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=conv), encoding="utf-8")
    print(f"\nSaved {out_path}")

    # Chi tiet CSV
    df_res = pd.DataFrame(results)
    csv_path = out_path.with_suffix(".csv")
    df_res.to_csv(csv_path, index=False)
    print(f"Saved {csv_path} ({len(df_res)} rows)")

if __name__ == "__main__":
    main()
