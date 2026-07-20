export const ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    ME: '/auth/me',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
  },
  REPORTS: {
    BASE: '/reports',
    UPLOAD: '/reports/upload',
    BY_ID: (id) => `/reports/${id}`,
  },
  MEDICATION: {
    BASE: '/medication',
    HISTORY: '/medication/history',
    LOG: (id) => `/medication/${id}/log`,
  },
  DASHBOARD: {
    SUMMARY: '/dashboard/summary',
  },
};

export default ENDPOINTS;
