import { router } from '@inertiajs/react';
import { Box, Button, CloseButton, Container, Group, Pagination, Text, TextInput, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { Search } from 'lucide-react';
import type { VacancyCardProps } from '../../types';
import { VacancyCard } from '../shared/VacancyCard';

type PaginationMeta = {
  total_pages: number;
  current_page: number;
};

type VacancyPageProps = {
  vacancies: VacancyCardProps[];
  pagination: PaginationMeta;
};

function VacanciesPage({ vacancies, pagination }: VacancyPageProps) {
  const form = useForm({
    mode: "uncontrolled",
    initialValues: {
      search: "",
      termsOfService: false,
    },
    onValuesChange: (value) => {
      if (!value.search) {
        handleSearch()
      }
    }
  });

  const handlePageChange = (pageNumber: number) => {
    router.get('', { search: form.getValues().search, page: pageNumber }, { preserveState: true, replace: true });
  }

  function handleSearch() {
    router.get('', { search: form.getValues().search, page: 1 }, {
      preserveState: true,
      replace: true,
    });
  }

  if (!vacancies) return "Loading..."

  return (
    <Container>
      <Title>Поиск вакансий</Title>
      <Text size="sm" c="dimmed">
        Найдите работу мечты среди тысяч IT-вакансий
      </Text>

      <form onSubmit={form.onSubmit(handleSearch)}>
        <Group mb={20} mt="xs" justify="space-between">
          <Box w="80%">
            <TextInput
              {...form.getInputProps('search')}
              radius="md"
              size="md"
              placeholder="Должность, технология или компания…"
              rightSection={<CloseButton onClick={form.reset} />}
              key={form.key('search')}
            />
          </Box>
          <Button type="submit" leftSection={<Search />} >Искать</Button>
        </Group>
      </form>

      {vacancies.map((vacancy) => (
        <VacancyCard key={vacancy.id} props={vacancy} />
      ))}

      <Pagination
        total={pagination.total_pages}
        value={pagination.current_page}
        onChange={handlePageChange}
        mt="sm"
      />

    </Container>
  );
}

export default VacanciesPage;