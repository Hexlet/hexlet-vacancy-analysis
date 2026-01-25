import React from "react";
import {
 Card,
 Flex,
 Text,
 Stack,
 Badge,
 rem,
 Loader,
 Alert,
} from "@mantine/core";
import { ArrowTrendingUpIcon, MapPinIcon } from "@heroicons/react/24/outline";

import { type VacancyCardProp } from "../api/data";
import { useGetPopularVacanciesQuery } from "../../../../store/api/vacanciesApi";

const VacancyItem = (props: VacancyCardProp) => {
 const isPositiveChange = props.change >= 0;

 const badgeBg = isPositiveChange ? "#418387" : "red.5";
 const badgeColor = isPositiveChange ? "#74e8c1" : "white";

 return (
  <Flex
   justify="space-between"
   align="center"
   p="sm"
   style={{
    background: "#327087",
    borderRadius: "10px",
   }}
  >
   <Stack gap={rem(2)}>
    <Text fz="md" fw={600} c="white">
     {props.title}
    </Text>
    <Text fz="sm">{props.count} вакансий</Text>
   </Stack>
   <Stack align="flex-end" gap={rem(4)}>
    <Badge
     radius="10px"
     size="md"
     bg={badgeBg}
     c={badgeColor}
     fw={500}
     px={rem(8)}
     py={rem(2)}
     style={{
      border: "1px solid #56BB93",
     }}
    >
     {isPositiveChange ? `+${props.change}%` : `${props.change}%`}
    </Badge>
    <Flex align="center" gap={rem(4)}>
     <MapPinIcon width={16} height={16} />
     <Text fz="sm">{props.location}</Text>
    </Flex>
   </Stack>
  </Flex>
 );
};

const PopularVacanciesCard: React.FC = () => {
 const {
  data: popularVacancies,
  error,
  isLoading,
 } = useGetPopularVacanciesQuery();

 if (isLoading) {
  return (
   <Stack align="center" ta="center" mt="70px" mb="xl">
    <Loader size="xl" color="rgba(50, 65, 102, 1)" />
    <Text>Загрузка популярных вакансий...</Text>
   </Stack>
  );
 }

 if (error) {
  let errorMessage = "Произошла неизвестная ошибка";
  if ("status" in error && "data" in error) {
   errorMessage = `Ошибка ${error.status}: ${JSON.stringify(error.data)}`;
  } else if (error instanceof Error) {
   errorMessage = error.message;
  }
  return (
   <Stack align="center" ta="center" mt="70px" mb="xl">
    <Alert title="Ошибка загрузки" color="red">
     {errorMessage}
    </Alert>
   </Stack>
  );
 }

 return (
  <Card
   radius="lg"
   mt="50px"
   mb="30px"
   p="xl"
   shadow="md"
   maw={rem(580)}
   w="100%"
   style={{
    background: "linear-gradient(90deg, #326580 , #1FA4AB)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    color: "white",
   }}
  >
   <Flex justify="space-between" align="center" mb="lg">
    <Text fz="lg" fw={500} c="white">
     Популярные вакансии
    </Text>
    <ArrowTrendingUpIcon width={30} height={25} color="#4ECDC4" />
   </Flex>

   <Stack gap="md" maw="600px">
    {popularVacancies?.map((vacancy) => (
     <VacancyItem key={vacancy.id} {...vacancy} />
    ))}
   </Stack>
  </Card>
 );
};

export default PopularVacanciesCard;
