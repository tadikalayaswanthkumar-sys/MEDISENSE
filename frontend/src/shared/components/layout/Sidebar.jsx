import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, Pill, BarChart3, User, Settings, Sparkles } from 'lucide-react';

export const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Medical Reports', path: '/reports', icon: FileText },
    { name: 'Medication', path: '/medication', icon: Pill },
    { name: 'Analytics', path: '/analytics', icon: BarChart3 },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  return (
    <aside className="w-64 glass-panel border-r border-slate-200/80 p-4 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-65px)]">
      <div className="space-y-6">
        <div className="px-3 py-2 text-xs font-bold uppercase tracking-wider text-slate-400">
          Main Navigation
        </div>
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 ${
                    isActive
                      ? 'bg-teal-50 text-teal-700 border border-teal-200 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`
                }
              >
                <Icon className="h-4 w-4" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      <div className="space-y-4">
        {/* AI Engine Status Card - Light theme */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-teal-50/80 via-emerald-50/50 to-white border border-teal-200/80 shadow-sm">
          <div className="flex items-center gap-2 text-teal-700 font-bold text-xs mb-1">
            <Sparkles className="h-4 w-4 text-teal-600" /> Gemini Medical AI
          </div>
          <p className="text-xs text-slate-600 leading-relaxed mb-3">
            Real-time report analysis &amp; health scoring active.
          </p>
          <div className="flex items-center justify-between text-[11px]">
            <span className="flex items-center gap-1.5 text-emerald-600 font-semibold">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span> Live Engine
            </span>
            <span className="font-mono text-slate-500">v2.5 Flash</span>
          </div>
        </div>

        <button className="flex items-center gap-3 w-full px-3.5 py-2.5 rounded-xl text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors">
          <Settings className="h-4 w-4 text-slate-500" />
          <span>System Settings</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
