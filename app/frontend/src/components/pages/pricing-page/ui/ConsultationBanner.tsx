import { Paper, Title, Text, Button, Stack } from '@mantine/core';
import { ChatBubbleOvalLeftIcon } from '@heroicons/react/24/outline';



const ConsultationBanner = () => {
  return (
    <Paper
     style={{
        background: `linear-gradient(to right, #4ECDC4, #00334d)`,
        color: '#FFFFFF', 
        textAlign: 'center',
        boxShadow: '0 10px 20px rgba(0, 0, 0, 0.3)', 
      }}
      radius="md"
      p={60} 
      maw={1120} 
      mx="auto" 
      mb="40px"
    >
      <Stack align="center" >
        <Title order={2} c="white" fw={600}>
          Нужна консультация?
        </Title>
        <Text size="lg" c="white" maw={600} mb="lg">
          Наши эксперты помогут выбрать оптимальный тариф для ваших целей
        </Text>

        <Button
          variant="white" 
          color="dark" 
          radius="md"
          size="lg"
          leftSection={<ChatBubbleOvalLeftIcon style={{ width: 18, height: 18 }}/>}
        > 
          Связаться с нами
        </Button>
      </Stack>
    </Paper>
  );
}

export default ConsultationBanner


