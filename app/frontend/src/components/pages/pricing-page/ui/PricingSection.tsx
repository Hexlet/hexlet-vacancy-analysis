import { Title, Text, Stack, Group, Flex, ThemeIcon } from "@mantine/core";

import { CheckCircleIcon } from "@heroicons/react/24/outline";
import PricingCard from "./PricingCard";
import { plans } from "../api/data";

const PricingSection = () => {
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
    {plans.map((plan) => (
     <PricingCard key={plan.id} {...plan} />
    ))}
   </Flex>
  </Stack>
 );
};

export default PricingSection;
