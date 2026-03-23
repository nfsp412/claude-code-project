'use client';

import React from 'react';

interface MetricCardProps {
  title: string;
  value: string;
  change: number;
  icon: React.ReactNode;
}

function MetricCard({ title, value, change, icon }: MetricCardProps) {
  const isPositive = change >= 0;
  return (
    <div className="flex flex-col gap-3 p-5 bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">{title}</span>
        <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-blue-600 dark:text-blue-400">
          {icon}
        </div>
      </div>
      <div className="flex items-end justify-between">
        <span className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">{value}</span>
        <span
          className={`flex items-center text-sm font-medium ${
            isPositive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
          }`}
        >
          {isPositive ? '↑' : '↓'} {Math.abs(change).toFixed(1)}%
        </span>
      </div>
    </div>
  );
}

interface MetricsCardsProps {
  selectedCategory: string;
  selectedRegion: string;
}

export default function MetricsCards({ selectedCategory, selectedRegion }: MetricsCardsProps) {
  // Format numbers for display
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    }).format(value / 1000000) + 'M';
  };

  const formatNumber = (value: number) => {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    }
    if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K';
    }
    return value.toString();
  };

  // Apply filters to metrics (simplified - in real app would filter actual data)
  const getFilteredMetrics = () => {
    let multiplier = 1;

    // Apply category filter effect
    if (selectedCategory !== 'All Categories') {
      multiplier *= 0.6;
    }

    // Apply region filter effect
    if (selectedRegion !== 'All Regions') {
      multiplier *= 0.7;
    }

    return {
      revenue: 21900000 * multiplier,
      sales: 21700000 * multiplier,
      customers: 101000 * multiplier,
      unitsSold: 169900 * multiplier,
    };
  };

  const metrics = getFilteredMetrics();

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <MetricCard
        title="Total Revenue"
        value={formatCurrency(metrics.revenue)}
        change={-0.8}
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        }
      />
      <MetricCard
        title="Total Sales"
        value={formatCurrency(metrics.sales)}
        change={2.3}
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        }
      />
      <MetricCard
        title="Customers"
        value={formatNumber(metrics.customers)}
        change={5.1}
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        }
      />
      <MetricCard
        title="Units Sold"
        value={formatNumber(metrics.unitsSold)}
        change={3.7}
        icon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        }
      />
    </div>
  );
}
