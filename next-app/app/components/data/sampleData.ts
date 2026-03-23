// Monthly sales trend data
export const salesTrendData = [
  { month: 'Jan', sales: 1850000, units: 14200 },
  { month: 'Feb', sales: 1720000, units: 13100 },
  { month: 'Mar', sales: 1980000, units: 15300 },
  { month: 'Apr', sales: 1890000, units: 14500 },
  { month: 'May', sales: 2100000, units: 16200 },
  { month: 'Jun', sales: 2250000, units: 17400 },
  { month: 'Jul', sales: 2180000, units: 16800 },
  { month: 'Aug', sales: 2320000, units: 17900 },
  { month: 'Sep', sales: 2150000, units: 16500 },
  { month: 'Oct', sales: 2280000, units: 17600 },
  { month: 'Nov', sales: 2450000, units: 18900 },
  { month: 'Dec', sales: 2580000, units: 19800 },
];

// Revenue by category data
export const revenueByCategory = [
  { name: 'Electronics', value: 8500000, color: '#3B82F6' },
  { name: 'Clothing', value: 5200000, color: '#10B981' },
  { name: 'Home & Garden', value: 4100000, color: '#F59E0B' },
  { name: 'Sports', value: 2800000, color: '#EF4444' },
  { name: 'Books', value: 1300000, color: '#8B5CF6' },
];

// YoY Growth by region data
export const yoyGrowthData = [
  { region: 'North America', growth: 12.5, revenue: 9800000 },
  { region: 'Europe', growth: 8.3, revenue: 7200000 },
  { region: 'Asia Pacific', growth: 18.7, revenue: 3500000 },
  { region: 'Latin America', growth: -2.1, revenue: 900000 },
  { region: 'Middle East', growth: 5.4, revenue: 500000 },
];

// Performance metrics data
export const performanceData = [
  { month: 'Jan', revenue: 1850000, profit: 370000, orders: 12500 },
  { month: 'Feb', revenue: 1720000, profit: 344000, orders: 11600 },
  { month: 'Mar', revenue: 1980000, profit: 396000, orders: 13400 },
  { month: 'Apr', revenue: 1890000, profit: 378000, orders: 12800 },
  { month: 'May', revenue: 2100000, profit: 420000, orders: 14200 },
  { month: 'Jun', revenue: 2250000, profit: 450000, orders: 15200 },
  { month: 'Jul', revenue: 2180000, profit: 436000, orders: 14700 },
  { month: 'Aug', revenue: 2320000, profit: 464000, orders: 15700 },
  { month: 'Sep', revenue: 2150000, profit: 430000, orders: 14500 },
  { month: 'Oct', revenue: 2280000, profit: 456000, orders: 15400 },
  { month: 'Nov', revenue: 2450000, profit: 490000, orders: 16500 },
  { month: 'Dec', revenue: 2580000, profit: 516000, orders: 17400 },
];

// Filter options
export const categories = ['All Categories', 'Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books'];
export const regions = ['All Regions', 'North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'];
export const timePeriods = ['Last 30 Days', 'Last 90 Days', 'Last 6 Months', 'Last 12 Months', 'Year to Date'];

// Key metrics
export const keyMetrics = {
  totalRevenue: { value: 21900000, change: -0.8, icon: 'dollar' },
  totalSales: { value: 21700000, change: 2.3, icon: 'cart' },
  customers: { value: 101000, change: 5.1, icon: 'users' },
  unitsSold: { value: 169900, change: 3.7, icon: 'box' },
};
