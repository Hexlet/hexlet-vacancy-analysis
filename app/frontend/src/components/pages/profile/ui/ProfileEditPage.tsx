import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import type { FormValues } from '../model/types'

const testUser = {
  name: 'Константин',
  lastName: 'Шаган',
  email: 'konstantinshagan@gmail.com',
  // phoneNumber: '+7 (123) 456-45-45',
  subscriptions: {
    isPro: true,
    validTill: '01.06.2008',
  },
  notifications: {
    newFilteredVacancies: true,
    weeklyAnalytics: false,
    newsAndUpdates: true,
  }
}

export const ProfileEditPage: React.FC = () => {
  const [isProfileSubmitting, setIsProfileSubmitting] = useState(false);
  const [isNotificationsSubmitting, setIsNotificationsSubmitting] = useState(false);

  // https://https://react-hook-form.com/docs/useform
  const { register, handleSubmit, setValue, formState: { errors } } = useForm<FormValues>({
    mode: 'onTouched',
    reValidateMode: 'onChange',
    defaultValues: {
      name: testUser.name,
      lastName: testUser.lastName,
      email: testUser.email,
      // phoneNumber: testUser.phoneNumber,
    },
  })

  // Состояние для чекбоксов с уведомлениями
  const [notifications, setNotifications] = useState({
    newFilteredVacancies: testUser.notifications.newFilteredVacancies,
    weeklyAnalytics: testUser.notifications.weeklyAnalytics,
    newsAndUpdates: testUser.notifications.newsAndUpdates,
    // Потом взять юзера с бэка вместо тестового
  })

  // Временный сабмит персональный данных
  const onSubmitProfile = async ( data: FormValues) => {
    setIsProfileSubmitting(true)
    console.log('Changed creds:', data)

    setTimeout(() => {
      setIsProfileSubmitting(false);
      console.log('Creds has been updated')
    }, 1000)
    // После интеграции с Инерцией подставить данные с бэка
  }

  // Временный сабмит уведомления для чекбоксов
  const onSubmitNotifications = async () => {
    setIsNotificationsSubmitting(true);
    console.log('amended')

    setTimeout(() => {
      setIsNotificationsSubmitting(false);
      console.log('Notificateions successfully amended')
    }, 1000)
    // После интеграции с Инерцией подставить данные с бэка
  }

  // Хэндлер для изменения чекбоксов с уведомлениями
  // Принимает ключ с типом, который берет тип значения из notifications
  // Распаковывает объект спредом и заменяет значение ключа на противоположное 
  const handleNotificationChange = (key: keyof typeof notifications) => {
    setNotifications((prev) => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  return (
    <div className='bg-gray-100 max-w-4xl mx-auto p-6 mt-1 space-y-8'>
      {/* Header */}
      <header className='border-gray-200 pb-2'>
        <h1 className='text-2xl font-bold text-gray-900'>Профиль пользователя</h1>
      </header>

      {/* Personal data */}
      <section className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>
        <h2 className='text-2xl font-bold mb-6 text-gray-900'>Персональные данные</h2>

        <form onSubmit={handleSubmit(onSubmitProfile)}>
          <div className='flex flex-col gap-6'>
            {/* Имя */}
            <div>
              <label htmlFor="name" className='block text-sm font-medium text-gray-700 mb-1'>Имя</label>
              <input 
                id="name" 
                type="text" 
                className={
                  `bg-gray-100 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 
                   ${errors.name ? 'border-red-500 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}`
                }
                placeholder='Введите имя'
                {...register('name', {
                  required: 'Введите имя',
                  minLength: {
                    value: 2,
                    message: 'Имя должно содержать минимум 2 буквы'
                  },
                })}
                />
                {errors.name && (
                  <p className='mt-1 text-sm text-red-600'>{errors.name.message}</p>
                )}
            </div>
            {/* Фамилия */}
            <div>
              <label htmlFor="lastName" className='block text-sm font-medium text-gray-700 mb-1'>Фамилия</label>
              <input 
                id="lastName" 
                type="text" 
                className={
                  `bg-gray-100 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 
                   ${errors.lastName ? 'border-red-500 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}`
                }
                placeholder='Введите фамилию'
                {...register('lastName', {
                  required: 'Введите фамилию',
                  minLength: {
                    value: 2,
                    message: 'Фамилия должна содержать минимум 2 буквы'
                  },
                })}
                />
                {errors.lastName && (
                  <p className='mt-1 text-sm text-red-600'>{errors.lastName.message}</p>
                )}
            </div>
            {/* Email */}
            <div>
              <label htmlFor="email" className='block text-sm font-medium text-gray-700 mb-1'>Email</label>
              <input 
                id="email" 
                type="email" 
                className={
                  `bg-gray-100 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 
                   ${errors.email ? 'border-red-500 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}`
                }
                placeholder='Введите email'
                {...register('email', {
                  required: 'Введите email',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Некорректный email'
                  },
                })}
                />
                {errors.email && (
                  <p className='mt-1 text-sm text-red-600'>{errors.email.message}</p>
                )}
            </div>
            {/* Телефон */}
            <div>
              <label htmlFor="phoneNumber" className='block text-sm font-medium text-gray-700 mb-1'>Телефон</label>
              <input 
                id="phoneNumber" 
                type="tel" 

                // РАСКОММЕНТИРОВАТЬ, КОГДА НА БЭКЕ ПОЯВИТСЯ СООТВЕТСТВУЮЩЕЕ ПОЛЕ 

                // className={
                //   `bg-gray-100 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 
                //    {${errors.phoneNumber ? 'border-red-500 focus:border-red-500 focus:ring-red-200' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}}`
                // }
                className='bg-gray-100 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 '
                placeholder='Введите номер телефона'
                // {...register('phoneNumber', {
                //   required: 'Введите номер телефона',
                //   pattern: {
                //     value: /^\+?[0-9\s\-\(\)]{10,20}$/,
                //     message: 'Некорректный формат телефона'
                //   },
                // })}
                />
                {/* {errors.phoneNumber && (
                  <p className='mt-1 text-sm text-red-600'>{errors.phoneNumber.message}</p>
                )} */}

            </div>
            {/* Кнопка отправки изменений */}         
            <button
              type='submit'
              disabled={isProfileSubmitting}
              className='w-fit text-white px-6 py-2 rounded-md hover:cursor-pointer disabled:cursor-not-allowed font-bold bg-[#20B0B4]'
            >
              {isProfileSubmitting ? 'Сохранение изменений...' : 'Сохранить изменения'}
            </button>
          </div>
        </form>
      </section>
      {/* Подписка и уведомления */}
      <section className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>
        <h2 className='text-2xl font-bold mb-6 text-gray-900'>Подписка и уведомления</h2>
        {/* Текущий план */}
        <div className='rounded-lg p-5 mb-6 bg-[#ECF7F7]'>
          <div className='flex justify-between items-start'>
            <div>
              <h3 className='text-lg font-medium text-gray-800 mb-1'>Текущий план</h3>
              <p className='text-sm font-semibold text-gray-600 mb-1'>Действует до {testUser.subscriptions.validTill}</p>
            </div>
          {testUser.subscriptions.isPro && (
            <div className='inline-flex items-center px-4 py-0.5 rounded-full bg-[#20B0B4]'>
              <span className="text-white font-semibold">Pro</span>
            </div>
          )}
          </div>
        </div>
        {/* Почтовые уведомления */}
        <div>
          <h3 className='text-lg font-medium text-gray-800 mb-3'>Почтовые уведомления</h3>
            <form onSubmit={onSubmitNotifications}>
              <div className='space-y-3'>
                <label className='flex items-center space-x-3 cursor-pointer'>
                  <input 
                    type="checkbox"
                    checked={testUser.notifications.newFilteredVacancies}
                    onChange={() => handleNotificationChange('newFilteredVacancies')}
                    />
                    <span className='font-semibold text-gray-800'>Новые вакансии по фильтрам</span>
                </label>
                <label className='flex items-center space-x-3 cursor-pointer'>
                  <input 
                    type="checkbox"
                    checked={testUser.notifications.weeklyAnalytics}
                    onChange={() => handleNotificationChange('weeklyAnalytics')}
                    />
                    <span className='font-semibold text-gray-800'>Еженедельная аналитика</span>
                </label>
                <label className='flex items-center space-x-3 cursor-pointer mb-4'>
                  <input 
                    type="checkbox"
                    checked={testUser.notifications.newsAndUpdates}
                    onChange={() => handleNotificationChange('newsAndUpdates')}
                    />
                    <span className='font-semibold text-gray-800'>Новости и обновления</span>
                </label>
              </div>
              {/* Кнопка отправки изменений */}         
              <button
                type='submit'
                disabled={isNotificationsSubmitting}
                style={{ backgroundColor: '#20B0B4' }}
                className='w-fit text-white px-6 py-2 rounded-md hover:cursor-pointer disabled:cursor-not-allowed font-bold'
              >
                {isNotificationsSubmitting ? 'Сохранение изменений...' : 'Сохранить изменения'}
              </button>
            </form>
        </div>
      </section>
    </div>
  )
}
