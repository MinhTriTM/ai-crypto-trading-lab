# AI Crypto Trading Lab

> **Thị trường thật — Tiền ảo — Sàn mô phỏng — AI tự học**

Hệ thống lab giao dịch crypto dùng dữ liệu thị trường thật, tài khoản ảo hoàn toàn tách biệt, sàn giao dịch mô phỏng và AI training qua hàng triệu branching simulation.

## Kiến trúc tổng quan

```
              REAL EXCHANGES (Binance / Bybit / OKX)
                         │
               ┌─────────┴─────────┐
               │                   │
         Historical Data      Live WebSocket
               │                   │
               └─────────┬─────────┘
                         ▼
                   MARKET ENGINE
                         │
                         ▼
                     AI BRAIN
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        Account 1    Account 2    Account N  ($1000 ảo)
            │            │            │
            └────────────┼────────────┘
                         ▼
                VIRTUAL EXCHANGE
         fee / funding / spread / slippage / latency / liquidation
                         │
                         ▼
                EXPERIENCE ENGINE
                         │
                         ▼
                    AI TRAINING ───↺
```

**Nguyên tắc cốt lõi:** Thị trường là thật, dữ liệu là thật, thời gian & biến động là thật — nhưng tiền, vị thế và lệnh hoàn toàn trong simulator. Không có tiền thật nào được đặt vào thị trường.

## 8 Module lõi

| Module | Vai trò |
|--------|---------|
| `market/` | Thu thập dữ liệu giá/orderbook thật qua WebSocket |
| `historical_intelligence/` | Học lịch sử, tìm pattern tương tự, tránh đoán mò |
| `portfolio/` | Tài khoản & tiền hoàn toàn ảo |
| `exchange_simulator/` | Giả lập sàn thật (fee, slippage, latency, liquidation) |
| `branching/` | Tạo N hướng đi song song từ cùng một market state |
| `simulation/` | Chạy hàng triệu episode |
| `training/` | Học từ tất cả kết quả (PPO/SAC/TD3/Evolutionary) |
| `paper_trading/` | Thi với thị trường realtime |

## Cây thư mục

Xem chi tiết trong `docs/architecture.md`. Cấu trúc tuân thủ spec V1 trong `chat.txt`.

## Quick Start

```bash
# 1. Cài đặt
pip install -r requirements.txt
# hoặc với pyproject
pip install -e .

# 2. Cấu hình
copy .env.example .env
# chỉnh sửa .env với API keys (chỉ dùng cho market data, không trade thật)

# 3. Chạy với Docker
docker-compose up -d

# 4. Thu thập dữ liệu lịch sử
python scripts/download_history.py --symbol BTCUSDT --days 30

# 5. Train
python scripts/train.py --config config/training.yaml

# 6. Simulate
python scripts/simulate.py --episodes 10000

# 7. Paper trading realtime
python scripts/paper_trade.py --symbol BTCUSDT

# 8. Evaluate
python scripts/evaluate.py --run runs/training/latest
```

## Hai chế độ

- **Historical Replay:** Replay dữ liệu đã xảy ra, tua nhanh hàng triệu lần, AI không được nhìn tương lai.
- **Live Paper Trading:** Dùng WebSocket realtime, thời gian 1:1 với thị trường, để kiểm nghiệm & đo robustness.

## Cấu hình

Tất cả config nằm trong `config/`:
`app.yaml`, `database.yaml`, `exchanges.yaml`, `markets.yaml`, `simulator.yaml`, `training.yaml`, `risk.yaml`, `logging.yaml`

## License

MIT
