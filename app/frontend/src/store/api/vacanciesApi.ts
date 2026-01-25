import { createApi, type BaseQueryFn } from '@reduxjs/toolkit/query/react';
import { popularVacancies, type VacancyCardProp } from '../../components/pages/home-page/api/data';

interface RequestOptions {
    url: string;
    method?: 'GET';
}

const mockBaseQuery: BaseQueryFn<
    RequestOptions,
    VacancyCardProp[],
    { status: number; data: string }
> = async ({ url }) => {
    await new Promise(resolve => setTimeout(resolve, 500)); 

    if (url === '/popular-vacancies') { 
        return { data: popularVacancies };
    }

    return {
        error: {
            status: 404,
            data: 'Not found',
        },
    };
};

export const vacanciesApi = createApi({
    reducerPath: 'vacanciesApi',
    baseQuery: mockBaseQuery,
    endpoints: (builder) => ({
        getPopularVacancies: builder.query<VacancyCardProp[], void>({ 
            query: () => ({ url: '/popular-vacancies', method: 'GET' }),
        }),
    }),
});

export const { 
    useGetPopularVacanciesQuery 
} = vacanciesApi;
