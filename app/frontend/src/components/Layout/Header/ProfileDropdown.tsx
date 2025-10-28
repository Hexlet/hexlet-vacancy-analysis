import { Menu, Tooltip } from '@mantine/core';
import { User as UserIcon, Settings, LogOut } from 'lucide-react';
import { router } from '@inertiajs/react';
import type { User } from '../../../types';

interface ProfileDropdownProps {
  user: User | null;
}

const ProfileDropdown = ({ user }: ProfileDropdownProps) => {
  const handleLogout = () => {
    router.post('/logout');
  };

  const goToProfile = () => router.get('/profile');
  const goToSettings = () => router.get('/settings');

  if (!user) {
    return null;
  }

  return (
    <Menu shadow="md" width={200} position="bottom-end">
      <Tooltip label={user.fullName} position="bottom" withArrow>
        <Menu.Target>
          <button className="flex items-center space-x-2 rounded-full p-1 transition hover:bg-gray-100">
            <img
              className="h-8 w-8 rounded-full object-cover"
              src={user.avatarUrl}
              alt="Аватар пользователя"
            />
            <span className="hidden md:inline text-sm font-medium text-gray-800">{user.name}</span>
          </button>
        </Menu.Target>
      </Tooltip>

      <Menu.Dropdown>
        <Menu.Label>Аккаунт</Menu.Label>
        <Menu.Item leftSection={<UserIcon size={14} />} onClick={goToProfile}>
          Профиль
        </Menu.Item>
        <Menu.Item leftSection={<Settings size={14} />} onClick={goToSettings}>
          Настройки
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item color="red" leftSection={<LogOut size={14} />} onClick={handleLogout}>
          Выход
        </Menu.Item>
      </Menu.Dropdown>
    </Menu>
  );
};

export default ProfileDropdown;
