/**
 *  Форматирует строку с зарплатой. Разделяет тысячи пробелом, заменяет строковое название валюты на соответствующий символ
 * @param {string} salaryStr - строка с зарплатой
 * @returns Отформатированную строку зарплаты с разделенными пробелами тысячами и символами валют
 * @example
 * Вернет "100 000 Br"
 * formatSalary('100000 белорусских рублей')
 */

export const formatSalary = (salaryStr: string): string => {
  const rules: [RegExp, string][] = [
    [/(евро|euro|eur)/gi, '€'],
    [/(доллар|usd|\$)(ов|а)?/gi, '$'],
    [/белорусских\s*рубл(ей)?/gi, 'Br'],
    [/\b(бел|byn|br)\b/gi, 'Br'],
    [/(рубл|руб|rub|р\.?)(ей|я|ю|ем)?/gi, '₽'],
    [/(тенге|kzt|₸|тг)/gi, '₸']
  ]
  // Регулярка ищет в строке числа и разбивает по тысячам пробелами
  const formatted = salaryStr.replace(/\d+/g, (match) => {
    return parseInt(match).toLocaleString('ru-RU');
  });

  let result = formatted;

  for (const [regExp, sign] of rules) {
    result = result.replace(regExp, sign);
  }
  // Регулярка убирает лишние пробелы
  return result.replace(/\s+/g, ' ').trim();
}