import { configureStore } from '@reduxjs/toolkit';
import { plansApi } from './api/plansApi';

export const store = configureStore({
    reducer: {
        [plansApi.reducerPath]: plansApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(plansApi.middleware),
});