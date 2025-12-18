import { Title, Stack, TextInput, Button, Text } from "@mantine/core";
import * as yup from "yup";
import { useForm, type SubmitHandler } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

// Схема валидации формы

export interface ContactFormData {
 companyName: string;
 fullName: string;
 email: string;
 phone: string;
}

const phoneRegExp = /^\+7(?:[()\s-]*\d){10}$/;

const contactFormSchema = yup.object().shape({
 companyName: yup
  .string()
  .min(3, 'Название компании должно содержать не менее 3 символов')
  .max(100, 'Название компании не должно превышать 100 символов')
  .required('Поле "Название компании" обязательно для заполнения'),

 fullName: yup
   .string()
   .min(3, 'Ваше имя должно содержать не менее 3 символов')
   .max(100, 'Ваше имя не должно превышать 100 символов')
   .required('Поле "Ваше имя" обязательно для заполнения'),

 email: yup
  .string()
  .email("Введите корректный Email адрес")
  .required('Поле "Email" обязательно для заполнения'),

 phone: yup
   .string()
   .required('Поле "Телефон" обязательно для заполнения')
   .matches(
      phoneRegExp,
      'Введите корректный номер телефона, начинающийся с +7'
   )
});

// сам компонент

const ContactForm = () => {
 const {
  register,
  handleSubmit,
  formState: { errors },
  reset,
 } = useForm<ContactFormData>({
  resolver: yupResolver(contactFormSchema),
  defaultValues: {
   companyName: "",
   fullName: "",
   email: "",
   phone: "",
  },
 });

 const onSubmit: SubmitHandler<ContactFormData> = () => {
  reset();
 };

 return (
  <Stack>
   <Title order={2} c="white" mb="xl" ta="left">
    Оставить заявку
   </Title>
   <Stack component="form" onSubmit={handleSubmit(onSubmit)} gap="md">
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
     {...register("companyName")}
     error={errors.companyName?.message}
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
     {...register("fullName")}
     error={errors.fullName?.message}
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
     {...register("email")}
     error={errors.email?.message}
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
     {...register("phone")}
     error={errors.phone?.message}
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
