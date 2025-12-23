import { createApi, type BaseQueryFn } from '@reduxjs/toolkit/query/react';
import { plans, type Plan } from '../../components/pages/agency-pricing-page/api/data';

interface RequestOptions {
    url: string;
    method?: 'GET';
    body?: unknown;
}

const mockBaseQuery: BaseQueryFn<
    RequestOptions,
    Plan[],
    { status: number; data: string }
> = async ({ url }) => {
    await new Promise(resolve => setTimeout(resolve, 500)); 

    if (url === '/agency-plans') { 
        return { data: plans };
    }
    return {
        error: {
            status: 404,
            data: 'Not found',
        },
    };
};

export const plansApi = createApi({
    reducerPath: 'plansApi',
    baseQuery: mockBaseQuery,
    endpoints: (builder) => ({
        getAgencyPlans: builder.query<Plan[], void>({
            query: () => ({ url: '/agency-plans', method: 'GET' }),
        }),
    }),
});

export const { useGetAgencyPlansQuery } = plansApi;