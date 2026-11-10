#!/usr/bin/env python3
"""
生成 GPU 显卡价格趋势图
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path


def load_historical_data(data_dir: Path) -> dict:
    """加载历史价格数据"""
    data = {}

    for json_file in sorted(data_dir.glob("*.json")):
        with open(json_file, 'r', encoding='utf-8') as f:
            day_data = json.load(f)
            date_str = day_data.get('date', json_file.stem)

            for product in day_data.get('products', []):
                if product.get('in_stock') and product.get('price'):
                    product_id = product['id']
                    if product_id not in data:
                        data[product_id] = {
                            'name': product['name'],
                            'category': product['category'],
                            'brand': product['brand'],
                            'model': product['model'],
                            'vram': product['vram'],
                            'dates': [],
                            'prices': []
                        }

                    data[product_id]['dates'].append(datetime.strptime(date_str, '%Y-%m-%d'))
                    data[product_id]['prices'].append(product['price'])

    return data


def generate_individual_charts(data: dict, output_dir: Path):
    """为每个产品生成单独的价格曲线图"""
    output_dir.mkdir(exist_ok=True)

    for product_id, product_data in data.items():
        if len(product_data['dates']) < 2:
            continue

        fig, ax = plt.subplots(figsize=(12, 6))

        color = '#76B900' if 'NVIDIA' in product_data['category'] else '#ED1C24'
        ax.plot(product_data['dates'], product_data['prices'],
                marker='o', linewidth=2, markersize=6, color=color)

        title = f"{product_data['brand']} {product_data['model']} {product_data['vram']}\nPrice History"
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (CNY)', fontsize=12)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        ax.grid(True, linestyle='--', alpha=0.6)

        min_price = min(product_data['prices']) * 0.95
        max_price = max(product_data['prices']) * 1.05
        ax.set_ylim(min_price, max_price)

        current_price = product_data['prices'][-1]
        current_date = product_data['dates'][-1]
        ax.annotate(f'¥{current_price:.2f}',
                   xy=(current_date, current_price),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                   fontsize=10, fontweight='bold')

        avg_price = sum(product_data['prices']) / len(product_data['prices'])
        min_p = min(product_data['prices'])
        max_p = max(product_data['prices'])

        stats_text = f'Avg: CNY{avg_price:.2f}\nMin: CNY{min_p:.2f}\nMax: CNY{max_p:.2f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        safe_name = f"{product_id}_{product_data['model']}_{product_data['vram']}".replace(' ', '_')
        fig.savefig(output_dir / f"{safe_name}.png", dpi=150, bbox_inches='tight')
        plt.close(fig)


def generate_category_charts(data: dict, output_dir: Path):
    """按品牌类别生成对比图"""
    if not data:
        return

    categories = {}
    for product_id, product_data in data.items():
        if len(product_data['dates']) < 2:
            continue

        category = product_data['category']
        if category not in categories:
            categories[category] = []

        categories[category].append((product_id, product_data))

    colors = plt.cm.viridis.colors

    for category, products in categories.items():
        fig, ax = plt.subplots(figsize=(14, 8))

        for (product_id, product_data), color in zip(products, colors):
            label = f"{product_data['model']} {product_data['vram']}"
            ax.plot(product_data['dates'], product_data['prices'],
                   marker='o', linewidth=2, markersize=5,
                   label=label, color=color)

        safe_category = category.replace(' ', '_').lower()
        ax.set_title(f'{category} - Price Comparison', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (CNY)', fontsize=12)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best', fontsize=9)

        plt.tight_layout()
        fig.savefig(output_dir / f"{safe_category}_comparison.png", dpi=150, bbox_inches='tight')
        plt.close(fig)


def generate_per_gb_analysis(data: dict, output_dir: Path):
    """生成每GB显存价格分析图"""
    if not data:
        return

    fig, ax = plt.subplots(figsize=(14, 8))

    for product_id, product_data in data.items():
        if len(product_data['dates']) < 2:
            continue

        vram_num = float(product_data['vram'].replace('GB', ''))
        per_gb_prices = [p / vram_num for p in product_data['prices']]

        color = '#76B900' if 'NVIDIA' in product_data['category'] else '#ED1C24'
        label = f"{product_data['brand']} {product_data['model']}"
        ax.plot(product_data['dates'], per_gb_prices,
               marker='s', linewidth=2, markersize=5,
               label=label, color=color)

    ax.set_title('Price per GB VRAM Trend', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price per GB (CNY)', fontsize=12)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='best', fontsize=8, ncol=2)

    plt.tight_layout()
    fig.savefig(output_dir / "price_per_gb_trend.png", dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    """主函数"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    charts_dir = base_dir / "charts"

    print("加载历史价格数据...")
    data = load_historical_data(data_dir)

    if not data:
        print("没有找到历史数据")
        return

    print(f"找到 {len(data)} 个产品的历史数据")

    print("生成单独产品价格曲线...")
    generate_individual_charts(data, charts_dir)

    print("生成品牌类别对比图...")
    generate_category_charts(data, charts_dir)

    print("生成每GB显存价格趋势图...")
    generate_per_gb_analysis(data, charts_dir)

    print(f"✅ 图表已保存到: {charts_dir}")


if __name__ == "__main__":
    main()
