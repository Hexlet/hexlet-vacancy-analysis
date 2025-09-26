import React from "react";
import { formatSalary } from "../../utils/FormatSalary";
// import { Link } from '@inertiajs/react';
import { truncateText } from "../../utils/TruncateText";
import type { VacancyProps } from "../../../vacancy/model/types";

export const VacancyCard: React.FC<VacancyProps> = (props) => {
  const { title, description, company, salary, city, id, key_skills } = props;
  
  return (
    // <Link href={`/vacancies/${id}`}>
        <div className="mx-auto border border-gray-200 rounded-lg shadow-sm p-6 m-4">
      {/* Информация о должности и город */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#0d2e4e] mb-2">{title}</h1>
        <p className="text-xl text-[#69717d]">{company} &bull; {city}</p>
      </div>
      {/* Зарплата и описание*/}   
      <div className="mb-4">
        <div className="flex justify-between items-start ">
          <p className="text-xl text-[#69717d] mb-3">Зарплата:</p>
          <div className="inline-flex items-center px-4 py-0.5 rounded-full bg-[#20B0B4]">
            <span className="text-white font-semibold">{formatSalary(salary)}</span>
          </div>
        </div>
        <p className="text-xl text-[#69717d]">{truncateText(description, 50)}</p>
      </div>
      {/* Ключевые навыки */}
      <div className="flex flex-wrap gap-3">
        {key_skills.map((skill) => (
          <div key={skill} className="inline-flex w-fit items-center px-4 py-0.5 border border-gray-200 rounded-full">
            <span className="font-bold text-[#0d2e4e]">{skill}</span>
          </div>
        ))}
      </div>
    </div>
    // </Link>
  )
}