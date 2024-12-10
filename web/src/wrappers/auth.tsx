import React from 'react';
import { Navigate, Outlet, useLocation } from '@umijs/max';

const Auth: React.FC = () => {
  const location = useLocation();
  const token = localStorage.getItem('access_token');

  if (!token) {
    return (
      <Navigate
        to="/user/login"
        replace
        state={{ from: location.pathname }}
      />
    );
  }

  return <Outlet />;
};

export default Auth;
