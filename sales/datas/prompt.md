@test.ipynb 该notebook读取了销售数据,并进行了一些分析,销售数据都以excel的格式存储在 @datas 目录中

**重构需求**

1. notebook结构重构
    - 需要包含数据字典
    - 需要有可视化展示
2. 提升代码质量
    - 创建 data_loader.py 负责加载和处理数据
    - 创建 business_calc.py 负责计算相关指标
3. 可视化展示
    - 增强可视化展示的效果