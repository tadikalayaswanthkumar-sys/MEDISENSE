import React from 'react';
import { Activity, Bell, Search, ShieldCheck, LogOut } from 'lucide-react';
import { useAuthContext } from '@/app/providers';

export const Navbar = () => {
  const { user, logout } = useAuthContext() || {};

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-200/80 px-6 py-3 flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-xl bg-teal-600 flex items-center justify-center shadow-md shadow-teal-600/20">
          <Activity className="h-6 w-6 text-white stroke-[2.5]" />
        </div>
        <div>
          <span className="font-heading font-extrabold text-xl tracking-tight text-slate-900">
            MediSense <span className="text-teal-600 font-black">AI</span>
          </span>
          <span className="ml-2.5 px-2 py-0.5 text-[10px] font-bold tracking-wider uppercase bg-teal-50 text-teal-700 border border-teal-200 rounded-full">
            v1.0.0
          </span>
        </div>
      </div>

      <div className="hidden md:flex items-center max-w-md w-full mx-8">
        <div className="relative w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search medical records, insights, medications..."
            className="w-full bg-slate-100/80 border border-slate-200 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 transition-all"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 relative transition-colors">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-teal-500 ring-2 ring-white"></span>
        </button>

        <div className="h-6 w-px bg-slate-200"></div>

        <div className="flex items-center gap-3">
          <img
            src={user?.avatar || 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150'}
            alt="Profile"
            className="h-9 w-9 rounded-xl object-cover ring-2 ring-teal-500/30"
          />
          <div className="hidden sm:block text-left">
            <p className="text-sm font-bold text-slate-800 leading-tight">{user?.name || 'Dr. Alex Vance'}</p>
            <p className="text-xs text-teal-600 font-semibold flex items-center gap-1">
              <ShieldCheck className="h-3 w-3 inline text-teal-600" /> {user?.role || 'Verified MD'}
            </p>
          </div>

          <button
            onClick={logout}
            title="Sign Out"
            className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors ml-1"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
