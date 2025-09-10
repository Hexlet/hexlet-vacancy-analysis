import './index.css';
import React from 'react';
import { createRoot } from 'react-dom/client';
import { createInertiaApp } from '@inertiajs/react';
import { InertiaProgress } from '@inertiajs/progress';

type PageModule = {
  default: React.ComponentType & { layout?: (page: React.ReactNode) => React.ReactNode };
};

InertiaProgress.init({ color: '#4B5563' });

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob<PageModule>('./pages/**/*.tsx', { eager: true });
    const pageModule = pages[`./pages/${name}.tsx`];

    if (!pageModule) {
      throw new Error(`Unknown page ${name}.`);
    }

    const page = pageModule.default;

    page.layout = page.layout || ((page: React.ReactNode) => page);

    return page;
  },

  setup({ el, App, props }) {
    createRoot(el).render(<App {...props} />);
  },
});