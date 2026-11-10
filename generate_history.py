#!/usr/bin/env python3
"""
生成历史测试数据
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 基础价格数据
BASE_PRICES = {
    "100034567801": {"base": 2399, "variance": 150, "name": "RTX 4060", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4060", "vram": "8GB"},
    "100034567802": {"base": 3199, "variance": 200, "name": "RTX 4060 Ti", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4060 Ti", "vram": "8GB"},
    "100034567803": {"base": 4299, "variance": 250, "name": "RTX 4070", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4070", "vram": "12GB"},
    "100034567804": {"base": 4899, "variance": 300, "name": "RTX 4070 Super", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4070 Super", "vram": "12GB"},
    "100034567805": {"base": 6499, "variance": 400, "name": "RTX 4070 Ti Super", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4070 Ti Super", "vram": "16GB"},
    "100034567806": {"base": 8999, "variance": 500, "name": "RTX 4080 Super", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4080 Super", "vram": "16GB"},
    "100034567807": {"base": 14999, "variance": 800, "name": "RTX 4090", "category": "NVIDIA显卡", "brand": "七彩虹", "model": "RTX 4090", "vram": "24GB"},
    "100034567808": {"base": 1999, "variance": 120, "name": "RX 7600", "category": "AMD显卡", "brand": "蓝宝石", "model": "RX 7600", "vram": "8GB"},
    "100034567809": {"base": 3199, "variance": 200, "name": "RX 7700 XT", "category": "AMD显卡", "brand": "蓝宝石", "model": "RX 7700 XT", "vram": "12GB"},
    "100034567810": {"base": 3999, "variance": 250, "name": "RX 7800 XT", "category": "AMD显卡", "brand": "蓝宝石", "model": "RX 7800 XT", "vram": "16GB"},
    "100034567811": {"base": 5499, "variance": 350, "name": "RX 7900 XT", "category": "AMD显卡", "brand": "蓝宝石", "model": "RX 7900 XT", "vram": "20GB"},
    "100034567812": {"base": 7499, "variance": 450, "name": "RX 7900 XTX", "category": "AMD显卡", "brand": "蓝宝石", "model": "RX 7900 XTX", "vram": "24GB"},
}


def generate_day_data(date_str: str) -> dict:
    """生成某一天的价格数据"""
    products = []

    for product_id, info in BASE_PRICES.items():
        price = info["base"] + random.uniform(-info["variance"], info["variance"])
        price = round(price, 2)
        in_stock = random.random() > 0.15

        product_data = {
            "id": product_id,
            "name": info["name"],
            "category": info["category"],
            "brand": info["brand"],
            "model": info["model"],
            "vram": info["vram"],
            "url": f"https://item.jd.com/{product_id}.html",
            "price": price if in_stock else None,
            "original_price": round(price * 1.1, 2) if random.random() > 0.5 and in_stock else None,
            "in_stock": in_stock,
            "coupon": round(random.uniform(50, 200), 2) if random.random() > 0.5 and in_stock else None,
        }
        products.append(product_data)

    return {
        "date": date_str,
        "timestamp": f"{date_str}T10:00:00.000000",
        "source": "simulated",
        "products": products
    }


def main():
    """生成过去30天的历史数据"""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    today = datetime.now()

    for i in range(30, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        data_file = data_dir / f"{date_str}.json"

        if not data_file.exists():
            data = generate_day_data(date_str)
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"生成数据: {date_str}")

    print("✅ 历史数据生成完成")


if __name__ == "__main__":
    main()
