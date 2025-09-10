import React from 'react';
import Layout from '../Layout/Layout';

const DashboardPage = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold">Дашборд</h1>
      <p>Вы успешно вошли в систему!</p>
    </div>
  );
};

DashboardPage.layout = (page: React.ReactNode) => <Layout>{page}</Layout>;

export default DashboardPage;