import "vite/modulepreload-polyfill";
import { createRoot } from "react-dom/client";
import { createInertiaApp } from "@inertiajs/react";
import { InertiaProgress } from '@inertiajs/progress';
import axios from 'axios';
import React from 'react';
document.addEventListener('DOMContentLoaded', () => {

    const csrfToken = document.querySelector('meta[name=csrf-token]').getAttribute('content');
    axios.defaults.headers.common['X-CSRF-Token'] = csrfToken;

    InertiaProgress.init({ color: '#4B5563' });

    createInertiaApp({
        resolve: (name) => import(`./components/pages/${name}.tsx`),
        setup({ el, App, props }: {
            el: HTMLElement,
            App: React.ComponentType<{ page: any }>,
            props: any
        }) {
            const root = createRoot(el);
            root.render(<App {...props} />);
        },
    });

});
