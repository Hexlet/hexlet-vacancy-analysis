export interface StaticticsCardProp {
    id: string;
    value: number;
    label: string;
    suffix: string;
}

export const statictiscCardsData: StaticticsCardProp[] = [
    { id: "1", value: 15000, label: "Вакансий", suffix: "+" },
    { id: "2", value: 500, label: "Компаний", suffix: "+" },
    { id: "3", value: 95, label: "Точность", suffix: "%" },
];