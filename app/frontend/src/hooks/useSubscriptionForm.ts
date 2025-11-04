import { useState } from 'react';

export const useSubscriptionForm = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setMessage('');

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setStatus('error');
      setMessage('Пожалуйста, введите корректный e-mail.');
      return;
    }

    try {
      const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        if (email.includes('error@')) {
          throw new Error('Данный e-mail уже используется.');
        }
        throw new Error('Ошибка сервера. Попробуйте позже.');
      }

      setStatus('success');
      setMessage('Спасибо за подписку!');
      setEmail('');
    } catch (error) {
      setStatus('error');
      setMessage(error instanceof Error ? error.message : 'Произошла неизвестная ошибка.');
    }
  };

  return {
    email,
    setEmail,
    status,
    message,
    handleSubmit,
  };
};
