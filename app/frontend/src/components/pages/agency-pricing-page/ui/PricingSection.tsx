import { Title, Text, Stack, Flex, Loader, Alert } from "@mantine/core";
import PricingCard from "./PricingCard";
import { useGetAgencyPlansQuery } from "../../../../store/api/plansApi";

const PricingSection = () => {
 const { data: plans, error, isLoading } = useGetAgencyPlansQuery();

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
    {plans?.map((plan) => (
     <PricingCard key={plan.id} {...plan} />
    ))}
   </Flex>
  </Stack>
 );
};

export default PricingSection;
