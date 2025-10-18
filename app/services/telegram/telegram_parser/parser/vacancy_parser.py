from app.services.hh.hh_parser.models import Vacancy

from .keyword_extractor import KeywordExtractor
from .line_parser import LineParser


class VacancyParser(KeywordExtractor):
    def __init__(self):
        super().__init__()

    async def parse_vacancy_from_text(self, text):
        await self.load_keywords()

        lines = text.strip().splitlines()
        parser = LineParser()

        all_fields = Vacancy._meta.get_fields()
        field_names = [field.name for field in all_fields]

        data = dict.fromkeys(field_names)
        data['title'] = next(
            (line.strip() for line in lines if line.strip()), None)

        actions = [
            ('company',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'company') else None),
            ('salary',
             lambda line: parser.extract_salary(line, self.keywords['salary'])
             if self.matches(line, 'salary') else None),
            ('city',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'city') else None),
            ('schedule',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'schedule') else None),
            ('work_format',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'work_format') else None),
            ('skills',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'skills') else None),
            ('description',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'description') else None),
            ('address',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'address') else None),
            ('experience',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'experience') else None),
            ('contacts', parser.extract_phone),
            ('url', parser.extract_link)
        ]

        for line in lines:
            line = line.strip()
            for key, func in actions:
                if not data[key]:
                    value = func(line)
                    if value:
                        data[key] = value

        return data
