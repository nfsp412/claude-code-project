# 销售分析模块

销售数据分析模块，提供数据加载、业务指标计算和可视化分析功能。

## 目录结构

```
sales_analysis/
├── __init__.py           # 模块初始化文件
├── data_loader.py        # 数据加载模块
├── business_calc.py      # 业务计算模块
├── sales_analysis.ipynb  # 分析笔记本
└── README.md             # 本文档
```

## 安装依赖

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## 快速开始

```python
from sales_analysis.data_loader import SalesDataLoader
from sales_analysis.business_calc import SalesMetricsCalculator

# 加载数据
loader = SalesDataLoader('datas/sales_data.xlsx')
data = loader.load_all()

# 计算核心指标
calculator = SalesMetricsCalculator(
    orders=data['orders'],
    products=data['products'],
    customers=data['customers'],
    targets=data['targets']
)
metrics = calculator.get_summary_metrics()
```

## 模块说明

### 1. data_loader.py - 数据加载模块

**SalesDataLoader 类**：统一的数据加载接口

#### 主要方法

| 方法 | 说明 |
|------|------|
| `load_orders()` | 加载订单数据 |
| `load_products()` | 加载产品数据 |
| `load_customers()` | 加载客户数据 |
| `load_targets()` | 加载销售目标数据 |
| `load_all()` | 一次性加载所有数据 |
| `get_data_dictionary()` | 获取数据字典（字段说明） |
| `get_data_info()` | 获取数据集基本信息 |

#### 数据字典

**订单明细表**
| 字段 | 说明 |
|------|------|
| order_id | 订单 ID，唯一标识每个订单 |
| order_date | 订单日期 |
| customer_id | 客户 ID |
| product_id | 产品 ID |
| quantity | 购买数量 |
| unit_price | 商品单价 |
| total_amount | 最终金额 |
| region | 销售区域 |

**产品信息表**
| 字段 | 说明 |
|------|------|
| product_id | 产品 ID |
| product_name | 产品名称 |
| category | 产品类别 |
| cost_price | 成本价格 |
| sell_price | 销售价格 |

**客户信息表**
| 字段 | 说明 |
|------|------|
| customer_id | 客户 ID |
| customer_name | 客户姓名 |
| city | 所在城市 |
| customer_type | 客户类型（企业/个人） |

#### 使用示例

```python
# 使用上下文管理器
with SalesDataLoader('datas/sales_data.xlsx') as loader:
    print(loader.available_sheets)  # 查看可用工作表
    info = loader.get_data_info()   # 获取数据概览
    data = loader.load_all()        # 加载所有数据
```

### 2. business_calc.py - 业务计算模块

**SalesMetricsCalculator 类**：计算各种业务指标

#### 主要方法

| 方法 | 说明 |
|------|------|
| `get_summary_metrics()` | 获取核心 KPI 汇总 |
| `get_regional_sales()` | 按区域统计销售额 |
| `get_product_sales()` | 按产品统计销量 |
| `get_customer_type_analysis()` | 客户类型分析 |
| `get_monthly_trend()` | 月度销售趋势 |
| `get_daily_trend()` | 每日销售趋势 |
| `get_category_performance()` | 产品类别表现 |
| `get_target_achievement()` | 销售目标达成率 |
| `get_region_product_matrix()` | 区域 - 产品销售矩阵 |

#### 使用示例

```python
calculator = SalesMetricsCalculator(
    orders=data['orders'],
    products=data['products'],
    customers=data['customers'],
    targets=data['targets']
)

# 获取核心指标
metrics = calculator.get_summary_metrics()
print(f"总销售额：¥{metrics['总销售额']:,.2f}")
print(f"毛利率：{metrics['整体毛利率']:.2f}%")

# 区域分析
region_sales = calculator.get_regional_sales()

# 产品 TOP10
top_products = calculator.get_product_sales(top_n=10)

# 月度趋势
monthly = calculator.get_monthly_trend()
```

## 核心业务指标说明

调用 `get_summary_metrics()` 返回的指标：

| 指标 | 说明 |
|------|------|
| 总销售额 | 所有订单的总销售额 |
| 总订单数 | 订单总数 |
| 活跃客户数 | 有购买记录的客户数 |
| 销售产品数 | 被购买的产品种类数 |
| 毛利润 | 总销售额 - 总成本 |
| 整体毛利率 | 毛利润 / 总销售额 |
| 平均订单金额 | 总销售额 / 总订单数 |
| 客单价 | 总销售额 / 活跃客户数 |

## Notebook 使用说明

运行 `sales_analysis.ipynb`  notebook 将自动生成完整的分析报告，包含：

- 数据字典展示
- 核心业务指标概览
- 区域销售分析（柱状图、饼图）
- 产品销售分析（TOP10、散点图）
- 客户类型分析
- 时间趋势分析
- 产品类别分析

## 扩展开发

### 添加新的业务指标

在 `business_calc.py` 中添加新方法：

```python
def get_new_metric(self) -> pd.DataFrame:
    """计算新指标"""
    # 实现逻辑
    return result
```

### 添加新的数据源

在 `data_loader.py` 中添加新的加载方法：

```python
def load_new_data(self) -> pd.DataFrame:
    """加载新数据表"""
    if self._new_data is None:
        self._new_data = pd.read_excel(
            self.excel_file,
            sheet_name='新工作表名'
        )
    return self._new_data
```
