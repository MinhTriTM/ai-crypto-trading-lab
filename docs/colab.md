# Colab — Lấy Data Trước + Futures x500 20→500

> Notebook: `colab/AI_Crypto_Lab_Colab.ipynb` — mở trực tiếp trên Colab: `File → Upload notebook`.

## 1. Tại sao phải lấy data trước?

Lab tuân thủ **thị trường thật, tiền ảo** — không fake chart. Trước khi cho AI trade, cần **tất cả nến** mọi khung để:
- `historical_intelligence/pattern_memory.py` học xác suất tương lai
- `branching` sinh hàng nghìn hướng và `simulation` đánh giá `reach_rate`
- `training` không bị lookahead (`market/clock/market_clock.py:14`)

Colab T4 (12GB) đủ cho **1h/4h/1d 5 năm 50 coin ~0.2GB**; **1m 9 năm 300 coin ~135GB không vừa** → phải chọn lọc.

## 2. Lệnh fetch đã test (Vision 30s cho 5 coin 1h 36 ngày)

```bash
# Cài (Colab)
!pip install -q -r requirements.txt
!pip install -q pyarrow  # để lưu parquet, không bắt buộc (fallback CSV)

# Kiểm tra realtime (phải ra giá thật)
python -c "import requests; print(requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=5).json())"
# -> {'symbol':'BTCUSDT','price':'80287.79'}

# Ước tính trước
python scripts/fetch_all_history.py --market spot --top 50 --intervals 1h 4h 1d --years 5 --dry-run
# 1h: ~43800 nến/symbol, 50 coin 5 năm ~0.20 GB

# Chạy thật (resume tự skip file đã tồn tại)
python scripts/fetch_all_history.py --market spot --top 50 --intervals 1h 4h 1d --years 5 --vision --workers 4 --out /content/drive/MyDrive/ai-lab/data/historical

# All coin (cẩn trọng)
python scripts/fetch_all_history.py --market spot --all --intervals 1h --years 5 --vision --workers 8 --out data/historical
python scripts/fetch_all_history.py --market futures --all --intervals 15m 1h 4h --years 3 --vision --workers 8 --out data/historical

# Demo đã chạy: 5 coin 1h 36 ngày -> 864 nến/coin, BTC 65098 -> 80731
python scripts/fetch_all_history.py --market spot --top 5 --intervals 1h --years 0.1 --vision --workers 3 --out data/historical
ls -lh data/historical/spot/1h/  # BTCUSDT.csv 120KB
```

Nguồn: `https://data.binance.vision/data/<spot|futures>/daily/klines/<SYMBOL>/<interval>/<SYMBOL>-<interval>-2024-01-01.zip` (`scripts/fetch_all_history.py:30`), nhanh hơn REST 10x.

## 3. Futures x500 20→500 — Kết quả thật 1000 nhánh

```bash
python scripts/evaluate_futures_x500.py --data data/historical --market spot --intervals 1h --top 5 --episodes 1000 --initial 20 --target 500 --max-leverage 500
```

Đã chạy trên 5 coin 1h thật (BTC 65098→80731, 864 nến):

```
Total episodes: 1000
Dat target 20->500 (x25.0): 1/1000 = 0.10%
Pha san (<10%): 284/1000 = 28.4%
Liquidated: 425/1000 = 42.5%
Avg final: 16.67, Best: 515.63 (SOL 1h hold_long x20 pos100%)
Theo leverage: x20 0.9% avg26.4 (tốt nhất), x500 0% avg5.1 liq52% bankrupt66%
Theo strategy: hold_long 0.8% avg43 (tốt nhất), rsi 0% avg9.1
>>> KET LUAN: TE - Cực khó, <2% đạt, x500 liquidation cao, khuyến nghị giảm leverage
Saved runs/evaluation/futures_x500.json
```

**Luật đã encode** (`scripts/evaluate_futures_x500.py:70`):
- Fee taker 0.04%, liquidation fee 0.5%
- Liquidation `liq = entry*(1±0.9/leverage)` → x500 chỉ lệch **0.18%** là cháy (`src/exchange_simulator/derivatives/liquidation.py:13`)
- Strategies: `ma_cross`, `rsi`, `breakout` (Bollinger), `mean_revert`, `trend`, `hold_long`, `random` với MA/RSI/BB/vol (`src/market/features/*`)
- Position 5-100%, leverage 5-500, auto giảm pos xuống 10% khi vol>2%

**Vì sao x500 tệ?** Để x25 cần +5% giá nếu all-in x500, nhưng -0.18% đã cháy → chỉ sống với pos nhỏ 5-10% và winrate >55% liên tiếp, rất hiếm. `x20` cần +125% giá nhưng khoảng cách liq 4.5% nên sống lâu hơn và compound được.

**Thử cấu hình dễ hơn:**
```bash
# Giảm target xuống 100 (x5) với x20
python scripts/evaluate_futures_x500.py --intervals 1h 4h --top 20 --episodes 2000 --initial 20 --target 100 --max-leverage 20
# Chỉ hold_long trend
python scripts/evaluate_futures_x500.py --symbols BTCUSDT ETHUSDT SOLUSDT --intervals 15m 1h --episodes 5000 --initial 20 --target 500 --max-leverage 125
```

## 4. Colab steps tóm tắt

1. Mount Drive, clone, pip
2. `fetch_all_history.py --vision` lấy data trước (bắt đầu top 50 1h 4h 1d)
3. `evaluate_futures_x500.py` chạy nhánh và đọc `runs/evaluation/futures_x500.json` để kết luận ĐẠT/TỆ
4. Nếu đạt <2%, giảm leverage, đổi strategy, hoặc tăng vốn lên 100 trước khi nghĩ x500.

## 5. Tích hợp luật & kiến thức trade

Thêm rule mới vào `scripts/evaluate_futures_x500.py:70` hoặc `src/risk/risk_engine.py:12` + `src/market/features/`:

- Funding: `src/market/features/funding.py` (funding >0.001 thì short bias)
- Kelly: `src/risk/position_sizing.py:4` `kelly_fraction`
- Drawdown: `src/risk/drawdown.py:4` dừng khi `max_dd>15%`
- Pattern: `src/historical_intelligence/pattern_memory.py:11` thay `random` bằng `nearest_neighbors` k=20

Docs: `docs/architecture.md`, `docs/virtual-exchange.md`, `colab/AI_Crypto_Lab_Colab.ipynb`
