import { Title, Stack, TextInput, Button, Text } from "@mantine/core";
import React from "react";

const ContactForm = () => {
 const handleSubmit = (event: React.FormEvent) => {
  event.preventDefault();
  console.log("Форма отправлена");
 };

 return (
  <Stack>
   <Title order={2} c="white" mb="xl" ta="left">
    Оставить заявку
   </Title>
   <Stack component="form" onSubmit={handleSubmit} gap="md">
    <TextInput
     placeholder="Название компании"
     size="lg"
     styles={{
      input: {
       backgroundColor: "#1A2F4B",
       color: "white",
       borderColor: "#4ECDC4",
       "&::placeholder": {
        color: "grey",
       },
       borderRadius: "8px",
      },
     }}
    />
    <TextInput
     placeholder="Ваше имя"
     size="lg"
     styles={{
      input: {
       backgroundColor: "#1A2F4B",
       color: "white",
       borderColor: "#4ECDC4",
       "&::placeholder": {
        color: "grey",
       },
       borderRadius: "8px",
      },
     }}
    />
    <TextInput
     placeholder="Email"
     type="email"
     size="lg"
     styles={{
      input: {
       backgroundColor: "#1A2F4B",
       color: "white",
       borderColor: "#4ECDC4",
       "&::placeholder": {
        color: "grey",
       },
       borderRadius: "8px",
      },
     }}
    />
    <TextInput
     placeholder="Телефон"
     type="tel"
     size="lg"
     styles={{
      input: {
       backgroundColor: "#1A2F4B",
       color: "white",
       borderColor: "#4ECDC4",
       "&::placeholder": {
        color: "grey",
       },
       borderRadius: "8px",
      },
     }}
    />
    <Button
     variant="filled"
     type="submit"
     fullWidth
     size="lg"
     color="#4ECDC4"
     radius="md"
     mt="md"
    >
     Отправить заявку
    </Button>
    <Text c="dimmed" size="sm" ta="center" mt="md">
     Мы свяжемся с вами в течение 24 часов
    </Text>
   </Stack>
  </Stack>
 );
};

export default ContactForm;
