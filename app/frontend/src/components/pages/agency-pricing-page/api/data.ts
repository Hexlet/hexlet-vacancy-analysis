import { CircleStackIcon, ShieldCheckIcon, PhoneIcon, UserGroupIcon} from "@heroicons/react/16/solid";

export const advantages = [
  {
    icon: UserGroupIcon,
    title: "Командная работа",
    description: "Управление доступами и совместная работа",
  },
  {
    icon: CircleStackIcon,
    title: "API интеграция",
    description: "Подключение к вашим внутренним системам",
  },
  {
    icon: ShieldCheckIcon,
    title: "Безопасность",
    description: "Защита данных на уровне enterprise",
  },
  {
    icon: PhoneIcon,
    title: "Поддержка 24/7",
    description: "Персональный менеджер и техподдержка",
  },
];


type Plan = {
  id: string;
  title: string;
  subtitle: string;
  price: string;
  period: string;
  features: string[];
  highlighted?: boolean;
};

export const plans: Plan[] = [
  {
    id: 'starter',
    title: 'Стартовый',
    subtitle: 'Для небольших HR-команд',
    price: '₽14,990 ',
    period: ' /мес',
    features: [
      'До 5 пользователей',
      '1000 запросов/месяц',
      'Базовая аналитика',
      'Email поддержка',
      'Еженедельные отчеты',
    ],
  },
  {
    id: 'pro',
    title: 'Профессиональный',
    subtitle: 'Для агентств и средних компаний',
    price: '₽29,990 ',
    period: ' /мес',
    features: [
      'До 20 пользователей',
      'Безлимитные запросы',
      'Расширенная аналитика',
      'API доступ',
      'Приоритетная поддержка',
      'Кастомные отчеты',
      'Интеграции',
    ],
    highlighted: true,
  },
  {
    id: 'enterprise',
    title: 'Корпоративный',
    subtitle: 'Для крупных компаний',
    price: '₽49,990',
    period: ' /мес',
    features: [
      'До 50 пользователей',
      'Безлимитные запросы',
      'Полная аналитика + AI',
      'API доступ',
      'Персональный менеджер',
      'SLA 99.9%',
      'Кастомные интеграции',
      'Обучение команды',
    ],
  },
];