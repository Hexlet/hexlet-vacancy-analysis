import React, { useEffect, useState } from "react";
import { VacancyCard } from "../../../shared/ui/vacancyCard";
import { VacancyDynamicsChart } from "../../../vacancy/dynamics/ui/VacancyDynamicsChart";
import type { VacancyWithExperience } from "../../../vacancy/model/types";
import { test_vacancies } from '../testData'
import { useVacancyFilters } from "../../../vacancy/filters/model/useVacancyFilters";
import { useVacancyDynamics } from "../../../vacancy/dynamics/model/useVacancyDynamics";
import { VacancyFilters } from "../../../vacancy/filters/ui/VacancyFilters";
import { Building2 } from "lucide-react";


const experience_options = ['0-1', '2-4', '5+'];

export const RegionPage: React.FC = () => {
  const {
    selectedExperience,
    selectedRegion,
    searchQuery, 
    filteredVacancies, 
    setFilters
  } = useVacancyFilters(test_vacancies)

  const dynamicsData = useVacancyDynamics(filteredVacancies);

  const [currentPage, setCurrentPage] = useState<number>(1);
  const pageSize = 6;
  const lastPage = Math.ceil(filteredVacancies.length / pageSize);
  const safeCurrentPage = Math.min(currentPage, lastPage || 1); // Страхуемся, что номер текущей страницы не больше, чем максимально возможное число страниц
  const paginatedVacancies = filteredVacancies.slice((safeCurrentPage - 1) * pageSize, safeCurrentPage * pageSize);

  const region = selectedRegion || (paginatedVacancies.length > 0 ? paginatedVacancies[0].city : 'Регион');

  useEffect(() => {
    setCurrentPage(1);
  }, [selectedExperience, selectedRegion, searchQuery])

  // Если приспичит сделать кнопки для переключения страниц
  // const handlePageChange = (newPage: number) => {
  //   if (newPage >= 1 && newPage <= lastPage) setCurrentPage(newPage);
  // }

  const calculateGrowth = (dynamics: VacancyWithExperience['dynamics']): number => {
    if (dynamics.length < 2) return 0;
    const startValue = dynamics[0].count;
    const currentValue = dynamics[dynamics.length - 1].count;
    
    return Math.round(((currentValue - startValue) / startValue) * 100)
  }

  return (
    <div className="container bg-[#f9f9f9] mx-auto p-6">
      {/* Название региона */}
      <div className="flex items-center w-fit border border-gray-200 rounded shadow text-2xl font-bold text-[#0c2e4d] p-3 mb-4">
        <Building2 className="mr-2" color="#20B0B4"/>
        {region}
      </div>
      {/* Конец названия региона */}
      {/* Карточки с аналитикой по специальностям */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {
        paginatedVacancies.length === 0 &&
        <p>Вакансии не найдены</p>
        }
        {paginatedVacancies.map((vacancy) => {
          const growth = calculateGrowth(vacancy.dynamics);
          return (
            <div key={vacancy.id} className="border bg-white border-gray-200 rounded shadow p-4">
              <h2 className="text-sm font-semibold text-[#0c2e4d] mb-1">{vacancy.title}</h2>
              <div className="flex justify-between items-start">
                <p className="text-2xl font-bold text-[#0c2e4d] mb-2">
                  {vacancy.dynamics.reduce((acc, cur) => acc + cur.count, 0)}
                </p>
                <div className="inline-flex items-center px-2 rounded-full bg-[#20B0B4]">
                  <div className="text-white text-sm">{growth >= 0 ? '+' : '-'}{growth}%</div>
                </div>
              </div>
              <hr className="w-full h-1 border border-solid rounded-full border-[#20B0B4] bg-[#20B0B4]" />
            </div>
          )
        })}
      </div>
      {/* Конец карточек с аналитикой по специальностям */}
      {dynamicsData.length > 0 && (
        <VacancyDynamicsChart data={dynamicsData} />
      )}
      {/* Фильтры */}
      <VacancyFilters
      experience={selectedExperience}
      region={selectedRegion}
      searchQuery={searchQuery}
      regionsOptions={Array.from(new Set(test_vacancies.map((v) => v.city)))}
      experienceOptions={experience_options}
      onChangeFilters={setFilters}
      />
      {/* Конец фильтров */}
      {paginatedVacancies.map((vacancy) => (
        <VacancyCard key={vacancy.id} {...vacancy} />
      ))}
    </div>
  )
}
