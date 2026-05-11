'use client';

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface SalesTrendChartProps {
  selectedCategory: string;
  selectedRegion: string;
  onCategoryClick?: (category: string) => void;
}

export default function SalesTrendChart({ selectedCategory, selectedRegion, onCategoryClick }: SalesTrendChartProps) {
  const data = [
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

  // Apply filter effects
  const getFilteredData = () => {
    let multiplier = 1;
    if (selectedCategory !== 'All Categories') multiplier *= 0.6;
    if (selectedRegion !== 'All Regions') multiplier *= 0.7;

    return data.map(item => ({
      ...item,
      sales: Math.round(item.sales * multiplier),
      units: Math.round(item.units * multiplier),
    }));
  };

  const filteredData = getFilteredData();

  const formatYAxis = (value: number) => {
    if (value >= 1000000) return `$${(value / 1000000).toFixed(0)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return `$${value}`;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-zinc-800 p-3 rounded-lg shadow-lg border border-zinc-200 dark:border-zinc-700">
          <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-1">{label}</p>
          <p className="text-sm text-blue-600 dark:text-blue-400">
            Sales: ${new Intl.NumberFormat('en-US').format(payload[0].value)}
          </p>
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            Units: {new Intl.NumberFormat('en-US').format(payload[0].payload.units)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-xl p-5 shadow-sm border border-zinc-200 dark:border-zinc-800">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-4">Sales Trend</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={filteredData}>
            <defs>
              <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" />
            <XAxis
              dataKey="month"
              stroke="#71717a"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#71717a"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={formatYAxis}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="sales"
              stroke="#3B82F6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorSales)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
