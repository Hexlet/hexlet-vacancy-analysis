export interface VacancyProps {
  title: string;
  description: string;
  company: string;
  salary: string;
  city: string;
  id: number;
  key_skills: string[];
}

export interface VacancyWithDynamics extends VacancyProps {
  dynamics: {
    count: number;
    month: string;
    year: number;
  }[];
}

export interface VacancyWithExperience extends VacancyWithDynamics {
  minExperience: number;
}