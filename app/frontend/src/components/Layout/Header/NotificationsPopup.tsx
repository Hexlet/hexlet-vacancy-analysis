import { useState, useEffect } from 'react';
import { Popover, Badge, Loader, Button, Text } from '@mantine/core';
import { Bell, AlertCircle } from 'lucide-react';
import { Link } from '@inertiajs/react';
import axios from 'axios';

interface Notification {
  id: string;
  text: string;
}

const NotificationsPopup = () => {
  const [count, setCount] = useState(0);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios.get('/api/notifications/count')
      .then(response => {
        setCount(response.data.count);
      })
      .catch(err => {
        console.error("Failed to fetch notification count:", err);
        setError('Ошибка');
      });
  }, []);

  const fetchNotifications = () => {
    if (notifications.length > 0) return;

    setIsLoading(true);
    setError(null);
    axios.get('/api/notifications?limit=5')
      .then(response => {
        setNotifications(response.data);
      })
      .catch(err => {
        console.error("Failed to fetch notifications:", err);
        setError('Ошибка загрузки уведомлений');
      })
      .finally(() => {
        setIsLoading(false);
      });
  };


  return (
    <Popover width={300} position="bottom-end" shadow="md">
      <Popover.Target>
        <button
          onClick={fetchNotifications}
          className="relative p-2 text-gray-500 rounded-full transition hover:bg-gray-100 hover:text-gray-700"
        >
          <Bell size={24} />
          {count > 0 && (
            <Badge color="red" variant="filled" size="xs" circle className="absolute top-1 right-1">
              {count}
            </Badge>
          )}
        </button>
      </Popover.Target>

      <Popover.Dropdown>
        <div className="flex justify-between items-center mb-2">
          <Text size="md" fw={500}>Уведомления</Text>
        </div>

        {isLoading && <div className="flex justify-center p-4"><Loader size="sm" /></div>}

        {error && <div className="text-red-500 p-4 text-center text-sm flex items-center gap-2"><AlertCircle size={16}/>{error}</div>}

        {!isLoading && !error && (
            notifications.length > 0 ? (
                <div className="flex flex-col gap-2">
                    {notifications.map(n => (
                        <div key={n.id} className="p-2 hover:bg-gray-50 rounded">
                           <Text size="sm">{n.text}</Text>
                        </div>
                    ))}
                </div>
            ) : (
                <Text size="sm" c="dimmed" ta="center" p="md">Нет новых уведомлений</Text>
            )
        )}

        <div className="border-t mt-2 pt-2">
          <Button component={Link} href="/notifications" variant="subtle" fullWidth>
            Все уведомления
          </Button>
        </div>
      </Popover.Dropdown>
    </Popover>
  );
};

export default NotificationsPopup;
