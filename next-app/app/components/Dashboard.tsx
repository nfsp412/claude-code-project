'use client';

import React, { useState, useCallback } from 'react';
import FilterSection from './FilterSection';
import MetricsCards from './MetricsCards';
import SalesTrendChart from './SalesTrendChart';
import RevenuePieChart from './RevenuePieChart';
import YoYGrowthChart from './YoYGrowthChart';
import PerformanceChart from './PerformanceChart';

export default function Dashboard() {
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const [selectedRegion, setSelectedRegion] = useState('All Regions');
  const [selectedTimePeriod, setSelectedTimePeriod] = useState('Last 12 Months');

  const handleCategoryChange = useCallback((category: string) => {
    setSelectedCategory(category);
  }, []);

  const handleRegionChange = useCallback((region: string) => {
    setSelectedRegion(region);
  }, []);

  const handleTimePeriodChange = useCallback((period: string) => {
    setSelectedTimePeriod(period);
  }, []);

  const handleCategoryClick = useCallback((category: string) => {
    setSelectedCategory(category);
  }, []);

  const handleRegionClick = useCallback((region: string) => {
    setSelectedRegion(region);
  }, []);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            Analytics Dashboard
          </h1>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            Interactive sales and revenue analysis with cross-filtering
          </p>
        </div>

        {/* Filters */}
        <FilterSection
          selectedCategory={selectedCategory}
          selectedRegion={selectedRegion}
          selectedTimePeriod={selectedTimePeriod}
          onCategoryChange={handleCategoryChange}
          onRegionChange={handleRegionChange}
          onTimePeriodChange={handleTimePeriodChange}
        />

        {/* Metrics Cards */}
        <MetricsCards
          selectedCategory={selectedCategory}
          selectedRegion={selectedRegion}
        />

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Sales Trend Chart */}
          <SalesTrendChart
            selectedCategory={selectedCategory}
            selectedRegion={selectedRegion}
            onCategoryClick={handleCategoryClick}
          />

          {/* Revenue Pie Chart */}
          <RevenuePieChart
            selectedCategory={selectedCategory}
            selectedRegion={selectedRegion}
            onCategoryClick={handleCategoryClick}
          />

          {/* YoY Growth Chart */}
          <YoYGrowthChart
            selectedCategory={selectedCategory}
            selectedRegion={selectedRegion}
            onRegionClick={handleRegionClick}
          />

          {/* Performance Chart */}
          <PerformanceChart
            selectedCategory={selectedCategory}
            selectedRegion={selectedRegion}
          />
        </div>

        {/* Footer info */}
        <div className="mt-6 text-center text-xs text-zinc-400 dark:text-zinc-500">
          <p>Click on chart elements to cross-filter data across all visualizations</p>
        </div>
      </div>
    </div>
  );
}
