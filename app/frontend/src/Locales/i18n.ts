import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import translationRU from './ru.json';
// import translationEN from './en.json';

// Тип для структуры переводов
type TranslationResources = {
  translation: typeof translationRU;
};

const resources: Record<string, TranslationResources> = {
  ru: {
    translation: translationRU,
  },
  en: {
    translation: {}, // Заглушка, пока нет EN-переводов
    // translation: translationEN, // Раскомментировать, когда добавятся EN-переводы
  },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'ru',
    fallbackLng: 'ru',
    interpolation: {
      escapeValue: false, // Не экранировать HTML в переводах
    },
  })
  .catch((err: Error) => {
    console.error('Ошибка инициализации i18n:', err);
  });

export default i18n;