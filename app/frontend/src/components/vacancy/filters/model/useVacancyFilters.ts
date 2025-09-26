import { useState, useMemo } from "react";
import type { VacancyWithExperience } from "../../model/types";

const experienceRange: Record<string, [number, number]> = {
  '0-1': [0, 1],
  '2-4': [2, 4],
  '5+': [5, Infinity],
}

export function useVacancyFilters(vacancies: VacancyWithExperience[]) {
  const [selectedExperience, setSelectedExperience] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredVacancies = useMemo(() => {
      return vacancies.filter((vacancy) => {
        /**
         * Функция фильтра для вакансии 
         * 
         * @param {VacancyWithExperience} vacancy - Объект вакансии
         * @param {Record<string, [number, number]>} experienceRange - это словарь, в котором ключи - строки, а значения - кортежи с двумя числами
         * @param {string} selectedExperience - это строка, которую пользователь выбрал с селекте
         * @returns {boolean} true, если опыт вакансии входит в выбранный диапазон или фильтр не выбран
        */
        const experienceMatch = selectedExperience ? (() => {
          const range = experienceRange[selectedExperience];
          if (!range) return true; // Если не выбран диапазон, то проверку проходят все вакансии и показываются
          const [min, max] = range;
          return vacancy.minExperience >= min && vacancy.minExperience <= max;
        })() : true
  
        const regionMatch = selectedRegion ? vacancy.city === selectedRegion : true; 
  
        const queryMatch = searchQuery 
          ? vacancy.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            vacancy.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            vacancy.key_skills.some((skill) => skill.toLowerCase().includes(searchQuery.toLowerCase()))
          : true; // Если нет ни одного совпадения, то не фильтрует по словам, а просто показывает результат
  
          return experienceMatch && regionMatch && queryMatch;
      })
    }, [vacancies, selectedExperience, selectedRegion, searchQuery]);

  function setFilters(params: { experience?: string; region?: string; query?: string; }) {
    if (params.experience !== undefined) setSelectedExperience(params.experience);
    if (params.region !== undefined) setSelectedRegion(params.region);
    if (params.query !== undefined) setSearchQuery(params.query);
  }

  return {
    selectedExperience,
    selectedRegion,
    searchQuery, 
    filteredVacancies, 
    setFilters
  };
}