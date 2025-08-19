import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux'
import { I18nextProvider } from 'react-i18next';
import './index.css'
import App from './App.tsx'
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import { store } from '../store/store.ts'
import i18n from './Locales/i18n';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <I18nextProvider i18n={i18n}>
        <MantineProvider> 
          <App />
        </MantineProvider>
      </I18nextProvider>
    </Provider>
  </React.StrictMode>,
)