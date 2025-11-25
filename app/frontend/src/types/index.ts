export interface User {
    name: string;
    fullName: string;
    avatarUrl: string;
    email: string;
}

export interface VacancyCardProps {
  id: number;
  title: string;
  url?: string;
  salary: string;
  experience?: string;
  employment?: string;
  company?: {
    id: number;
    name: string;
  };
  city?: {
    id: number;
    name: string;
  };
  skills: string[];
}
