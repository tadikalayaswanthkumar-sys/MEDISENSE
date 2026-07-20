import React, { useEffect, useState } from 'react';
import { Activity, FileText, Pill, Sparkles, CheckCircle2, AlertCircle, ArrowUpRight, TrendingUp } from 'lucide-react';
import Card from '@/shared/components/ui/Card';
import Button from '@/shared/components/ui/Button';

export const DashboardPage = () => {
  const [backendStatus, setBackendStatus] = useState({ loading: true, status: 'checking', service: '' });

  useEffect(() => {
    fetch('/api/v1/health')
      .then((res) => res.json())
      .then((data) => {
        setBackendStatus({ loading: false, status: data.status, service: data.service });
      })
      .catch(() => {
        setBackendStatus({ loading: false, status: 'offline', service: 'MediSense FastAPI Backend' });
      });
  }, []);

  const healthMetrics = [
    { title: 'AI Health Index', value: '94/100', status: 'Optimal', change: '+3.2%', icon: Activity, color: 'text-teal-600 bg-teal-50 border-teal-200' },
    { title: 'Medical Reports', value: '18 Analyzed', status: 'All Clear', change: '2 New', icon: FileText, color: 'text-emerald-600 bg-emerald-50 border-emerald-200' },
    { title: 'Active Medications', value: '3 Prescriptions', status: 'On Schedule', change: '100% Adherence', icon: Pill, color: 'text-indigo-600 bg-indigo-50 border-indigo-200' },
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header Banner - Pleasant light gradient */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-8 rounded-3xl bg-gradient-to-r from-teal-700 via-teal-600 to-emerald-600 text-white shadow-xl shadow-teal-700/10 relative overflow-hidden">
        <div className="space-y-2 z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md border border-white/30 text-white text-xs font-bold">
            <Sparkles className="h-3.5 w-3.5" /> Phase 1 Setup Verified &amp; Operational
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            MediSense AI <span className="text-teal-100">Health Command Center</span>
          </h1>
          <p className="text-teal-50/90 text-sm max-w-xl font-medium">
            Integrated diagnostic insights, automated report OCR parsing, and personalized medical recommendation engine powered by Gemini AI.
          </p>
        </div>
        
        <div className="flex items-center gap-3 z-10">
          <Button variant="secondary" size="lg" className="bg-white text-teal-800 hover:bg-slate-50 border-0 font-bold shadow-md">
            Upload Medical Report <ArrowUpRight className="h-4 w-4 text-teal-700" />
          </Button>
        </div>
      </div>

      {/* Backend API Connection Status Widget */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-white border border-slate-200/90 shadow-sm border-l-4 border-l-teal-600">
        <div className="flex items-center gap-3">
          {backendStatus.status === 'healthy' ? (
            <CheckCircle2 className="h-5 w-5 text-emerald-600" />
          ) : (
            <AlertCircle className="h-5 w-5 text-amber-500 animate-pulse" />
          )}
          <div>
            <p className="text-sm font-bold text-slate-800">
              Backend Status: <span className="capitalize text-teal-700">{backendStatus.status}</span>
            </p>
            <p className="text-xs text-slate-500">
              FastAPI service running on <code className="text-slate-700 font-mono bg-slate-100 px-1.5 py-0.5 rounded">http://localhost:8000</code>
            </p>
          </div>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded-lg bg-teal-50 border border-teal-200 text-teal-700 font-semibold">
          CORS &amp; REST Active
        </span>
      </div>

      {/* Metrics Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {healthMetrics.map((metric, idx) => {
          const Icon = metric.icon;
          return (
            <Card key={idx} glow={idx === 0}>
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-xl border ${metric.color}`}>
                  <Icon className="h-6 w-6" />
                </div>
                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                  <TrendingUp className="h-3 w-3" /> {metric.change}
                </span>
              </div>
              <h3 className="text-2xl font-extrabold text-slate-900 tracking-tight mb-1">{metric.value}</h3>
              <p className="text-sm text-slate-600 font-semibold">{metric.title}</p>
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span>Status</span>
                <span className="text-slate-700 font-bold">{metric.status}</span>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Recent Activity & Modules */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <FileText className="h-5 w-5 text-teal-600" /> Recent Medical Reports
            </h3>
            <span className="text-xs text-teal-700 font-semibold hover:underline cursor-pointer">View All</span>
          </div>

          <div className="space-y-3">
            {[
              { name: 'Comprehensive Blood Panel.pdf', date: 'Yesterday, 4:30 PM', status: 'Parsed & Verified', score: 'Normal' },
              { name: 'Lipid Profile & Glucose.pdf', date: '15 Jul 2026', status: 'AI Analyzed', score: 'Optimal' },
              { name: 'Thyroid Stimulating Hormone.pdf', date: '02 Jul 2026', status: 'AI Analyzed', score: 'Stable' }
            ].map((report, i) => (
              <div key={i} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-slate-300 transition-colors">
                <div>
                  <p className="text-sm font-bold text-slate-800">{report.name}</p>
                  <p className="text-xs text-slate-500">{report.date}</p>
                </div>
                <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-teal-50 text-teal-700 border border-teal-200">
                  {report.status}
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Pill className="h-5 w-5 text-indigo-600" /> Daily Medication Reminder
            </h3>
            <span className="text-xs text-indigo-600 font-semibold hover:underline cursor-pointer">Manage</span>
          </div>

          <div className="space-y-3">
            {[
              { name: 'Atorvastatin - 10mg', time: '08:00 AM', status: 'Taken' },
              { name: 'Omega-3 Fish Oil - 1000mg', time: '01:00 PM', status: 'Taken' },
              { name: 'Metformin - 500mg', time: '08:00 PM', status: 'Scheduled' }
            ].map((med, i) => (
              <div key={i} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-slate-300 transition-colors">
                <div>
                  <p className="text-sm font-bold text-slate-800">{med.name}</p>
                  <p className="text-xs text-slate-500">{med.time}</p>
                </div>
                <span className={`text-xs font-bold px-2.5 py-1 rounded-lg ${med.status === 'Taken' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}`}>
                  {med.status}
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
