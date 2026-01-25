import { configureStore } from '@reduxjs/toolkit';
import { vacanciesApi } from './api/vacanciesApi';

export const store = configureStore({
    reducer: {
        [vacanciesApi.reducerPath]: vacanciesApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(vacanciesApi.middleware),
});