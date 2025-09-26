import React from "react";
import { AreaChart, Area, XAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ChartColumn } from "lucide-react";

interface VacancyDynamicsChartProps {
  data: { month: string; count: number}[]
}

export const VacancyDynamicsChart: React.FC<VacancyDynamicsChartProps> = ({ data }) => {
  return (
    <div className="w-full h-64 mb-6 bg-white border border-gray-200 rounded shadow p-4">
      <div className="flex items-center mb-4">
        <ChartColumn className="h-6 w-6 text-[#20B0B4] mr-2" />
        <h2 className="text-xl font-bold text-[#0c2e4d]">Динамика вакансий</h2>
      </div>
      <div className="md:w-1/2 mx-auto h-full">
        <ResponsiveContainer width='100%' height='100%'>
          <AreaChart
            data={ data }
            margin={{ top: 10, right: 15, left: 15, bottom: 25}}    
          >
          <defs>
            <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#20B0B4" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#20B0B4" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey='month' interval={0} tick={{ fontSize: 12 }}/>
          <CartesianGrid vertical={false} strokeDasharray="" />
          <Tooltip />
          <Area type="monotone" dataKey="count" stroke="#20B0B4" fillOpacity={1} fill="url(#chartGrad)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}