import React from 'react';
import { Outlet } from 'react-router-dom';
import { Activity, ShieldCheck, Sparkles } from 'lucide-react';

export const AuthLayout = () => {
  return (
    <div className="min-h-screen flex bg-slate-50 text-slate-800">
      {/* Left Branding Hero Section */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-teal-700 via-teal-600 to-emerald-700 p-12 text-white flex-col justify-between relative overflow-hidden">
        <div className="absolute -right-20 -bottom-20 w-96 h-96 bg-white/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -left-20 -top-20 w-96 h-96 bg-emerald-400/20 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex items-center gap-3 z-10">
          <div className="h-11 w-11 rounded-2xl bg-white text-teal-700 flex items-center justify-center shadow-lg">
            <Activity className="h-7 w-7 stroke-[2.5]" />
          </div>
          <span className="font-heading font-extrabold text-2xl tracking-tight text-white">
            MediSense <span className="text-teal-200">AI</span>
          </span>
        </div>

        <div className="space-y-6 max-w-lg z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 border border-white/30 text-xs font-bold text-teal-100">
            <Sparkles className="h-4 w-4 text-teal-200" /> Next-Gen Health Intelligence Platform
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight leading-tight text-white">
            AI-Driven Medical Analysis &amp; Diagnostic Insights
          </h1>
          <p className="text-teal-50/90 text-base leading-relaxed">
            Securely upload medical lab reports, track prescription adherence, and obtain real-time diagnostic summaries powered by Gemini Medical AI.
          </p>

          <div className="pt-4 grid grid-cols-2 gap-4 text-xs font-semibold">
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md p-3.5 rounded-xl border border-white/20">
              <ShieldCheck className="h-5 w-5 text-teal-200" /> HIPAA Compliant Encryption
            </div>
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md p-3.5 rounded-xl border border-white/20">
              <Sparkles className="h-5 w-5 text-teal-200" /> Automated OCR Lab Parsing
            </div>
          </div>
        </div>

        <div className="text-xs text-teal-100/80 font-medium z-10">
          &copy; {new Date().getFullYear()} MediSense AI. All rights reserved.
        </div>
      </div>

      {/* Right Form Container */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 md:p-12">
        <div className="w-full max-w-md">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
