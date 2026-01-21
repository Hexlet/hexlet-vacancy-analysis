export interface StaticticsCardProp {
 id: string;
 value: number;
 label: string;
 suffix: string;
}

export const staticticsCardsData: StaticticsCardProp[] = [
 { id: "1", value: 15000, label: "Вакансий", suffix: "+" },
 { id: "2", value: 500, label: "Компаний", suffix: "+" },
 { id: "3", value: 95, label: "Точность", suffix: "%" },
];

export interface VacancyCardProp {
 id: string;
 title: string;
 count: number;
 change: number;
 location: string;
}

export const popularVacancies: VacancyCardProp[] = [
 {
  id: "1",
  title: "Frontend разработчик",
  count: 1247,
  change: 15,
  location: "По всей России",
 },
 {
  id: "2",
  title: "Backend разработчик",
  count: 892,
  change: 8,
  location: "По всей России",
 },
 {
  id: "3",
  title: "DevOps инженер",
  count: 543,
  change: 22,
  location: "По всей России",
 },
];