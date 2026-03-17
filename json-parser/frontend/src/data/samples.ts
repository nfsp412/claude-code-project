export const jsonSamples = {
  simple: {
    name: '简单对象',
    data: `{
  "name": "张三",
  "age": 28,
  "city": "北京",
  "isStudent": false
}`
  },
  complex: {
    name: '复杂嵌套',
    data: `{
  "users": [
    {
      "id": 1,
      "name": "Alice",
      "profile": {
        "email": "alice@example.com",
        "phone": "+86 138-0000-0001",
        "address": {
          "street": "中关村大街",
          "city": "北京",
          "zip": "100086"
        }
      },
      "tags": ["developer", "frontend"]
    },
    {
      "id": 2,
      "name": "Bob",
      "profile": {
        "email": "bob@example.com",
        "phone": "+86 138-0000-0002",
        "address": {
          "street": "科技路",
          "city": "上海",
          "zip": "200000"
        }
      },
      "tags": ["designer", "ui"]
    }
  ],
  "total": 2,
  "success": true
}`
  },
  api: {
    name: 'API 响应',
    data: `{
  "code": 200,
  "message": "success",
  "data": {
    "userId": 10001,
    "userName": "admin",
    "roles": ["admin", "user"],
    "permissions": [
      "read",
      "write",
      "delete"
    ],
    "lastLogin": "2026-03-02T10:30:00Z",
    "settings": {
      "theme": "dark",
      "language": "zh-CN",
      "notifications": true
    }
  },
  "timestamp": 1709393400000
}`
  },
  product: {
    name: '商品数据',
    data: `{
  "product": {
    "id": "PRD-2026-001",
    "name": "智能手表 Pro",
    "price": 1999.00,
    "currency": "CNY",
    "stock": 150,
    "categories": ["电子产品", "可穿戴设备"],
    "features": [
      "心率监测",
      "睡眠追踪",
      "防水 50米",
      "续航 7天"
    ],
    "specs": {
      "display": "1.5英寸 OLED",
      "battery": "450mAh",
      "weight": "45g"
    },
    "images": [
      "https://example.com/img1.jpg",
      "https://example.com/img2.jpg"
    ],
    "reviews": {
      "count": 328,
      "rating": 4.8
    }
  }
}`
  }
};
