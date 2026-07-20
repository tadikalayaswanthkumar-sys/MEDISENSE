import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import DashboardLayout from '../shared/components/layout/DashboardLayout';
import DashboardPage from '../features/dashboard/pages/DashboardPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <DashboardLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: 'reports',
        element: (
          <div className="p-8 glass-card rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-2">Medical Reports Module</h2>
            <p className="text-slate-400 text-sm">Upload, OCR extract, and AI summarize medical records.</p>
          </div>
        ),
      },
      {
        path: 'medication',
        element: (
          <div className="p-8 glass-card rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-2">Medication Tracker</h2>
            <p className="text-slate-400 text-sm">Schedule pill reminders and interaction safety alerts.</p>
          </div>
        ),
      },
      {
        path: 'analytics',
        element: (
          <div className="p-8 glass-card rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-2">Health Analytics</h2>
            <p className="text-slate-400 text-sm">Longitudinal trend analysis and AI risk assessments.</p>
          </div>
        ),
      },
      {
        path: 'profile',
        element: (
          <div className="p-8 glass-card rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-2">User Profile &amp; Settings</h2>
            <p className="text-slate-400 text-sm">Manage personal health profile, allergies, and permissions.</p>
          </div>
        ),
      },
    ],
  },
]);

export default router;
