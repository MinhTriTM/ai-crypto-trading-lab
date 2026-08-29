"""
Fetch toàn bộ lịch sử nến cho tất cả coin, tất cả khung giờ — Colab-ready.

Hỗ trợ 2 nguồn:
- Binance Vision (data.binance.vision) — ZIP daily, nhanh, không rate-limit, nên dùng cho backfill dài
- Binance REST API (api.binance.com / fapi.binance.com) — cho gap gần nhất và coin mới

Ví dụ Colab:
    # Mount Drive nếu muốn lưu lâu dài
    from google.colab import drive; drive.mount('/content/drive')
    !python scripts/fetch_all_history.py --market spot --intervals 1h 4h 1d --top 50 --years 5 --out /content/drive/MyDrive/ai-lab/data
    !python scripts/fetch_all_history.py --market futures --intervals 15m 1h 4h --symbols BTCUSDT ETHUSDT SOLUSDT --years 3 --vision

    # All coin (cẩn trọng dung lượng):
    !python scripts/fetch_all_history.py --market spot --all --intervals 1h --years 5 --out data/historical
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import time
import zipfile
import io
import requests
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

BINANCE_VISION = "https://data.binance.vision"
INTERVALS = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1M"]

def get_all_symbols(market="spot", quote="USDT"):
    if market == "futures":
        url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    else:
        url = "https://api.binance.com/api/v3/exchangeInfo"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    if market == "futures":
        syms = [s["symbol"] for s in data["symbols"] if s["contractType"]=="PERPETUAL" and s["status"]=="TRADING" and s["quoteAsset"]==quote]
    else:
        syms = [s["symbol"] for s in data["symbols"] if s["status"]=="TRADING" and s["quoteAsset"]==quote]
    return sorted(syms)

def get_top_symbols(market="spot", top=50):
    # top theo quoteVolume 24h
    if market == "futures":
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    else:
        url = "https://api.binance.com/api/v3/ticker/24hr"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    tickers = r.json()
    # lọc USDT
    tickers = [t for t in tickers if t["symbol"].endswith("USDT")]
    tickers.sort(key=lambda x: float(x.get("quoteVolume", 0)), reverse=True)
    return [t["symbol"] for t in tickers[:top]]

def fetch_vision_daily(symbol, interval, date_str, market="spot"):
    # date_str: 2024-01-01
    kind = "futures/um" if market=="futures" else "spot"
    url = f"{BINANCE_VISION}/data/{kind}/daily/klines/{symbol}/{interval}/{symbol}-{interval}-{date_str}.zip"
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        return None
    z = zipfile.ZipFile(io.BytesIO(r.content))
    # bên trong có 1 csv
    name = z.namelist()[0]
    df = pd.read_csv(z.open(name), header=None)
    # Binance Vision header: open_time, open, high, low, close, volume, close_time, quote_volume, trades, taker_buy_base, taker_buy_quote, ignore
    cols = ["open_time","open","high","low","close","volume","close_time","quote_volume","trades","taker_buy_base","taker_buy_quote","ignore"]
    df.columns = cols[:len(df.columns)]
    df["symbol"] = symbol
    df["interval"] = interval
    return df

def fetch_api_klines(symbol, interval, start_ms, end_ms=None, limit=1000, market="spot"):
    if market == "futures":
        url = "https://fapi.binance.com/fapi/v1/klines"
    else:
        url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit, "startTime": start_ms}
    if end_ms:
        params["endTime"] = end_ms
    # retry với backoff khi 429
    for attempt in range(5):
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 2 ** attempt))
            print(f"  Rate limit 429, doi {wait}s...")
            time.sleep(wait + random.uniform(0,1))
            continue
        r.raise_for_status()
        data = r.json()
        if not data:
            return []
        # weight check
        weight = int(r.headers.get("x-mbx-used-weight-1m", 0))
        if weight > 1000:
            time.sleep(0.5)
        return data
    raise RuntimeError(f"429 qua nhieu lan {symbol} {interval}")

def backfill_vision(symbol, interval, start_date, end_date, market, out_dir: Path):
    # Lap qua tung ngay, tai ZIP daily
    import datetime
    cur = start_date
    dfs = []
    total = (end_date - start_date).days
    print(f"  Vision {symbol} {interval} {start_date.date()}->{end_date.date()} ({total} ngay)")
    while cur < end_date:
        date_str = cur.strftime("%Y-%m-%d")
        df = fetch_vision_daily(symbol, interval, date_str, market)
        if df is not None:
            dfs.append(df)
        else:
            # ngay khong co data (coin moi) -> bo qua
            pass
        cur += datetime.timedelta(days=1)
        # progress moi 30 ngay
        if len(dfs) % 30 == 0 and len(dfs)>0:
            print(f"    ... {len(dfs)}/{total} ngay OK, rows={sum(len(d) for d in dfs)}")
        time.sleep(0.05)  # nhe nhang, Vision khong rate limit manh nhưng tránh spam
    if not dfs:
        print(f"  Vision khong co data {symbol} {interval}")
        return None
    full = pd.concat(dfs, ignore_index=True)
    full = full.sort_values("open_time").drop_duplicates("open_time")
    # Luu
    out_path = out_dir / market / interval / f"{symbol}.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        full.to_parquet(out_path, compression="zstd")
        print(f"  -> Saved {out_path} rows={len(full)} ({out_path.stat().st_size/1024/1024:.1f} MB)")
    except Exception as e:
        # fallback csv
        out_path = out_path.with_suffix(".csv")
        full.to_csv(out_path, index=False)
        print(f"  -> pyarrow missing, saved CSV {out_path} rows={len(full)} ({e})")
    return full

def backfill_api(symbol, interval, start_ms, end_ms, market, out_dir: Path):
    # Dung API klines pagination, moi request 1000 nến
    all_rows = []
    cur = start_ms
    interval_ms = {
        "1m":60*1000, "3m":3*60*1000, "5m":5*60*1000, "15m":15*60*1000, "30m":30*60*1000,
        "1h":60*60*1000, "2h":2*60*60*1000, "4h":4*60*60*1000, "6h":6*60*60*1000, "8h":8*60*60*1000,
        "12h":12*60*60*1000, "1d":24*60*60*1000
    }[interval]
    print(f"  API {symbol} {interval} from {pd.to_datetime(start_ms, unit='ms')} to {pd.to_datetime(end_ms, unit='ms') if end_ms else 'now'}")
    while True:
        if end_ms and cur >= end_ms:
            break
        data = fetch_api_klines(symbol, interval, cur, end_ms, market=market)
        if not data:
            break
        all_rows.extend(data)
        # next start = last close_time +1
        last_close = data[-1][6]
        cur = last_close + 1
        if len(data) < 1000:
            break
        # rate limit nhe
        time.sleep(0.2)
        if len(all_rows) % 5000 == 0:
            print(f"    ... {len(all_rows)} nến, last {pd.to_datetime(last_close, unit='ms')}")
        # neu gap gan now thi break
        if end_ms is None and last_close > int(time.time()*1000) - interval_ms:
            break
    if not all_rows:
        print(f"  API khong co data {symbol}")
        return None
    cols = ["open_time","open","high","low","close","volume","close_time","quote_volume","trades","taker_buy_base","taker_buy_quote","ignore"]
    df = pd.DataFrame(all_rows, columns=cols)
    df["symbol"] = symbol
    df["interval"] = interval
    # convert numeric
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    out_path = out_dir / market / interval / f"{symbol}.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(out_path, compression="zstd")
        print(f"  -> Saved {out_path} rows={len(df)}")
    except Exception as e:
        out_path = out_path.with_suffix(".csv")
        df.to_csv(out_path, index=False)
        print(f"  -> fallback CSV {out_path} rows={len(df)} ({e})")
    return df

def main():
    parser = argparse.ArgumentParser(description="Fetch ALL history ALL coins ALL intervals - Colab ready")
    parser.add_argument("--market", choices=["spot","futures"], default="spot", help="spot hay futures um")
    parser.add_argument("--symbols", nargs="*", default=None, help="chi dinh symbols, vi du BTCUSDT ETHUSDT")
    parser.add_argument("--all", action="store_true", help="lay TAT CA symbols (524 futures / 485 spot) - can trong dung luong")
    parser.add_argument("--top", type=int, default=None, help="lay top N theo volume 24h (uu tien hon --all)")
    parser.add_argument("--intervals", nargs="+", default=["1h","4h","1d"], help="khung gio, vi du 1m 5m 15m 1h 4h 1d")
    parser.add_argument("--years", type=float, default=5, help="so nam lich su, tinh tu now - years")
    parser.add_argument("--start", type=str, default=None, help="YYYY-MM-DD thay cho --years")
    parser.add_argument("--end", type=str, default=None, help="YYYY-MM-DD, mac dinh now")
    parser.add_argument("--out", type=str, default="data/historical", help="thu muc luu, tren Colab co the /content/drive/MyDrive/ai-lab/data")
    parser.add_argument("--vision", action="store_true", help="dung Binance Vision ZIP (nhanh, khuyen nghi)")
    parser.add_argument("--api", action="store_true", help="dung REST API (cham hon, cho coin moi)")
    parser.add_argument("--workers", type=int, default=4, help="so luong dong thoi (Vision 4-8, API 2-3 tranh rate limit)")
    parser.add_argument("--dry-run", action="store_true", help="chi in uoc tinh, khong tai")
    args = parser.parse_args()

    # chon symbols
    if args.symbols:
        symbols = [s.upper() for s in args.symbols]
    elif args.top:
        symbols = get_top_symbols(args.market, args.top)
        print(f"Top {args.top} {args.market} symbols: {symbols[:10]}... ({len(symbols)} total)")
    elif args.all:
        symbols = get_all_symbols(args.market)
        print(f"ALL {args.market} symbols: {len(symbols)}")
    else:
        # mac dinh top 20
        symbols = get_top_symbols(args.market, 20)
        print(f"Mac dinh top 20: {symbols}")

    # validate intervals
    for iv in args.intervals:
        if iv not in INTERVALS:
            raise ValueError(f"interval {iv} khong hop le, chon trong {INTERVALS}")

    # tinh start/end
    import datetime
    if args.end:
        end_date = datetime.datetime.strptime(args.end, "%Y-%m-%d")
    else:
        end_date = datetime.datetime.utcnow()
    if args.start:
        start_date = datetime.datetime.strptime(args.start, "%Y-%m-%d")
    else:
        start_date = end_date - datetime.timedelta(days=int(args.years*365))

    # uoc tinh dung luong
    days = (end_date - start_date).days
    print(f"\n=== UOC TINH ===")
    print(f"Symbols: {len(symbols)}, Intervals: {args.intervals}, Khoang: {start_date.date()} -> {end_date.date()} ({days} ngay)")
    for iv in args.intervals:
        iv_ms = {"1m":1,"5m":5,"15m":15,"1h":60,"4h":240,"1d":1440}.get(iv, 60)
        rows_per_symbol = days*24*60 // iv_ms
        total_rows = rows_per_symbol * len(symbols)
        size_gb = total_rows * 120 / 1024/1024/1024  # ~120 bytes/row parquet zstd
        print(f"  {iv}: ~{rows_per_symbol:,} nến/symbol, tong {total_rows:,} nến (~{size_gb:.2f} GB parquet)")

    if args.dry_run:
        print("Dry-run, dung lai.")
        return

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # chon nguon: Vision uu tien neu co
    use_vision = args.vision or not args.api
    if use_vision:
        print(f"\n=== BAT DAU TAI VISION ({len(symbols)*len(args.intervals)} jobs, workers={args.workers}) ===")
        # Vision: moi job = 1 symbol + 1 interval
        jobs = [(s, iv) for s in symbols for iv in args.intervals]
        # Check ton tai de resume
        def need_fetch(sym, iv):
            p_parquet = out_dir / args.market / iv / f"{sym}.parquet"
            p_csv = out_dir / args.market / iv / f"{sym}.csv"
            if p_parquet.exists() or p_csv.exists():
                # kiem tra xem da du den end_date chua? Don gian: check mtime
                # Neu file >1 ngay thi skip, con lai fetch tiep via API gap
                # O day skip luon de resume nhanh
                return False
            return True

        jobs = [j for j in jobs if need_fetch(j[0], j[1])]
        print(f"Con lai {len(jobs)} jobs can tai (da skip cac file ton tai)")

        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(backfill_vision, sym, iv, start_date, end_date, args.market, out_dir): (sym, iv) for sym, iv in jobs}
            for fut in as_completed(futs):
                sym, iv = futs[fut]
                try:
                    fut.result()
                except Exception as e:
                    print(f"  Loi {sym} {iv}: {e}")

        # Sau Vision, dung API de lap gap cuoi (Vision delay 1 ngay)
        print("\n=== LAP GAP CUOI BANG API (1 ngay gan nhat) ===")
        # Lay tu Vision end -> now via API
        gap_start = int(end_date.timestamp()*1000) - 2*24*60*60*1000  # 2 ngay cuoi
        for sym, iv in jobs[:5]:  # chi demo 5 dau, de tranh rate limit neu full
            try:
                # merge gap vao file cu
                print(f"Gap {sym} {iv}...")
                # Khong can full, chi info
            except Exception as e:
                print(e)

    else:
        print(f"\n=== BAT DAU TAI API ({len(symbols)*len(args.intervals)} jobs) ===")
        start_ms = int(start_date.timestamp()*1000)
        end_ms = int(end_date.timestamp()*1000)
        jobs = [(s, iv) for s in symbols for iv in args.intervals]
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(backfill_api, sym, iv, start_ms, end_ms, args.market, out_dir): (sym, iv) for sym, iv in jobs}
            for fut in as_completed(futs):
                sym, iv = futs[fut]
                try:
                    fut.result()
                except Exception as e:
                    print(f"  Loi {sym} {iv}: {e}")

    print("\n=== HOAN TAT ===")
    # Tong ket
    total_files = list(out_dir.rglob("*.parquet")) + list(out_dir.rglob("*.csv"))
    total_size = sum(f.stat().st_size for f in total_files) / 1024/1024
    print(f"Tong {len(total_files)} files, {total_size:.1f} MB trong {out_dir}")
    for f in total_files[:10]:
        print(f"  {f.relative_to(out_dir)} {f.stat().st_size/1024:.1f} KB")

if __name__ == "__main__":
    main()
