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