import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import DashboardLayout from '@/shared/components/layout/DashboardLayout';
import AuthLayout from '@/shared/components/layout/AuthLayout';
import DashboardPage from '@/features/dashboard/pages/DashboardPage';
import LoginPage from '@/features/authentication/pages/LoginPage';
import RegisterPage from '@/features/authentication/pages/RegisterPage';
import { useAuthContext } from '@/app/providers';

const ProtectedRoute = ({ children }) => {
  const { token, loading } = useAuthContext();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-600">
        <div className="flex items-center gap-2 font-semibold text-sm">
          <div className="h-4 w-4 rounded-full border-2 border-teal-600 border-t-transparent animate-spin"></div>
          Verifying MediSense Authentication...
        </div>
      </div>
    );
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: 'reports',
        element: (
          <div className="p-8 glass-card rounded-2xl bg-white border border-slate-200">
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Medical Reports Module</h2>
            <p className="text-slate-600 text-sm">Upload, OCR extract, and AI summarize medical records.</p>
          </div>
        ),
      },
      {
        path: 'medication',
        element: (
          <div className="p-8 glass-card rounded-2xl bg-white border border-slate-200">
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Medication Tracker</h2>
            <p className="text-slate-600 text-sm">Schedule pill reminders and interaction safety alerts.</p>
          </div>
        ),
      },
      {
        path: 'analytics',
        element: (
          <div className="p-8 glass-card rounded-2xl bg-white border border-slate-200">
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Health Analytics</h2>
            <p className="text-slate-600 text-sm">Longitudinal trend analysis and AI risk assessments.</p>
          </div>
        ),
      },
      {
        path: 'profile',
        element: (
          <div className="p-8 glass-card rounded-2xl bg-white border border-slate-200">
            <h2 className="text-2xl font-bold text-slate-900 mb-2">User Profile &amp; Settings</h2>
            <p className="text-slate-600 text-sm">Manage personal health profile, allergies, and permissions.</p>
          </div>
        ),
      },
    ],
  },
  {
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'register',
        element: <RegisterPage />,
      },
    ],
  },
]);

export default router;
