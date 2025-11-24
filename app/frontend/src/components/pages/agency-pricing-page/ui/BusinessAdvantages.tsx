import { Title, Stack, Group, Text, ThemeIcon } from "@mantine/core";
import { advantages } from "../api/data";

const BusinessAdvantages = () => {
 return (
  <Stack>
   <Title order={2} c="white" mb="xl" ta="left">
    Преимущества для бизнеса
   </Title>
   <Stack gap="lg">
    {advantages.map((advantage, index) => (
     <Group key={index} wrap="nowrap" align="flex-start">
      <ThemeIcon
       size="lg"
       radius="md"
       variant="light"
       color="#4ECDC4"
       style={{
        backgroundColor: "transparent",
        border: "1px solid #4ECDC4",
       }}
      >
       <advantage.icon size={24} stroke={1.5} />
      </ThemeIcon>
      <Stack gap={4}>
       <Text fw={700} c="white">
        {advantage.title}
       </Text>
       <Text size="sm" c="dimmed">
        {advantage.description}
       </Text>
      </Stack>
     </Group>
    ))}
   </Stack>
  </Stack>
 );
};

export default BusinessAdvantages;
