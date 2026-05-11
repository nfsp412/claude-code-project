'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface YoYGrowthChartProps {
  selectedCategory: string;
  selectedRegion: string;
  onRegionClick?: (region: string) => void;
}

export default function YoYGrowthChart({ selectedCategory, selectedRegion, onRegionClick }: YoYGrowthChartProps) {
  const data = [
    { region: 'N. America', growth: 12.5, revenue: 9800000, color: '#3B82F6' },
    { region: 'Europe', growth: 8.3, revenue: 7200000, color: '#10B981' },
    { region: 'Asia Pac', growth: 18.7, revenue: 3500000, color: '#F59E0B' },
    { region: 'LatAm', growth: -2.1, revenue: 900000, color: '#EF4444' },
    { region: 'M. East', growth: 5.4, revenue: 500000, color: '#8B5CF6' },
  ];

  // Apply filter effects
  const getFilteredData = () => {
    let multiplier = 1;
    if (selectedCategory !== 'All Categories') multiplier *= 0.6;
    if (selectedRegion !== 'All Regions') {
      return data.filter(item =>
        selectedRegion === 'All Regions' || item.region.includes(selectedRegion.split(' ')[0])
      );
    }
    return data.map(item => ({ ...item, revenue: Math.round(item.revenue * multiplier) }));
  };

  const filteredData = getFilteredData();

  const formatYAxis = (value: number) => {
    if (value >= 0) return `+${value}%`;
    return `${value}%`;
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-zinc-800 p-3 rounded-lg shadow-lg border border-zinc-200 dark:border-zinc-700">
          <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-1">{data.region}</p>
          <p className="text-sm" style={{ color: data.growth >= 0 ? '#10b981' : '#ef4444' }}>
            Growth: {data.growth >= 0 ? '+' : ''}{data.growth}%
          </p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400">
            Revenue: ${new Intl.NumberFormat('en-US', { notation: 'compact' }).format(data.revenue)}
          </p>
        </div>
      );
    }
    return null;
  };

  const handleBarClick = (data: any) => {
    if (onRegionClick) {
      const fullRegionName = data.payload.region.replace('N. America', 'North America')
        .replace('Europe', 'Europe')
        .replace('Asia Pac', 'Asia Pacific')
        .replace('LatAm', 'Latin America')
        .replace('M. East', 'Middle East');
      onRegionClick(fullRegionName);
    }
  };

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-xl p-5 shadow-sm border border-zinc-200 dark:border-zinc-800">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-4">YoY Growth by Region</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={filteredData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" />
            <XAxis
              dataKey="region"
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
            <Bar dataKey="growth" onClick={handleBarClick} style={{ cursor: 'pointer' }}>
              {filteredData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.growth >= 0 ? entry.color : '#ef4444'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
