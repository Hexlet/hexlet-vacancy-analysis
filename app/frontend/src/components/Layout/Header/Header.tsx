import { Link } from 'react-router-dom';
import logoSrc from '../../../assets/logo.png';

const Header = () => {
  return (
    <header className="bg-white shadow-md">
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/">
          <img src={logoSrc} alt="Логотип Skill Pulse" className="h-8 w-auto" />
        </Link>
        <div>
          <Link to="/login" className="text-gray-600 hover:text-blue-500 mx-2">Войти</Link>
          <Link to="/register" className="text-gray-600 hover:text-blue-500 mx-2">Регистрация</Link>
        </div>
      </nav>
    </header>
  );
};

export default Header;