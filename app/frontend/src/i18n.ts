import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import translationRU from './Locales/ru.json';
// import translationEN from './Locales/en.json';

// Используем встроенный тип Resource из i18next
const resources: i18n.Resource = {
  ru: {
    translation: translationRU, // translationRU должен соответствовать Record<string, string>
  },
  // en: {
  //   translation: translationEN,
  // },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'ru',
    fallbackLng: 'ru',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;