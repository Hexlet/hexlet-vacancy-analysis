// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});

// Экспортируем типы
export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;