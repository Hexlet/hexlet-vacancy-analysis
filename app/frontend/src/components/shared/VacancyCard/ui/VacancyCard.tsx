import React from "react";
import type { VacancyCardProps } from "../../../../types";
import { Card, Group, Text, Badge, Button, Stack, Box } from '@mantine/core';
import { Building2, MapPin, ChevronDown, ChevronUp, Send } from "lucide-react";
import { useState } from "react";
import { router } from "@inertiajs/core";

interface VacancyCardPropsWrapper {
  props: VacancyCardProps;
}

export const VacancyCard: React.FC<VacancyCardPropsWrapper> = ({ props }) => {

  const { id, title, url, salary, employment, company, city, skills } = props;

  const [skillsExpanded, setSkillsExpanded] = useState(false);

  const skillsCutDesktop = skills.slice(0,12);
  const remainingSkillsCount = skills.length - 3;
  const hasMoreSkills = skills.length > 3;

  const displayedSkills = skillsExpanded ? skills : skills.slice(0, 3);

  const handleCardLink = (e: React.MouseEvent) => {
    e.preventDefault();
    router.get(`/vacancies/${id}`)
  };

  const handleButtonLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(url, '_blank')
  }

  return (
     <Card 
      shadow="sm" 
      padding="lg" 
      radius="md" 
      withBorder 
      mx="auto" 
      style={{ width: '100%', cursor: 'pointer'}} 
      mb={20}
      onClick={handleCardLink}
      >
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
                skillsCutDesktop.map((skill) => (
                  <Badge 
                    key={skill} 
                    color="#20B0B4"
                    variant="outline"
                    size="md"
                    style={{ width: 'auto'}}
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
            onClick={handleButtonLink}
          >
            <Group gap={10}>
              <Send size={15}/>
              <span>Откликнуться</span>
            </Group>
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
         <Stack gap="xs">
          <Group wrap="wrap" gap="xs" style={{ alignItems: 'center' }}>
            {skills && skills.length > 0 ? (
              <>
                {displayedSkills.map((skill) => (
                  <Badge 
                    key={skill} 
                    color="#20B0B4"
                    variant="outline"
                    size="md"
                    style={{ width: 'auto', flexShrink: 0 }}
                  >
                    {skill}
                  </Badge>
                ))}
                
                {/* Кнопка для показа/скрытия навыков */}
                {hasMoreSkills && (
                  <Button
                    variant="subtle"
                    color="#20B0B4"
                    size="compact-md"
                    radius='xl'
                    style={{ 
                      height: '32px',
                      flexShrink: 0,
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '0 10px'
                    }}
                    onClick={(e) => {
                      e.stopPropagation();
                      setSkillsExpanded(!skillsExpanded)}
                    }
                  >
                    <span>{skillsExpanded ? 'Свернуть' : `...ещё ${remainingSkillsCount}`}</span>
                    {skillsExpanded ? <ChevronUp/> : <ChevronDown/>}
                  </Button>
                )}
              </>
            ) : (
              <Text fw={700} size="md" c="#0d2e4e">Необходимые навыки не указаны</Text>
            )}
          </Group>
        </Stack>

        <Button 
          color="#20B0B4" 
          radius='md' 
          fullWidth
        >
          <Group gap={10}>
            <Send size={15}/>
            <span>Откликнуться</span>
          </Group>
        </Button>
      </Stack>
    </Card>
  );
};

