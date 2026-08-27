"""Entry point cho AI Crypto Trading Lab."""
import asyncio
import argparse
from pathlib import Path
import yaml
from src.utils.logger import get_logger
logger = get_logger('main')

def load_config(path: str = 'config/app.yaml'):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)

async def main():
    parser = argparse.ArgumentParser(description='AI Crypto Trading Lab')
    parser.add_argument('--config', default='config/app.yaml')
    parser.add_argument('--mode', choices=['collect','train','simulate','paper'], default='collect')
    args = parser.parse_args()
    cfg = load_config(args.config)
    logger.info(f"Khoi dong lab mode={args.mode} config={args.config}")
    print(f"[LAB] Mode={args.mode} - Thi truong that, tien ao, san mo phong")

if __name__ == '__main__':
    asyncio.run(main())
