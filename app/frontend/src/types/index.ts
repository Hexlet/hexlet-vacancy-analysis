export interface User {
    name: string;
    fullName: string;
    avatarUrl: string;
    email: string;
}

export interface VacancyCardProps {
  id: string;
  title: string;
  url?: string;
  salary: string;
  experience?: string;
  employment?: string;
  company?: string;
  city?: string;
  skills?: string;
  address?: string;
}
