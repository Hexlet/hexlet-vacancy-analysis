import { Link, usePage } from '@inertiajs/react';
import { useMediaQuery } from '@mantine/hooks';
import { Search, Menu } from 'lucide-react';
import logoSrc from '../../../assets/logo.png';
import ProfileDropdown from './ProfileDropdown';
import NotificationsPopup from './NotificationsPopup';
import type { User } from '../../../types';
import type { PageProps as InertiaPageProps } from '@inertiajs/core';

interface PageProps extends InertiaPageProps {
  auth: {
    user: User;
  };
}

const Header = () => {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const { auth: { user } } = usePage<PageProps>().props;

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:p-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            {isMobile && <button className="mr-4"><Menu size={24} /></button>}
            <Link href="/dashboard">
              <img src={logoSrc} alt="Логотип" className="h-8 w-auto" />
            </Link>
          </div>
          <div className="flex items-center gap-2 sm:gap-4">
            {isMobile && <button><Search size={22} /></button>}
            <NotificationsPopup />
            <ProfileDropdown user={user} />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
