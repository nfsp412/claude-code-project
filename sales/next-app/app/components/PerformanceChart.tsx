'use client';

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts';

interface PerformanceChartProps {
  selectedCategory: string;
  selectedRegion: string;
}

export default function PerformanceChart({ selectedCategory, selectedRegion }: PerformanceChartProps) {
  const data = [
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

  // Apply filter effects
  const getFilteredData = () => {
    let multiplier = 1;
    if (selectedCategory !== 'All Categories') multiplier *= 0.6;
    if (selectedRegion !== 'All Regions') multiplier *= 0.7;

    return data.map(item => ({
      ...item,
      revenue: Math.round(item.revenue * multiplier),
      profit: Math.round(item.profit * multiplier),
      orders: Math.round(item.orders * multiplier),
    }));
  };

  const filteredData = getFilteredData();

  const formatYAxis = (value: number) => {
    if (value >= 1000000) return `$${(value / 1000000).toFixed(0)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return `$${value}`;
  };

  const formatOrdersYAxis = (value: number) => {
    if (value >= 10000) return `${(value / 1000).toFixed(0)}K`;
    return `${value}`;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-zinc-800 p-3 rounded-lg shadow-lg border border-zinc-200 dark:border-zinc-700">
          <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-2">{label}</p>
          {payload.map((item: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: item.color }}>
              {item.name}: {item.name === 'Orders' ? item.value : `$${new Intl.NumberFormat('en-US').format(item.value)}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-xl p-5 shadow-sm border border-zinc-200 dark:border-zinc-800">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-4">Performance Metrics</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={filteredData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" />
            <XAxis
              dataKey="month"
              stroke="#71717a"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              yAxisId="left"
              stroke="#71717a"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={formatYAxis}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#71717a"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={formatOrdersYAxis}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="revenue"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={false}
            />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="profit"
              stroke="#10B981"
              strokeWidth={2}
              dot={false}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="orders"
              stroke="#F59E0B"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
