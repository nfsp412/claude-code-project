"""
销售数据分析 Streamlit 仪表盘

基于 Jupyter notebook 转换的交互式销售数据分析仪表盘。
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
import sys

# 添加 sales_analysis 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import SalesDataLoader
from business_calc import SalesMetricsCalculator

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'Songti SC', 'STFangsong', 'Microsoft YaHei', 'SimHei', 'WenQuanYi Micro Hei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('whitegrid')

# 配色方案
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#2ECC71',
    'warning': '#E74C3C',
    'palette': ['#2E86AB', '#A23B72', '#F18F01', '#2ECC71', '#E74C3C', '#8E44AD', '#1ABC9C', '#F39C12']
}


def init_data(excel_path: str):
    """初始化数据"""
    loader = SalesDataLoader(excel_path)
    data = loader.load_all()
    calculator = SalesMetricsCalculator(
        orders=data['orders'],
        products=data['products'],
        customers=data['customers'],
        targets=data['targets']
    )
    return loader, calculator, data


def render_sidebar():
    """渲染侧边栏"""
    st.sidebar.header("导航")
    sections = [
        "首页",
        "核心业务指标",
        "区域销售分析",
        "产品分析",
        "客户分析",
        "时间趋势分析",
        "产品类别分析",
        "数据字典"
    ]
    selected = st.sidebar.radio("选择页面", sections)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 关于")
    st.sidebar.info("销售数据分析仪表盘 v1.0")

    return selected


def render_home(loader, calculator):
    """渲染首页"""
    st.title("销售数据分析仪表盘")
    st.markdown("欢迎使用销售数据分析仪表盘，本仪表盘提供多维度的销售数据可视化分析。")

    # 数据概览
    st.header("数据概览")
    info = loader.get_data_info()

    cols = st.columns(3)
    metrics = [
        ("订单总数", info["订单总数"]),
        ("唯一客户数", info["唯一客户数"]),
        ("唯一产品数", info["唯一产品数"]),
        ("销售区域数", info["销售区域数"]),
        ("总销售额", info["总销售额"]),
        ("数据时间范围", info["数据时间范围"]),
    ]

    for i, (label, value) in enumerate(metrics):
        with cols[i % 3]:
            st.metric(label, value)

    # 关键发现
    st.header("关键发现")
    st.markdown("""
    ### 主要发现
    1. **区域表现**：华东地区销售额最高，占总销售额的重要比例
    2. **产品表现**：笔记本电脑是销售额最高的产品
    3. **客户类型**：企业客户和个人客户的销售额相对均衡
    4. **时间趋势**：5 月份销售额达到峰值

    ### 建议
    - 重点关注华东地区的市场维护
    - 对低销量产品考虑促销策略
    - 针对企业客户开发更多高价值产品
    - 分析销售低谷期的原因并制定对策
    """)


def render_metrics(calculator):
    """渲染核心业务指标"""
    st.title("核心业务指标")

    metrics = calculator.get_summary_metrics()

    # 创建指标卡片
    cols = st.columns(4)
    metrics_list = [
        ("总销售额", f"¥{metrics['总销售额']:,.2f}", COLORS['primary']),
        ("总订单数", f"{metrics['总订单数']:,}", COLORS['secondary']),
        ("活跃客户数", f"{metrics['活跃客户数']:,}", COLORS['accent']),
        ("销售产品数", f"{metrics['销售产品数']:,}", COLORS['success']),
        ("毛利润", f"¥{metrics['毛利润']:,.2f}", COLORS['warning']),
        ("整体毛利率", f"{metrics['整体毛利率']:.2f}%", COLORS['primary']),
        ("平均订单金额", f"¥{metrics['平均订单金额']:,.2f}", COLORS['secondary']),
        ("客单价", f"¥{metrics['客单价']:,.2f}", COLORS['accent']),
    ]

    for i, (label, value, color) in enumerate(metrics_list):
        with cols[i % 4]:
            st.metric(label, value)

    # 指标表格
    st.subheader("指标明细")
    metrics_df = pd.DataFrame({
        '指标': ['总销售额', '总订单数', '活跃客户数', '销售产品数', '毛利润', '整体毛利率', '平均订单金额', '客单价'],
        '数值': [
            f"¥{metrics['总销售额']:,.2f}",
            f"{metrics['总订单数']:,}",
            f"{metrics['活跃客户数']:,}",
            f"{metrics['销售产品数']:,}",
            f"¥{metrics['毛利润']:,.2f}",
            f"{metrics['整体毛利率']:.2f}%",
            f"¥{metrics['平均订单金额']:,.2f}",
            f"¥{metrics['客单价']:,.2f}"
        ]
    })
    st.dataframe(metrics_df, hide_index=True, use_container_width=True)


def render_regional_analysis(calculator):
    """渲染区域销售分析"""
    st.title("区域销售分析")

    region_sales = calculator.get_regional_sales()

    # 创建可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 区域销售额柱状图
    ax1 = axes[0, 0]
    bars1 = ax1.barh(region_sales['region'], region_sales['总销售额'], color=COLORS['palette'][:len(region_sales)])
    ax1.set_xlabel('Sales Amount (CNY)')
    ax1.set_title('Total Sales by Region', fontsize=14, fontweight='bold')
    for bar, val in zip(bars1, region_sales['总销售额']):
        ax1.text(val + 1000, bar.get_y() + bar.get_height()/2, f'¥{val:,.0f}', va='center', fontsize=9)

    # 2. 区域销售占比饼图
    ax2 = axes[0, 1]
    wedges, texts, autotexts = ax2.pie(region_sales['总销售额'], labels=region_sales['region'],
                                         autopct='%1.1f%%', colors=COLORS['palette'][:len(region_sales)])
    ax2.set_title('Sales Share by Region', fontsize=14, fontweight='bold')

    # 3. 区域订单数分布
    ax3 = axes[1, 0]
    bars3 = ax3.bar(region_sales['region'], region_sales['订单数'], color=COLORS['secondary'])
    ax3.set_ylabel('Number of Orders')
    ax3.set_title('Order Count by Region', fontsize=14, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    for bar, val in zip(bars3, region_sales['订单数']):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}', ha='center', fontsize=9)

    # 4. 区域平均订单金额
    ax4 = axes[1, 1]
    bars4 = ax4.bar(region_sales['region'], region_sales['平均订单金额'], color=COLORS['accent'])
    ax4.set_ylabel('Average Order Value (CNY)')
    ax4.set_title('Average Order Value by Region', fontsize=14, fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    for bar, val in zip(bars4, region_sales['平均订单金额']):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, f'¥{val:.0f}', ha='center', fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)

    # 显示详细数据
    st.subheader("区域销售详细数据")
    display_df = region_sales.copy()
    display_df['总销售额'] = display_df['总销售额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['平均订单金额'] = display_df['平均订单金额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['销售占比'] = display_df['销售占比'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(display_df, hide_index=True, use_container_width=True)


def render_product_analysis(calculator):
    """渲染产品分析"""
    st.title("产品分析")

    product_sales = calculator.get_product_sales()

    # 创建可视化
    fig = plt.figure(figsize=(16, 12))

    # 1. 产品销售额排行（TOP 10）
    ax1 = plt.subplot(2, 2, 1)
    top10 = product_sales.head(10)
    bars1 = ax1.barh(range(len(top10)), top10['总销售额'], color=COLORS['palette'][:len(top10)])
    ax1.set_yticks(range(len(top10)))
    ax1.set_yticklabels(top10['product_name'])
    ax1.set_xlabel('Sales Amount (CNY)')
    ax1.set_title('Top 10 Products by Sales', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()
    for bar, val in zip(bars1, top10['总销售额']):
        ax1.text(val + 3000, bar.get_y() + bar.get_height()/2, f'¥{val:,.0f}', va='center', fontsize=9)

    # 2. 产品销量 vs 销售额散点图
    ax2 = plt.subplot(2, 2, 2)
    scatter = ax2.scatter(product_sales['总销量'], product_sales['总销售额'],
                          s=product_sales['毛利率']/2, c=product_sales['毛利率'],
                          cmap='RdYlGn', alpha=0.7, edgecolors='black')
    ax2.set_xlabel('Total Sales Volume')
    ax2.set_ylabel('Total Sales Amount (CNY)')
    ax2.set_title('Product Volume vs Sales vs Gross Margin', fontsize=14, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.7)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Gross Margin (%)')

    # 3. 产品销量分布
    ax3 = plt.subplot(2, 2, 3)
    ax3.bar(product_sales['product_name'], product_sales['总销量'], color=COLORS['success'])
    ax3.set_ylabel('Sales Volume')
    ax3.set_title('Sales Volume by Product', fontsize=14, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)

    # 4. 产品毛利率对比
    ax4 = plt.subplot(2, 2, 4)
    bars4 = ax4.bar(product_sales['product_name'], product_sales['毛利率'], color=COLORS['warning'])
    ax4.set_ylabel('Gross Margin (%)')
    ax4.set_title('Gross Margin by Product', fontsize=14, fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    ax4.axhline(y=product_sales['毛利率'].mean(), color='r', linestyle='--', label=f"Avg: {product_sales['毛利率'].mean():.1f}%")
    ax4.legend()

    plt.tight_layout()
    st.pyplot(fig)

    # 显示详细数据
    st.subheader("产品销售详细数据")
    display_columns = ['product_name', '总销量', '总销售额', '平均订单金额', '订单数', '毛利率']
    display_df = product_sales[display_columns].copy()
    display_df['总销售额'] = display_df['总销售额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['平均订单金额'] = display_df['平均订单金额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['毛利率'] = display_df['毛利率'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(display_df, hide_index=True, use_container_width=True)


def render_customer_analysis(calculator):
    """渲染客户分析"""
    st.title("客户分析")

    customer_analysis = calculator.get_customer_type_analysis()

    # 创建可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 1. 客户类型销售额对比
    ax1 = axes[0]
    bars1 = ax1.bar(customer_analysis['customer_type'], customer_analysis['总销售额'],
                    color=[COLORS['primary'], COLORS['secondary']])
    ax1.set_ylabel('Sales Amount (CNY)')
    ax1.set_title('Total Sales by Customer Type', fontsize=14, fontweight='bold')
    for bar, val in zip(bars1, customer_analysis['总销售额']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000, f'¥{val:,.0f}', ha='center', fontsize=10)

    # 2. 客户类型订单数对比
    ax2 = axes[1]
    bars2 = ax2.bar(customer_analysis['customer_type'], customer_analysis['订单数'],
                    color=[COLORS['accent'], COLORS['success']])
    ax2.set_ylabel('Number of Orders')
    ax2.set_title('Order Count by Customer Type', fontsize=14, fontweight='bold')
    for bar, val in zip(bars2, customer_analysis['订单数']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}', ha='center', fontsize=10)

    # 3. 客户类型平均订单金额对比
    ax3 = axes[2]
    bars3 = ax3.bar(customer_analysis['customer_type'], customer_analysis['平均订单金额'],
                    color=[COLORS['warning'], COLORS['success']])
    ax3.set_ylabel('Average Order Value (CNY)')
    ax3.set_title('Average Order Value by Customer Type', fontsize=14, fontweight='bold')
    for bar, val in zip(bars3, customer_analysis['平均订单金额']):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, f'¥{val:.0f}', ha='center', fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)

    # 显示详细数据
    st.subheader("客户类型分析详细数据")
    display_df = customer_analysis.copy()
    display_df['总销售额'] = display_df['总销售额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['平均订单金额'] = display_df['平均订单金额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['销售占比'] = display_df['销售占比'].apply(lambda x: f"{x:.2f}%")
    display_df['标准差'] = display_df['标准差'].apply(lambda x: f"{x:.2f}")
    st.dataframe(display_df, hide_index=True, use_container_width=True)


def render_time_analysis(calculator):
    """渲染时间趋势分析"""
    st.title("时间趋势分析")

    monthly_sales = calculator.get_monthly_trend()

    # 创建可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 月度销售额趋势
    ax1 = axes[0, 0]
    ax1.plot(monthly_sales['month'], monthly_sales['销售额'], marker='o', linewidth=2,
             markersize=8, color=COLORS['primary'])
    ax1.fill_between(monthly_sales['month'], monthly_sales['销售额'], alpha=0.3, color=COLORS['primary'])
    ax1.set_ylabel('Sales Amount (CNY)')
    ax1.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', alpha=0.7)
    for x, y in zip(monthly_sales['month'], monthly_sales['销售额']):
        ax1.text(x, y + 2000, f'¥{y:,.0f}', ha='center', fontsize=9)

    # 2. 月度订单数趋势
    ax2 = axes[0, 1]
    ax2.bar(monthly_sales['month'], monthly_sales['订单数'], color=COLORS['secondary'], alpha=0.8)
    ax2.set_ylabel('Number of Orders')
    ax2.set_title('Monthly Order Count Trend', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    for x, y in zip(monthly_sales['month'], monthly_sales['订单数']):
        ax2.text(x, y + 1, f'{y}', ha='center', fontsize=9)

    # 3. 月度平均订单金额趋势
    ax3 = axes[1, 0]
    ax3.plot(monthly_sales['month'], monthly_sales['平均订单金额'], marker='s', linewidth=2,
             markersize=8, color=COLORS['accent'])
    ax3.set_ylabel('Average Order Value (CNY)')
    ax3.set_title('Monthly Average Order Value Trend', fontsize=14, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, linestyle='--', alpha=0.7)

    # 4. 月度销量趋势
    ax4 = axes[1, 1]
    ax4.plot(monthly_sales['month'], monthly_sales['总销量'], marker='^', linewidth=2,
             markersize=8, color=COLORS['success'])
    ax4.fill_between(monthly_sales['month'], monthly_sales['总销量'], alpha=0.3, color=COLORS['success'])
    ax4.set_ylabel('Sales Volume')
    ax4.set_title('Monthly Sales Volume Trend', fontsize=14, fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

    # 显示月度销售数据
    st.subheader("月度销售详细数据")
    display_df = monthly_sales.copy()
    display_df['销售额'] = display_df['销售额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['平均订单金额'] = display_df['平均订单金额'].apply(lambda x: f"¥{x:,.2f}")
    st.dataframe(display_df, hide_index=True, use_container_width=True)


def render_category_analysis(calculator):
    """渲染产品类别分析"""
    st.title("产品类别分析")

    category_analysis = calculator.get_category_performance()

    # 创建可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 1. 各类别销售额对比
    ax1 = axes[0]
    bars1 = ax1.barh(category_analysis['category'], category_analysis['总销售额'],
                     color=COLORS['palette'][:len(category_analysis)])
    ax1.set_xlabel('Sales Amount (CNY)')
    ax1.set_title('Total Sales by Category', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()
    for bar, val in zip(bars1, category_analysis['总销售额']):
        ax1.text(val + 10000, bar.get_y() + bar.get_height()/2, f'¥{val:,.0f}', va='center', fontsize=9)

    # 2. 各类别毛利率对比
    ax2 = axes[1]
    bars2 = ax2.bar(category_analysis['category'], category_analysis['毛利率'],
                    color=COLORS['palette'][:len(category_analysis)])
    ax2.set_ylabel('Gross Margin (%)')
    ax2.set_title('Gross Margin by Category', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.axhline(y=category_analysis['毛利率'].mean(), color='r', linestyle='--',
                label=f"Avg: {category_analysis['毛利率'].mean():.1f}%")
    ax2.legend()
    for bar, val in zip(bars2, category_analysis['毛利率']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}%', ha='center', fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)

    # 显示详细数据
    st.subheader("产品类别分析详细数据")
    display_df = category_analysis.copy()
    display_df['总销售额'] = display_df['总销售额'].apply(lambda x: f"¥{x:,.2f}")
    display_df['毛利润'] = display_df['毛利润'].apply(lambda x: f"¥{x:,.2f}")
    display_df['毛利率'] = display_df['毛利率'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(display_df, hide_index=True, use_container_width=True)


def render_data_dictionary(loader):
    """渲染数据字典"""
    st.title("数据字典")

    data_dict = loader.get_data_dictionary()

    for sheet_name, fields in data_dict.items():
        st.markdown(f"### {sheet_name}")

        dict_df = pd.DataFrame({
            '字段名': list(fields.keys()),
            '说明': list(fields.values())
        })
        st.dataframe(dict_df, hide_index=True, use_container_width=True)
        st.markdown("---")


def main():
    """主函数"""
    st.set_page_config(
        page_title="销售数据分析仪表盘",
        page_icon="",
        layout="wide"
    )

    # 初始化数据
    excel_path = Path(__file__).parent.parent / 'datas' / 'sales_data.xlsx'

    try:
        loader, calculator, data = init_data(excel_path)
    except FileNotFoundError:
        st.error(f"数据文件未找到：{excel_path}")
        return
    except Exception as e:
        st.error(f"加载数据失败：{e}")
        return

    # 渲染侧边栏
    selected = render_sidebar()

    # 根据选择渲染页面
    if selected == "首页":
        render_home(loader, calculator)
    elif selected == "核心业务指标":
        render_metrics(calculator)
    elif selected == "区域销售分析":
        render_regional_analysis(calculator)
    elif selected == "产品分析":
        render_product_analysis(calculator)
    elif selected == "客户分析":
        render_customer_analysis(calculator)
    elif selected == "时间趋势分析":
        render_time_analysis(calculator)
    elif selected == "产品类别分析":
        render_category_analysis(calculator)
    elif selected == "数据字典":
        render_data_dictionary(loader)


if __name__ == "__main__":
    main()
