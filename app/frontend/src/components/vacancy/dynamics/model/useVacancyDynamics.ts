import { useMemo } from "react";
import type { VacancyWithDynamics } from "../../model/types";

const monthOrder = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];

export function useVacancyDynamics(vacancies: VacancyWithDynamics[]) {
  return useMemo(() => {
    const monthCounts: Record<string, number> = {};

    monthOrder.forEach((month) => {
      monthCounts[month] = 0;
    })

    for (const vacancy of vacancies) {
      for (const dynamics of vacancy.dynamics) {
        monthCounts[dynamics.month] = (monthCounts[dynamics.month] || 0) + dynamics.count;
      }
    }

    const data = monthOrder.map((month) => ({ month, count: monthCounts[month] })).filter((item) => item.count > 0);

    return data;
  }, [vacancies]);
}