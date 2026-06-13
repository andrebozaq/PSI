import React from 'react';
import { Navigate } from 'react-router';
import { useAuth } from '../../features/auth/contexts/AuthContext';

export const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return <div className="flex h-screen items-center justify-center">Cargando...</div>;
  }

  // Si no hay usuario, lo mandamos al login
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
