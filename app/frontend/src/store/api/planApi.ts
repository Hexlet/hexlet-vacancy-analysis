import { createApi, type BaseQueryFn } from '@reduxjs/toolkit/query/react';
import { plans, type Plan } from '../../components/pages/pricing-page/api/data';


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

    if (url === '/pricing-plans') {
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
        getPricingPlans: builder.query<Plan[], void>({
            query: () => ({ url: '/pricing-plans', method: 'GET' }),
        }),
    }),
});

export const { useGetPricingPlansQuery } = plansApi;