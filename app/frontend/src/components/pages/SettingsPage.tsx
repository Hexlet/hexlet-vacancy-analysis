import React from 'react';
import Layout from '../Layout/Layout';

const SettingsPage = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold">Настройки</h1>
    </div>
  );
};

SettingsPage.layout = (page: React.ReactNode) => <Layout>{page}</Layout>;

export default SettingsPage;
