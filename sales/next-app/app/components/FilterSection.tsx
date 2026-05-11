'use client';

import React from 'react';

interface FilterSectionProps {
  selectedCategory: string;
  selectedRegion: string;
  selectedTimePeriod: string;
  onCategoryChange: (category: string) => void;
  onRegionChange: (region: string) => void;
  onTimePeriodChange: (period: string) => void;
}

const categories = ['All Categories', 'Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books'];
const regions = ['All Regions', 'North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'];
const timePeriods = ['Last 30 Days', 'Last 90 Days', 'Last 6 Months', 'Last 12 Months', 'Year to Date'];

export default function FilterSection({
  selectedCategory,
  selectedRegion,
  selectedTimePeriod,
  onCategoryChange,
  onRegionChange,
  onTimePeriodChange,
}: FilterSectionProps) {
  return (
    <div className="flex flex-wrap gap-4 mb-6 p-4 bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800">
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-zinc-600 dark:text-zinc-400">Category</label>
        <select
          value={selectedCategory}
          onChange={(e) => onCategoryChange(e.target.value)}
          className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-sm font-medium text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer hover:bg-zinc-100 dark:hover:bg-zinc-750"
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-zinc-600 dark:text-zinc-400">Region</label>
        <select
          value={selectedRegion}
          onChange={(e) => onRegionChange(e.target.value)}
          className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-sm font-medium text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer hover:bg-zinc-100 dark:hover:bg-zinc-750"
        >
          {regions.map((region) => (
            <option key={region} value={region}>
              {region}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-zinc-600 dark:text-zinc-400">Time Period</label>
        <select
          value={selectedTimePeriod}
          onChange={(e) => onTimePeriodChange(e.target.value)}
          className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-sm font-medium text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer hover:bg-zinc-100 dark:hover:bg-zinc-750"
        >
          {timePeriods.map((period) => (
            <option key={period} value={period}>
              {period}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
