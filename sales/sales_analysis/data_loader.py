"""
数据加载模块

负责加载和处理 Excel 中的销售数据，提供统一的数据访问接口。
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional


class SalesDataLoader:
    """销售数据加载器

    从 Excel 文件中加载销售相关数据，包括订单、产品、客户和销售目标。
    """

    # 数据字典 - 描述各字段含义
    DATA_DICTIONARY = {
        '订单明细': {
            'order_id': '订单 ID，唯一标识每个订单',
            'order_date': '订单日期，格式为 YYYY-MM-DD',
            'customer_id': '客户 ID，关联客户信息表',
            'product_id': '产品 ID，关联产品信息表',
            'quantity': '购买数量',
            'unit_price': '商品单价（元）',
            'subtotal': '小计金额 = quantity * unit_price',
            'discount_rate': '折扣率，0-1 之间的小数',
            'discount_amount': '折扣金额 = subtotal * discount_rate',
            'total_amount': '最终金额 = subtotal - discount_amount',
            'region': '销售区域：华东/华南/华北/华中/西北/西南'
        },
        '产品信息': {
            'product_id': '产品 ID，唯一标识每个产品',
            'product_name': '产品名称',
            'category': '产品类别',
            'cost_price': '成本价格（元）',
            'sell_price': '销售价格（元）'
        },
        '客户信息': {
            'customer_id': '客户 ID，唯一标识每个客户',
            'customer_name': '客户姓名',
            'city': '所在城市',
            'customer_type': '客户类型：企业客户/个人客户'
        },
        '销售目标': {
            'salesperson_id': '销售人员 ID',
            'salesperson_name': '销售人员姓名',
            'target_jan': '1 月销售目标（元）',
            'target_feb': '2 月销售目标（元）',
            'target_mar': '3 月销售目标（元）',
            'target_apr': '4 月销售目标（元）',
            'target_may': '5 月销售目标（元）',
            'target_jun': '6 月销售目标（元）'
        }
    }

    def __init__(self, excel_path: str):
        """初始化数据加载器

        Args:
            excel_path: Excel 文件路径
        """
        self.excel_path = Path(excel_path)
        self._excel_file: Optional[pd.ExcelFile] = None
        self._orders: Optional[pd.DataFrame] = None
        self._products: Optional[pd.DataFrame] = None
        self._customers: Optional[pd.DataFrame] = None
        self._targets: Optional[pd.DataFrame] = None

    @property
    def excel_file(self) -> pd.ExcelFile:
        """获取 Excel 文件对象（惰性加载）"""
        if self._excel_file is None:
            self._excel_file = pd.ExcelFile(self.excel_path)
        return self._excel_file

    @property
    def available_sheets(self) -> list:
        """获取可用的工作表列表"""
        return self.excel_file.sheet_names

    def load_orders(self) -> pd.DataFrame:
        """加载订单数据"""
        if self._orders is None:
            self._orders = pd.read_excel(self.excel_file, sheet_name='订单明细')
            self._orders['order_date'] = pd.to_datetime(self._orders['order_date'])
        return self._orders

    def load_products(self) -> pd.DataFrame:
        """加载产品数据"""
        if self._products is None:
            self._products = pd.read_excel(self.excel_file, sheet_name='产品信息')
        return self._products

    def load_customers(self) -> pd.DataFrame:
        """加载客户数据"""
        if self._customers is None:
            self._customers = pd.read_excel(self.excel_file, sheet_name='客户信息')
        return self._customers

    def load_targets(self) -> pd.DataFrame:
        """加载销售目标数据"""
        if self._targets is None:
            self._targets = pd.read_excel(self.excel_file, sheet_name='销售目标')
        return self._targets

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """加载所有数据表

        Returns:
            包含所有数据表的字典
        """
        return {
            'orders': self.load_orders(),
            'products': self.load_products(),
            'customers': self.load_customers(),
            'targets': self.load_targets()
        }

    def get_data_dictionary(self, sheet_name: Optional[str] = None) -> Dict:
        """获取数据字典

        Args:
            sheet_name: 可选，指定返回特定工作表的数据字典

        Returns:
            数据字典，包含字段说明
        """
        if sheet_name:
            return self.DATA_DICTIONARY.get(sheet_name, {})
        return self.DATA_DICTIONARY

    def get_data_info(self) -> Dict:
        """获取数据集基本信息

        Returns:
            包含数据规模、时间范围等信息的字典
        """
        orders = self.load_orders()
        return {
            '订单总数': len(orders),
            '唯一客户数': orders['customer_id'].nunique(),
            '唯一产品数': orders['product_id'].nunique(),
            '数据时间范围': f"{orders['order_date'].min().strftime('%Y-%m-%d')} 至 {orders['order_date'].max().strftime('%Y-%m-%d')}",
            '销售区域数': orders['region'].nunique(),
            '总销售额': f"¥{orders['total_amount'].sum():,.2f}"
        }

    def close(self):
        """关闭 Excel 文件"""
        if self._excel_file:
            self._excel_file.close()
            self._excel_file = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
