import { useState, useEffect } from 'react'; 


import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { useAppDispatch } from '../../../store/hooks';
import { useTranslation } from 'react-i18next';
import {
  signup, clearAuthError, getAuthStatus, getAuthError,
} from '../../../store/authSlice';
import { useForm } from '@mantine/form';
import '@mantine/core/styles.css';
import { notifications } from '@mantine/notifications';
import {
  TextInput,
  PasswordInput,
  Button,
  Alert,
  Card,
  Container,
  Title,
  Text,
  Anchor,
  Group,
  Checkbox,
  Image
} from '@mantine/core';
import vkIcon from '../../assets/VK_icon.png';
import gitHubIcon from '../../assets/GitHub_icon.png';
import yandexIcon from '../../assets/Yandex_icon.png';
import tBankIcon from '../../assets/T-Bank_icon.png';
import sberBankIcon from '../../assets/ SberBank_icon.png';


const RegisterPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const status = useSelector(getAuthStatus);
  const signupError = useSelector(getAuthError);
  const [liveErrors, setLiveErrors] = useState<Record<string, string>>({});

  const form = useForm({
    initialValues: {
      email: '',
      password: '',
      confirmPassword: '',
      terms: false,
    },
    validate: {
      email: (value) => {
        // Проверка на пустое значение
        if (!value) return t('errors.validation.emailRequired');
      
        // Регулярное выражение для проверки email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          return t('errors.validation.emailCorrect');
        }

        // Валидация пройдена
        return null;
      },
      password: (value) => {
        if (!value) return t('errors.validation.required');
      
        // Минимальная длина 8 символов
        if (value.length <= 8) return t('errors.validation.passwdMinLength');
        
        // Проверка на наличие цифры
        if (!/\d/.test(value)) return t('errors.validation.passwdNumContain');
        
        // Проверка на спецсимвол
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
          return t('errors.validation.passwdSpecCharContain');
        }
        
        return null;
      },
      confirmPassword: (value, values) => 
        value !== values.password 
          ? t('errors.validation.confirmPasswdConfirm') 
          : null,
      terms: (value) => 
        !value 
          ? 'Вы должны принять условия' 
          : null,
    },
  });

  // Обновление live errors при изменении ошибок формы
  useEffect(() => {
    const errors: Record<string, string> = {};
    Object.entries(form.errors).forEach(([key, value]) => {
      if (value) errors[key] = value;
    });
    setLiveErrors(errors);
  }, [form.errors]);

  const handleSubmit = (values: typeof form.values) => {
    dispatch(clearAuthError());
    setLiveErrors({});


    dispatch(signup(values))
    .unwrap()
    .then(() => {
      notifications.show({
        title: 'Успех',
        message: 'Добро пожаловать!',
        color: 'green',
      });
      setTimeout(() => navigate('/'), 1500);
    })
    .catch((err: string) => {
      const errorMsg = err.includes('409') 
        ? t('errors.signupUserUnique') 
        : t('errors.unknown');
      
      form.setErrors({ email: errorMsg });
      setLiveErrors({ email: errorMsg });
    });
  };

  // Компонент для ARIA live сообщений
  const AriaLiveMessages = () => (
    <div 
      aria-live="polite" 
      aria-atomic="true" 
      style={{ 
        position: 'absolute', 
        left: '-9999px', 
        width: '1px', 
        height: '1px', 
        overflow: 'hidden' 
      }}
    >
      {Object.entries(liveErrors).map(([field, error]) => (
        <div key={field}>{`${field}: ${error}`}</div>
      ))}
      {status === 'failed' && signupError && (
        <div>{signupError}</div>
      )}
    </div>
  );

  return (
    <Container size={400} px="md" py="xl">
      <AriaLiveMessages />

      <Card shadow="sm" p="lg" radius="md" withBorder>

        <Title order={1} ta="center" mb="lg">
          {t('login.signup')}
        </Title>

        <Text ta="center" mb="lg" c="dimmed">
          Используйте привычный способ входа
        </Text>

        <Group align="center" gap="md" justify="center" mb= "lg">
          <Anchor href="#" target="_blank">
            {/*<IconBrandVk size={32} color="#4C75A3" />*/}
            <Image 
              src={vkIcon}
              alt="VK"
              radius="md"
              style={{ width: 32, height: 32 }}
            />
          </Anchor>
          <Anchor href="#" target="_blank">
            <Image 
              src={yandexIcon}
              alt="Yandex"
              radius="md"
              style={{ width: 32, height: 32 }}
            />
            {/*<IconBrandYandex size={32} color="#FF0000" />*/}
          </Anchor>
          <Anchor href="#" target="_blank">
            <Image 
              src={sberBankIcon}
              alt="SberBank"
              radius="md"
              style={{ width: 32, height: 32 }}
            />
            {/*<SberbankidPrdIcon20/>*/}
            {/*<SberIDButton onClick={() => {}} size={32}/>*/}
          </Anchor>
          <Anchor href="#" target="_blank">
            <Image 
              src={tBankIcon}
              alt="T-Bank"
              radius="md"
              style={{ width: 32, height: 32 }}
            />
            {/*<IconBrandTinkoff size={32} color="#1E96C8" />*/}
          </Anchor>
          <Anchor href="#" target="_blank">
            <Image 
              src={gitHubIcon}
              alt="GitHub"
              radius="md"
              style={{ width: 32, height: 32 }}
            />
            {/*<IconBrandGithub size={32} color="#333333" />*/}
          </Anchor>
        </Group>

        <Text ta="center" mb="lg" c="dimmed">
          или
        </Text>

        {status === 'failed' && signupError && (
          <Alert 
            color="red" 
            mb="lg" 
            role="alert"
            aria-live="assertive"
          >
            {signupError}
          </Alert>
        )}

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            placeholder="E-mail"
            {...form.getInputProps('email')}
            mb="md"
            required
            onBlur={() => form.validateField('email')}
            onChange={(e) => {
              form.getInputProps('email').onChange(e);
              if (e.currentTarget.value.length > 0) {
                form.validateField('email');
              }
            }}
          />

          <PasswordInput
            placeholder="Пароль"
            {...form.getInputProps('password')}
            mb="md"
            required
            onBlur={() => form.validateField('password')}
            onChange={(e) => {
              form.getInputProps('password').onChange(e);
              if (e.currentTarget.value.length >= 8) {
                form.validateField('password');
              }
            }}
          />

          <PasswordInput
            placeholder="Повторите пароль"
            {...form.getInputProps('confirmPassword')}
            mb="md"
            required
            onBlur={() => form.validateField('confirmPassword')}
            onChange={(e) => {
              form.getInputProps('confirmPassword').onChange(e);
              if (e.currentTarget.value.length > 0) {
                form.validateField('confirmPassword');
              }
            }}
          />


          <Checkbox
            mt="md"
            id="terms-checkbox"
            label={
              <>
                Я принимаю условия
              </>
            }
            {...form.getInputProps('terms', { type: 'checkbox' })}
          />

          <Button 
            type="submit" 
            fullWidth 
            size="md" 
            mt="xl"
            disabled={status === 'loading' || !form.isValid()}
            loading={status === 'loading'}
          >
            {t('signup.signup')}
          </Button>
        </form>

        <Text ta="center" mt="md">
          Уже есть аккаунт?{' '}
          <Anchor
            onClick={() => navigate('/login')}
            underline="hover"
            aria-label="Перейти к странице входа"
          >
            {t('signup.input')}
          </Anchor>
        </Text>
      </Card>
    </Container>
  );
};

export default RegisterPage;