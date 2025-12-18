import {
 Title,
 Text,
 Stack,
 Group,
 Flex,
 ThemeIcon,
 Loader,
 Alert,
} from "@mantine/core";

import { CheckCircleIcon } from "@heroicons/react/24/outline";
import PricingCard from "./PricingCard";
import { useGetPricingPlansQuery } from "../../../../store/api/planApi";

const PricingSection = () => {
 const { data: plans, error, isLoading } = useGetPricingPlansQuery();

 if (isLoading) {
  return (
   <Stack align="center" ta="center" mt="70px" mb="xl">
    <Loader size="xl" color="rgba(50, 65, 102, 1)" />
    <Text>Загрузка тарифных планов...</Text>
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
  <Stack align="center" ta="center" mt="70px" mb="xl">
   <Title order={1} c="dark">
    Выберите свой план
   </Title>
   <Text size="lg" c="dimmed">
    Инвестируйте в свою карьеру с прозрачными ценами и без скрытых платежей
   </Text>
   <Group mb="xl">
    <Flex
     direction={{ base: "column", md: "row" }}
     gap="10px"
     align="flex-start"
    >
     <Flex gap="5px" align="center" ta="center">
      <ThemeIcon size="sm" radius="xl" color="#4ECDC4" variant="light">
       <CheckCircleIcon />
      </ThemeIcon>
      <Text size="xs" c="dimmed">
       Отмена в любое время
      </Text>
     </Flex>
     <Flex gap="5px" align="center" ta="center">
      <ThemeIcon size="sm" radius="xl" color="#4ECDC4" variant="light">
       <CheckCircleIcon />
      </ThemeIcon>
      <Text size="xs" c="dimmed">
       Безопасные платежи
      </Text>
     </Flex>
     <Flex gap="5px" align="center" ta="center">
      <ThemeIcon size="sm" radius="xl" color="#4ECDC4" variant="light">
       <CheckCircleIcon />
      </ThemeIcon>
      <Text size="xs" c="dimmed">
       Возврат средств в течении 14 дней
      </Text>
     </Flex>
    </Flex>
   </Group>
   <Flex
    gap="xl"
    wrap="wrap"
    justify="center"
    align="stretch"
    style={{ width: "100%" }}
   >
    {plans?.map((plan) => (
     <PricingCard key={plan.id} {...plan} />
    ))}
   </Flex>
  </Stack>
 );
};

export default PricingSection;
