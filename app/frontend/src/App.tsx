import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Layout/Header/Header';
import Footer from './components/Layout/Footer/Footer';

import HomePage from './components/pages/HomePage';
import CareersPage from './components/pages/CareersPage';
import PartnersPage from './components/pages/PartnersPage';
import FaqPage from './components/pages/FaqPage';
import ReviewsPage from './components/pages/ReviewsPage';
import ContactsPage from './components/pages/ContactsPage';
import GdprPage from './components/pages/GdprPage';
import PrivacyPolicyPage from './components/pages/PrivacyPolicyPage';
import LoginPage from './components/pages/LoginPage';
import RegisterPage from './components/pages/RegisterPage';

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow ">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/careers" element={<CareersPage />} />
            <Route path="/partners" element={<PartnersPage />} />
            <Route path="/faq" element={<FaqPage />} />
            <Route path="/reviews" element={<ReviewsPage />} />
            <Route path="/contacts" element={<ContactsPage />} />
            <Route path="/gdpr" element={<GdprPage />} />
            <Route path="/policy" element={<PrivacyPolicyPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App
