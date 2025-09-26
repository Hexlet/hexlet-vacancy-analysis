import type { VacancyWithExperience } from "../../../vacancy/model/types";

export interface RegionPageProps {
  region: string;
  vacancies: VacancyWithExperience[];
  experienceOptions: string[];
  countryRegions: string[];
  filters: {
    experience: string;
    region: string;
    query: string;
  };
  pagination: {
    currentPage: number;
    lastPage: number;
    nextPageUrl: string | null;
    prevPageUrl: string | null;
  }
}