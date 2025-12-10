import React from 'react';
import { ArrowTrendingUpIcon } from "@heroicons/react/16/solid";
import { CurrencyDollarIcon, LightBulbIcon, CheckIcon } from "@heroicons/react/24/outline";



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
        title: 'Базовый',
        subtitle: 'Для начинающих специалистов',
        price: '₽0 ',
        period: ' /навсегда',
        features: [
            'Просмотр аналитики рынка',
            'Базовые отчеты',
            '50 запросов/месяц',
            'Доступ к вакансиям',
            'Email поддержка',
        ],
    },
    {
        id: 'pro',
        title: 'Профи',
        subtitle: 'Для активного поиска работы',
        price: '₽29,990 ',
        period: ' /мес',
        features: [
            'Все из базового',
            'Безлимитные запросы',
            'Расширенная аналитика',
            'Персональные рекомендации',
            'Тота ИИ помощник',
            'Приоритетная поддержка',
            'Отчеты по карьерному росту',
        ],
        highlighted: true,
    },
    {
        id: 'enterprise',
        title: 'Премиум',
        subtitle: 'Для профессионалов',
        price: '₽990',
        period: ' /мес',
        features: [
            'Все из Профи',
            'AI карьерный консультант',
            'Индивидуальный план развития',
            'Прогнозы зарплат',
            'Эксклюзивные вакансии',
            'Менторство от экспертов',
            'Приоритет в рекомендациях',
            'Персональный менеджер',
        ],
    },
];


interface FaqItem {
 question: string;
 answer: string;
}

export const faqData: FaqItem[] = [
 {
  question: "Можно ли отменить подписку?",
  answer: "Да, вы можете отменить подписку в любой момент без штрафов.",
 },
 {
  question: "Какие способы оплаты доступны?",
  answer: "Принимаем банковские карты, СБП, PayPal и криптовалюту.",
 },
 {
  question: "Есть ли скидки для студентов?",
  answer: "Да! Студентам предоставляется скидка 50% на все тарифы.",
 },
 {
  question: "Можно ли перейти на другой тариф?",
  answer: "Конечно! Вы можете изменить тариф в любое время.",
 },
];

export interface FeatureCardData {
  id: string; 
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>; 
  title: string;
  description: string;
}

export const featuresData: FeatureCardData[] = [
  {
    id: 'career-growth',
    icon: ArrowTrendingUpIcon,
    title: 'Рост карьеры',
    description: 'Персональные рекомендации для развития',
  },
  {
    id: 'salary-increase',
    icon: CurrencyDollarIcon,
    title: 'Увеличение зарплаты',
    description: 'Данные для успешных переговоров',
  },
  {
    id: 'ai-assistant',
    icon: LightBulbIcon,
    title: 'AI помощник',
    description: 'Умный ассистент для карьерных решений',
  },
  {
    id: 'accurate-forecasts',
    icon: CheckIcon,
    title: 'Точные прогнозы',
    description: 'Аналитика трендов и востребованности',
  },
];