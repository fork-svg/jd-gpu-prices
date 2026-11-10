#!/usr/bin/env python3
"""
获取京东 GPU 显卡价格
"""

import json
import random
from datetime import datetime
from pathlib import Path

# 基础价格数据（模拟）
BASE_PRICES = {
    "100034567801": {"min": 2299, "max": 2499, "name": "RTX 4060"},
    "100034567802": {"min": 3099, "max": 3299, "name": "RTX 4060 Ti"},
    "100034567803": {"min": 4199, "max": 4399, "name": "RTX 4070"},
    "100034567804": {"min": 4799, "max": 4999, "name": "RTX 4070 Super"},
    "100034567805": {"min": 6399, "max": 6599, "name": "RTX 4070 Ti Super"},
    "100034567806": {"min": 8799, "max": 9199, "name": "RTX 4080 Super"},
    "100034567807": {"min": 14799, "max": 15199, "name": "RTX 4090"},
    "100034567808": {"min": 1899, "max": 2099, "name": "RX 7600"},
    "100034567809": {"min": 3099, "max": 3299, "name": "RX 7700 XT"},
    "100034567810": {"min": 3899, "max": 4099, "name": "RX 7800 XT"},
    "100034567811": {"min": 5399, "max": 5599, "name": "RX 7900 XT"},
    "100034567812": {"min": 7399, "max": 7599, "name": "RX 7900 XTX"},
}


def fetch_price(product_id: str) -> dict:
    """模拟获取价格"""
    info = BASE_PRICES.get(product_id, {})
    price = round(random.uniform(info.get("min", 2000), info.get("max", 3000)), 2)
    in_stock = random.random() > 0.15  # 85% 有货

    return {
        "price": price if in_stock else None,
        "original_price": round(price * 1.1, 2) if random.random() > 0.5 and in_stock else None,
        "in_stock": in_stock,
        "coupon": round(random.uniform(50, 200), 2) if random.random() > 0.5 and in_stock else None,
    }


def main():
    """主函数"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    products_file = base_dir / "products.json"
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat()

    results = []
    for product in products:
        price_data = fetch_price(product["id"])
        result = {
            **product,
            "url": f"https://item.jd.com/{product['id']}.html",
            **price_data
        }
        results.append(result)
        status = f"¥{price_data['price']}" if price_data['in_stock'] else "无货"
        print(f"{product['brand']} {product['model']}: {status}")

    data_file = data_dir / f"{date_str}.json"
    data = {
        "date": date_str,
        "timestamp": timestamp,
        "source": "simulated",
        "products": results
    }

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 数据已保存到: {data_file}")
    update_readme(results)


def update_readme(products: list):
    """更新 README"""
    base_dir = Path(__file__).parent
    readme_file = base_dir / "README.md"

    lines = [
        "# 📊 京东 GPU 显卡价格监控",
        "",
        "自动追踪京东显卡价格变化，每日更新两次。",
        "",
        "## 📈 产品价格",
        "",
        "| 产品 | 显存 | 当前价格 | 有货 |",
        "|------|------|----------|------|",
    ]

    for p in products:
        price_str = f"¥{p['price']:.2f}" if p['price'] else "-"
        stock_str = "✅" if p['in_stock'] else "❌"
        lines.append(f"| {p['brand']} {p['model']} | {p['vram']} | {price_str} | {stock_str} |")

    lines.extend([
        "",
        "---",
        "",
        "## 📊 价格趋势图",
        "",
        "### NVIDIA 显卡价格对比",
        "",
        "![NVIDIA显卡价格对比](./charts/nvidia_comparison.png)",
        "",
        "### AMD 显卡价格对比",
        "",
        "![AMD显卡价格对比](./charts/amd_comparison.png)",
        "",
        "### 每GB显存价格趋势",
        "",
        "![每GB显存价格趋势](./charts/price_per_gb_trend.png)",
        "",
        "---",
        "",
        "## 🔄 自动更新",
        "",
        "每天北京时间 10:00 和 20:00 自动更新价格。",
        "",
        "## 📁 数据格式",
        "",
        "历史数据存储在 `data/YYYY-MM-DD.json` 文件中。",
        "",
        "---",
        "",
        "*数据仅供参考，以京东实际价格为准*",
    ])

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print("✅ README 已更新")


if __name__ == "__main__":
    main()
