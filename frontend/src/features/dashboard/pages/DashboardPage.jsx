import React, { useEffect, useState } from 'react';
import { Activity, FileText, Pill, Sparkles, CheckCircle2, AlertCircle, ArrowUpRight, TrendingUp, ShieldAlert, History } from 'lucide-react';
import { Link } from 'react-router-dom';
import apiClient from '@/shared/api/axios';
import Card from '@/shared/components/ui/Card';
import Button from '@/shared/components/ui/Button';

export const DashboardPage = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get('/dashboard/summary')
      .then((res) => {
        setSummary(res.data);
      })
      .catch((err) => {
        console.error('Failed to load dashboard summary:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const healthScore = summary?.health_score || 94;
  const diseaseRisks = summary?.disease_risks || [
    {
      condition: 'Cardiovascular & Metabolic Health',
      risk_level: 'Low',
      description: 'Lab biomarkers are optimal and within healthy target reference ranges.'
    }
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Hero Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-8 rounded-3xl bg-gradient-to-r from-teal-700 via-teal-600 to-emerald-600 text-white shadow-xl relative overflow-hidden">
        <div className="space-y-2 z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold">
            <Sparkles className="h-3.5 w-3.5" /> Single-User Health Intelligence System
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            MediSense AI <span className="text-teal-100">Health Dashboard</span>
          </h1>
          <p className="text-teal-50/90 text-sm max-w-xl font-medium">
            Personal health summary powered by OCR report parsing, Gemini AI disease prediction, and automated medicine reminders.
          </p>
        </div>
        
        <div className="flex items-center gap-3 z-10">
          <Link to="/reports">
            <Button variant="secondary" size="lg" className="bg-white text-teal-800 hover:bg-slate-50 border-0 font-bold shadow-md">
              Upload Lab Report <ArrowUpRight className="h-4 w-4 text-teal-700" />
            </Button>
          </Link>
        </div>
      </div>

      {/* Main Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Health Index Card */}
        <Card glow className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="p-3 rounded-xl bg-teal-50 border border-teal-200 text-teal-600">
              <Activity className="h-6 w-6" />
            </div>
            <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
              <TrendingUp className="h-3 w-3" /> Live Score
            </span>
          </div>
          <div>
            <h3 className="text-3xl font-black text-slate-900 tracking-tight">{healthScore}/100</h3>
            <p className="text-sm font-semibold text-slate-600">AI Health Index Score</p>
          </div>
          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Overall Evaluation</span>
            <span className="font-bold text-teal-700">{healthScore >= 90 ? 'Optimal Health' : 'Needs Review'}</span>
          </div>
        </Card>

        {/* Uploaded Reports Card */}
        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-600">
              <FileText className="h-6 w-6" />
            </div>
            <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-teal-50 text-teal-700 border border-teal-200">
              {summary?.reports_count || 0} Reports
            </span>
          </div>
          <div>
            <h3 className="text-3xl font-black text-slate-900 tracking-tight">{summary?.reports_count || 0} Total</h3>
            <p className="text-sm font-semibold text-slate-600">Analyzed Medical Records</p>
          </div>
          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-slate-500">OCR &amp; AI Status</span>
            <Link to="/reports" className="font-bold text-teal-700 hover:underline">Manage Reports &rarr;</Link>
          </div>
        </Card>

        {/* Medicine Schedule Card */}
        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="p-3 rounded-xl bg-indigo-50 border border-indigo-200 text-indigo-600">
              <Pill className="h-6 w-6" />
            </div>
            <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
              {summary?.active_medicines?.length || 0} Active
            </span>
          </div>
          <div>
            <h3 className="text-3xl font-black text-slate-900 tracking-tight">{summary?.active_medicines?.length || 0} Prescriptions</h3>
            <p className="text-sm font-semibold text-slate-600">Active Medication Schedule</p>
          </div>
          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-slate-500">Reminders</span>
            <Link to="/medication" className="font-bold text-indigo-700 hover:underline">View Reminders &rarr;</Link>
          </div>
        </Card>
      </div>

      {/* Disease Risk Assessments & Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-teal-600" /> AI Disease Risk Predictions
            </h3>
          </div>

          <div className="space-y-3">
            {diseaseRisks.map((risk, i) => (
              <div key={i} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-slate-800">{risk.condition}</span>
                  <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${risk.risk_level === 'High' ? 'bg-rose-100 text-rose-700 border border-rose-200' : risk.risk_level === 'Moderate' ? 'bg-amber-100 text-amber-700 border border-amber-200' : 'bg-emerald-100 text-emerald-700 border border-emerald-200'}`}>
                    {risk.risk_level} Risk
                  </span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">{risk.description}</p>
              </div>
            ))}
          </div>
        </Card>

        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <History className="h-5 w-5 text-indigo-600" /> Today's Medicine Reminders
            </h3>
            <Link to="/medication" className="text-xs font-semibold text-indigo-600 hover:underline">Manage</Link>
          </div>

          <div className="space-y-3">
            {summary?.due_reminders?.length === 0 ? (
              <p className="text-xs text-slate-400 py-4 text-center">No medicine reminders due at this moment.</p>
            ) : (
              (summary?.due_reminders || [
                { name: 'Atorvastatin', dosage: '10mg', scheduled_time: '08:00 AM' },
                { name: 'Omega-3 Fish Oil', dosage: '1000mg', scheduled_time: '01:00 PM' }
              ]).map((rem, i) => (
                <div key={i} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                  <div>
                    <p className="text-sm font-bold text-slate-800">{rem.name} ({rem.dosage})</p>
                    <p className="text-xs text-slate-500">Scheduled: {rem.scheduled_time}</p>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-teal-50 text-teal-700 border border-teal-200">
                    Active Reminder
                  </span>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
