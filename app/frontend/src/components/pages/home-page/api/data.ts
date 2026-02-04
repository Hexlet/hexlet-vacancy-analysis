import { MagnifyingGlassIcon, MapPinIcon, BellIcon, ChartBarIcon, ClipboardDocumentIcon } from "@heroicons/react/24/outline";
import { ArrowTrendingUpIcon } from "@heroicons/react/16/solid";
import React from "react";



type FeatureKeys = "monitor" | "search" | "chart" | "map" | "document" | "bell";

interface Feature {
  id: number;
  title: string;
  text: string;
  icon: FeatureKeys;
}

interface FeaturesBlockData {
  greeting: string,
  description: string,
  features: Feature[]
}

// примерные данные с бекенда

export const featuresData: FeaturesBlockData = {
  greeting: "Привет, мы Skill Pulse 👋",
  description: "Экосистема для мониторинга рынка труда, которая помогает принимать взвешенные карьерные решения на основе реальных данных",
  features: [{
    id: 1,
    title: "Мониторинг рынка труда",
    text: "Отслеживайте актуальные тренды и изменения на рынке IT в реальном времени",
    icon: "monitor",
  },
  {
    id: 2,
    title: "Анализ вакансий",
    text: "Детальная аналитика по зарплатам, навыкам и требованиям работодателей",
    icon: "search"
  },
  {
    id: 3,
    title: "Прогнозы и тренды",
    text: "Предсказание востребованности технологий на основе ML-алгоритмов",
    icon: "chart",
  },
  {
    id: 4,
    title: "Региональная карта",
    text: "Интерактивная география вакансий по всей России с детальной статистикой",
    icon: "map",
  },
  {
    id: 5,
    title: "Автоматические отчеты",
    text: "Еженедельные дайджесты и персонализированные аналитические отчеты",
    icon: "document",
  },
  {
    id: 6,
    title: "Уведомления",
    text: "Получайте оповещения о новых возможностях и изменениях на рынке",
    icon: "bell",
  },
  ]
};

// словарь для отображения данных с бекенда для отрисовки иконок

export const hashmapForFeaturesIcons: Record<FeatureKeys, React.ElementType<React.SVGProps<SVGSVGElement>>> = {
  monitor: ChartBarIcon,
  search: MagnifyingGlassIcon,
  chart: ArrowTrendingUpIcon,
  map: MapPinIcon,
  document: ClipboardDocumentIcon,
  bell: BellIcon
};
