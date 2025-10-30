import React from "react";
import type { VacancyCardProps } from "../../../../types";
import { Card, Group, Text, Badge, Button, Stack, Box } from '@mantine/core';
import { Building2, MapPin } from "lucide-react";
import { Link } from "@inertiajs/react";

interface VacancyCardPropsWrapper {
  props: VacancyCardProps;
}

export const VacancyCard: React.FC<VacancyCardPropsWrapper> = ({ props }) => {

  const { id, title, url, salary, employment, company, city, skills } = props;
  return (
    <Link href={url || `/vacancies/${id}`} style={{ textDecoration: 'none' }}>
     <Card shadow="sm" padding="lg" radius="md" withBorder mx="auto" style={{ width: '100%'}}>
      {/* Десктопная версия */}
      <Group justify="space-between" wrap="nowrap" visibleFrom="sm">
        {/* Левая часть */}
        <Box style={{ flex: 1 }} maw='60%'>
          <Stack gap='xs'>
            {/* Название вакансии */}
            <Text fw={700} size="xl" c="#0d2e4e">{title}</Text>

            {/* Информация о компании */}
            <Group gap='xs'>
              {company ? 
                <Group gap={5}>
                  <Building2 size={16} />
                  <Text size="md">{company.name}</Text>
                </Group> :
                <Text fw={700} size="md" c="#0d2e4e">Название компании не указано</Text>
              }
              {city ? 
                <Group gap={5}>
                  <MapPin size={16} />
                  <Text>{city.name}</Text>
                </Group> :
                <Text fw={700} size="md" c="#0d2e4e">Город не указан</Text>
              }
              <Badge color="#20B0B4">{employment}</Badge>
            </Group>

            {/* Навыки */}
        <Group wrap="wrap" gap="xs">
          {skills && skills.length > 0 ? (
            skills.map((skill) => (
              <Badge 
                key={skill} 
                color="#20B0B4"
                variant="outline"
                size="md"
                style={{ width: 'auto' }}
              >
                {skill}
              </Badge>
            ))
          ) : (
            <Text fw={700} size="md" c="#0d2e4e">Необходимые навыки не указаны</Text>
          )}
        </Group>
          </Stack>
        </Box>

        {/* Правая часть */}
        
        <Stack gap="md" align="flex-end">
          {salary ?
          <Text size="xl" fw={700} c='#20B0B4'>{salary}</Text> :
          <Text size="xl" fw={700} c='#0d2e4e'>Зарплата не указана</Text>
          }
          <Button 
            w='fit-content' 
            color="#20B0B4" 
            radius='md'
            onClick={(e) => e.preventDefault()}
          >
            Откликнуться
          </Button>
        </Stack>
      </Group>

      {/* Мобильная версия */}
      <Stack gap="md" hiddenFrom="sm">
        {/* Название вакансии */}
        <Text fw={700} size="xl" c="#0d2e4e">{title}</Text>

        {/* Компания и город */}
        <Group gap='xs'>
          {company ? 
          <Group gap={5}>
            <Building2 size={16} />
              <Text size="md">{company.name}</Text>
          </Group> :
          <Text fw={700} size="md" c="#0d2e4e">Название компании не указано</Text>
          }
          {city ? 
          <Group gap={5}>
            <MapPin size={16} />
            <Text>{city.name}</Text>
          </Group> :
          <Text fw={700} size="md" c="#0d2e4e">Город не указан</Text>
          }
        </Group>

        {/* Формат работы */}
        <Badge color="#20B0B4" w="fit-content">{employment}</Badge>

        {/* Зарплата */}
        {salary ?
          <Text size="xl" fw={700} c='#20B0B4'>{salary}</Text> :
          <Text size="xl" fw={700} c='#0d2e4e'>Зарплата не указана</Text>
        }

        {/* Навыки */}
        <Group wrap="wrap" gap="xs">
          {skills && skills.length > 0 ? (
            skills.map((skill) => (
              <Badge 
                key={skill} 
                color="#20B0B4"
                variant="outline"
                size="md"
                style={{ width: 'auto' }}
              >
                {skill}
              </Badge>
            ))
          ) : (
            <Text fw={700} size="md" c="#0d2e4e">Необходимые навыки не указаны</Text>
          )}
        </Group>

        <Button color="#20B0B4" radius='md' fullWidth>Откликнуться</Button>
      </Stack>
    </Card>
    </Link>
  );
};