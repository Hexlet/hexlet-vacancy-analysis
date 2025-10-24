from app.services.parser.models import HhVacancy, SuperjobVacancy


class VacancySaver:
    def save_vacancy(self, vacancy_data, source='hh'):
        if source == 'hh':
            model = HhVacancy
            model.objects.update_or_create(
                hh_id=vacancy_data.get('hh_id'),
                defaults=vacancy_data
            )
        elif source == 'superjob':
            model = SuperjobVacancy
            model.objects.update_or_create(
                superjob_id=vacancy_data.get('superjob_id'),
                defaults=vacancy_data
            )
