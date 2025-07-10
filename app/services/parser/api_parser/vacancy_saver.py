from app.services.parser.models import HhVacancy, SuperjobVacancy


class VacancySaver:
    @staticmethod
    def save_vacancy(vacancy_data, source='hh'):
        if source == 'hh':
            model = HhVacancy
            id_field = 'hh_id'
        else:
            model = SuperjobVacancy
            id_field = 'superjob_id'

        model.objects.update_or_create(
            **{id_field: vacancy_data['source_id']},
            defaults=vacancy_data
        )
