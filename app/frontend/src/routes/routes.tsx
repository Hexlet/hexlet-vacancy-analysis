import React from 'react';
import { Route, Routes } from 'react-router-dom';

import HomePage from '../components/pages/HomePage';
import CareersPage from '../components/pages/CareersPage';
import PartnersPage from '../components/pages/PartnersPage';
import FaqPage from '../components/pages/FaqPage';
import ReviewsPage from '../components/pages/ReviewsPage';
import ContactsPage from '../components/pages/ContactsPage';
import GdprPage from '../components/pages/GdprPage';
import PrivacyPolicyPage from '../components/pages/PrivacyPolicyPage';
import LoginPage from '../components/pages/LoginPage';
import RegisterPage from '../components/pages/RegisterPage';

const routes = [
  { path: '/', element: <HomePage /> },
  { path: '/careers', element: <CareersPage /> },
  { path: '/partners', element: <PartnersPage /> },
  { path: '/faq', element: <FaqPage /> },
  { path: '/reviews', element: <ReviewsPage /> },
  { path: '/contacts', element: <ContactsPage /> },
  { path: '/gdpr', element: <GdprPage /> },
  { path: '/policy', element: <PrivacyPolicyPage /> },
  { path: '/login', element: <LoginPage /> },
  { path: '/register', element: <RegisterPage /> },
];

export const renderRoutes = (): React.ReactNode => {
  return (
    <Routes>
      {routes.map((route, index) => (
        <Route
          key={index}
          path={route.path}
          element={route.element}
        />
      ))}
    </Routes>
  );
};

export default routes;