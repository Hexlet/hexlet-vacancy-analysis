import { Title, Text, Stack, Flex } from "@mantine/core";
import PricingCard from "./PricingCard";
import { plans } from "../api/data";

const PricingSection = () => {
 return (
  <Stack align="center" ta="center" mt="70px" mb="xl">
   <Title order={1} c="dark">
    Решения для агентств и HR-команд
   </Title>
   <Text size="lg" c="dimmed" mb="xl">
    Мощные инструменты аналитики рынка труда для профессионального рекрутинга
   </Text>

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
