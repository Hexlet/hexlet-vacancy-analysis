import { createRoot } from "react-dom/client";
import { createInertiaApp } from "@inertiajs/react";
import { InertiaProgress } from '@inertiajs/progress';
import axios from 'axios';
import React from 'react';

document.addEventListener('DOMContentLoaded', () => {
    const csrfMeta = document.querySelector('meta[name=csrf-token]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';
    axios.defaults.headers.common['X-CSRF-Token'] = csrfToken;

    InertiaProgress.init({ color: '#4B5563' });

    createInertiaApp({
        resolve: (name) => import(`./components/pages/${name}.tsx`),
        setup: ({ el, App, props }) => {
            const root = createRoot(el);
            root.render(React.createElement(App, props));
        },
    });
});
