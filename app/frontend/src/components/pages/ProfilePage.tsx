import React from 'react';
import Layout from '../Layout/Layout';

const ProfilePage = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold">Профиль</h1>
    </div>
  );
};

ProfilePage.layout = (page: React.ReactNode) => <Layout>{page}</Layout>;

export default ProfilePage;