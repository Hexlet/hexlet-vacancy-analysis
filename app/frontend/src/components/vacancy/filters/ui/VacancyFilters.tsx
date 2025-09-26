import React from "react";
import { ChevronDown } from "lucide-react";

interface VacancyFiltersProps {
  experience: string;
  region: string;
  searchQuery: string;
  regionsOptions: string[];
  experienceOptions: string[];
  onChangeFilters: (params: { experience?: string; region?: string; searchQuery?: string; }) => void;
}

export const VacancyFilters: React.FC<VacancyFiltersProps> = ({ experience, region, searchQuery, regionsOptions, experienceOptions, onChangeFilters }) => {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border border-gray-200 rounded shadow p-4">
      {/* Селекты */}
      <div className="flex flex-col gap-4 md:flex-row md:gap-4">
      {/* Опыт */}
        <div className="relative inline-block w-full">
          <select
            value={experience}
            onChange={(e) => {
            onChangeFilters({ experience: e.target.value });
            }}
            className="text-[#2f4664] border border-gray-200 rounded p-2 md:w-30 w-full appearance-none pr-6"
          >
          <option value="">Опыт</option>
          {experienceOptions.map((exp) => (
            <option key={exp} value={exp}>{exp === '5+' ? `${exp} лет` : `${exp} года`}</option>
          ))}
          </select>
          <div className="pointer-events-none absolute top-1/2 right-3 transform -translate-y-1/2">
            <ChevronDown color="#afb8c3" size={18}/>
          </div>
        </div>
        {/* Регион */}
        <div className="relative inline-block w-full">
          <select 
            value={region}
            onChange={(e) => {
              onChangeFilters({ region: e.target.value });
            }} 
            className="appearance-none text-[#2f4664] border border-gray-200 rounded p-2 md:w-42 w-full" 
          >
          <option value="">Регион</option>
          {regionsOptions.map((region) => (
            <option key={region} value={region}>{region}</option>
          ))}
          </select>
          <div className="pointer-events-none absolute top-1/2 right-3 transform -translate-y-1/2">
            <ChevronDown color="#afb8c3" size={18}/>
          </div>
        </div>
      </div>
      {/* Конец селектов */}
      {/* Поиск по словам */}
      <div className="flex flex-wrap w-full md:w-auto gap-4">
        <input 
          type="text" 
          placeholder="Поиск по ключевым словам..."
          value={searchQuery}
          onChange={(e) => {
            onChangeFilters({ searchQuery: e.target.value });
          }}
          className="border border-gray-200 rounded p-2 flex-grow w-full md:w-60 text-xs"
          style={{ fontSize: '14px' }}
        />
        <button className="flex items-center justify-center text-white px-4 py-1 rounded-md cursor-pointer bg-[#20B0B4] w-full md:w-auto hover:bg-[#1a8f90]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4 mr-3"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1110.5 3a7.5 7.5 0 016.15 13.65z"
          />
          </svg>
          Найти</button>
      </div>
    </div>
  )
}