from app.services.parser.models import HhVacancy, SuperjobVacancy


class VacancySaver:
    def save_vacancy(self, vacancy_data, source='hh'):
        if source == 'hh':
            model = HhVacancy
        else:
            model = SuperjobVacancy

        model.objects.update_or_create(
            defaults=vacancy_data
        )
