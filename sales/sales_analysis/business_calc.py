"""
业务计算模块

负责计算销售相关的业务指标和 KPI。
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple


class SalesMetricsCalculator:
    """销售指标计算器

    基于订单、产品、客户数据计算各种业务指标。
    """

    def __init__(self, orders: pd.DataFrame, products: pd.DataFrame,
                 customers: pd.DataFrame, targets: Optional[pd.DataFrame] = None):
        """初始化计算器

        Args:
            orders: 订单数据
            products: 产品数据
            customers: 客户数据
            targets: 可选，销售目标数据
        """
        self.orders = orders.copy()
        self.products = products.copy()
        self.customers = customers.copy()
        self.targets = targets.copy() if targets is not None else None

    def get_regional_sales(self, ascending: bool = False) -> pd.DataFrame:
        """按区域统计销售额

        Args:
            ascending: 是否按升序排列

        Returns:
            包含区域、销售额、占比的 DataFrame
        """
        region_sales = self.orders.groupby('region')['total_amount'].agg(['sum', 'count', 'mean'])
        region_sales.columns = ['总销售额', '订单数', '平均订单金额']
        region_sales = region_sales.sort_values('总销售额', ascending=ascending)

        total = region_sales['总销售额'].sum()
        region_sales['销售占比'] = (region_sales['总销售额'] / total * 100).round(2)

        return region_sales.reset_index()

    def get_product_sales(self, top_n: Optional[int] = None) -> pd.DataFrame:
        """按产品统计销量和销售额

        Args:
            top_n: 可选，只返回前 N 个产品

        Returns:
            包含产品销量、销售额的 DataFrame
        """
        product_stats = self.orders.groupby('product_id').agg({
            'quantity': 'sum',
            'total_amount': ['sum', 'mean'],
            'order_id': 'count'
        })
        product_stats.columns = ['总销量', '总销售额', '平均订单金额', '订单数']

        # 合并产品信息
        result = product_stats.merge(
            self.products[['product_id', 'product_name', 'category']],
            on='product_id',
            how='left'
        )

        # 计算毛利率
        result = result.merge(
            self.products[['product_id', 'cost_price', 'sell_price']],
            on='product_id',
            how='left',
            suffixes=('', '_ref')
        )
        result['毛利率'] = ((result['sell_price'] - result['cost_price']) / result['sell_price'] * 100).round(2)

        result = result.sort_values('总销售额', ascending=False)

        if top_n:
            result = result.head(top_n)

        return result.reset_index(drop=True)

    def get_customer_type_analysis(self) -> pd.DataFrame:
        """按客户类型分析销售情况

        Returns:
            包含客户类型分析的 DataFrame
        """
        merged = self.orders.merge(
            self.customers[['customer_id', 'customer_type']],
            on='customer_id'
        )

        analysis = merged.groupby('customer_type')['total_amount'].agg([
            'sum', 'mean', 'count', 'std'
        ])
        analysis.columns = ['总销售额', '平均订单金额', '订单数', '标准差']
        analysis['销售占比'] = (analysis['总销售额'] / analysis['总销售额'].sum() * 100).round(2)

        return analysis.reset_index()

    def get_monthly_trend(self) -> pd.DataFrame:
        """计算月度销售趋势

        Returns:
            包含月度销售数据的 DataFrame
        """
        orders_copy = self.orders.copy()
        orders_copy['month'] = orders_copy['order_date'].dt.strftime('%Y-%m')

        monthly = orders_copy.groupby('month').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        })
        monthly.columns = ['销售额', '平均订单金额', '订单数', '总销量']

        return monthly.reset_index()

    def get_daily_trend(self, month: Optional[str] = None) -> pd.DataFrame:
        """计算每日销售趋势

        Args:
            month: 可选，指定月份 (格式：YYYY-MM)

        Returns:
            包含每日销售数据的 DataFrame
        """
        orders_copy = self.orders.copy()
        orders_copy['date'] = orders_copy['order_date'].dt.strftime('%Y-%m-%d')

        if month:
            orders_copy = orders_copy[orders_copy['date'].str.startswith(month)]

        daily = orders_copy.groupby('date').agg({
            'total_amount': ['sum', 'mean'],
            'quantity': 'sum',
            'order_id': 'count'
        })
        daily.columns = ['销售额', '平均订单金额', '销量', '订单数']

        return daily.reset_index()

    def get_category_performance(self) -> pd.DataFrame:
        """分析产品类别表现

        Returns:
            包含类别表现的 DataFrame
        """
        merged = self.orders.merge(
            self.products[['product_id', 'category', 'cost_price']],
            on='product_id'
        )

        category_stats = merged.groupby('category').agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'order_id': 'count'
        })
        category_stats.columns = ['总销量', '总销售额', '订单数']

        # 计算利润
        merged['profit'] = merged['total_amount'] - (merged['quantity'] * merged['cost_price'])
        profit_by_category = merged.groupby('category')['profit'].sum()

        category_stats = category_stats.merge(profit_by_category, left_index=True, right_index=True)
        category_stats.columns = ['总销量', '总销售额', '订单数', '毛利润']
        category_stats['毛利率'] = (category_stats['毛利润'] / category_stats['总销售额'] * 100).round(2)

        return category_stats.sort_values('总销售额', ascending=False).reset_index()

    def get_target_achievement(self, actual_sales: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """计算销售目标达成率

        Args:
            actual_sales: 可选，实际销售数据（按月统计）

        Returns:
            包含目标达成情况的 DataFrame
        """
        if self.targets is None:
            raise ValueError("未提供销售目标数据")

        # 计算月实际销售额
        if actual_sales is None:
            actual_sales = self.orders.copy()
            actual_sales['month'] = actual_sales['order_date'].dt.strftime('%Y-%m')
            monthly_actual = actual_sales.groupby('month')['total_amount'].sum()
        else:
            monthly_actual = actual_sales

        # 转换目标数据格式
        targets_melted = self.targets.melt(
            id_vars=['salesperson_id', 'salesperson_name'],
            value_vars=['target_jan', 'target_feb', 'target_mar',
                       'target_apr', 'target_may', 'target_jun'],
            var_name='month_name',
            value_name='target'
        )

        month_map = {
            'target_jan': '2025-01', 'target_feb': '2025-02',
            'target_mar': '2025-03', 'target_apr': '2025-04',
            'target_may': '2025-05', 'target_jun': '2025-06'
        }
        targets_melted['month'] = targets_melted['month_name'].map(month_map)

        # 计算总目标
        total_target = targets_melted.groupby('salesperson_id')['target'].sum()
        total_actual = self.orders.groupby('customer_id')['total_amount'].sum()  # 简化处理

        result = self.targets.copy()
        result['总目标'] = result[['target_jan', 'target_feb', 'target_mar',
                                   'target_apr', 'target_may', 'target_jun']].sum(axis=1)

        return result

    def get_summary_metrics(self) -> dict:
        """获取核心业务指标汇总

        Returns:
            包含核心指标的字典
        """
        total_revenue = self.orders['total_amount'].sum()
        total_orders = len(self.orders)
        total_customers = self.orders['customer_id'].nunique()
        total_products = self.orders['product_id'].nunique()

        # 计算利润
        merged = self.orders.merge(
            self.products[['product_id', 'cost_price']],
            on='product_id'
        )
        total_cost = (merged['quantity'] * merged['cost_price']).sum()
        total_profit = total_revenue - total_cost

        return {
            '总销售额': total_revenue,
            '总订单数': total_orders,
            '活跃客户数': total_customers,
            '销售产品数': total_products,
            '总成本': total_cost,
            '毛利润': total_profit,
            '整体毛利率': (total_profit / total_revenue * 100) if total_revenue > 0 else 0,
            '平均订单金额': total_revenue / total_orders if total_orders > 0 else 0,
            '客单价': total_revenue / total_customers if total_customers > 0 else 0
        }

    def get_region_product_matrix(self) -> pd.DataFrame:
        """获取区域 - 产品销售矩阵

        Returns:
            区域 x 产品的销售矩阵
        """
        matrix = self.orders.pivot_table(
            index='region',
            columns='product_id',
            values='total_amount',
            aggfunc='sum',
            fill_value=0
        )
        return matrix
