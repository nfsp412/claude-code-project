'use client';

import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface RevenuePieChartProps {
  selectedCategory: string;
  selectedRegion: string;
  onCategoryClick?: (category: string) => void;
}

export default function RevenuePieChart({ selectedCategory, selectedRegion, onCategoryClick }: RevenuePieChartProps) {
  const data = [
    { name: 'Electronics', value: 8500000, color: '#3B82F6' },
    { name: 'Clothing', value: 5200000, color: '#10B981' },
    { name: 'Home & Garden', value: 4100000, color: '#F59E0B' },
    { name: 'Sports', value: 2800000, color: '#EF4444' },
    { name: 'Books', value: 1300000, color: '#8B5CF6' },
  ];

  // Apply filter effects
  const getFilteredData = () => {
    let multiplier = 1;
    if (selectedRegion !== 'All Regions') multiplier *= 0.7;

    // If a specific category is selected, highlight it
    if (selectedCategory !== 'All Categories') {
      return data
        .filter(item => item.name === selectedCategory)
        .map(item => ({ ...item, value: Math.round(item.value * multiplier) }));
    }

    return data.map(item => ({ ...item, value: Math.round(item.value * multiplier) }));
  };

  const filteredData = getFilteredData();

  const formatValue = (value: number) => {
    if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return `$${value}`;
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const percentage = ((data.value / filteredData.reduce((sum, item) => sum + item.value, 0)) * 100).toFixed(1);
      return (
        <div className="bg-white dark:bg-zinc-800 p-3 rounded-lg shadow-lg border border-zinc-200 dark:border-zinc-700">
          <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-1">{data.name}</p>
          <p className="text-sm" style={{ color: data.color }}>
            {formatValue(data.value)}
          </p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400">{percentage}% of total</p>
        </div>
      );
    }
    return null;
  };

  const handleSliceClick = (data: any) => {
    if (onCategoryClick) {
      onCategoryClick(data.payload.name);
    }
  };

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-xl p-5 shadow-sm border border-zinc-200 dark:border-zinc-800">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-4">Revenue by Category</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={filteredData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              onClick={handleSliceClick}
              style={{ cursor: 'pointer' }}
            >
              {filteredData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => (
                <span className="text-sm text-zinc-600 dark:text-zinc-400">{value}</span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
