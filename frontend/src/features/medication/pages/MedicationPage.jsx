import React, { useState, useEffect } from 'react';
import { Pill, Plus, CheckCircle2, XCircle, Clock, AlertCircle, History } from 'lucide-react';
import apiClient from '@/shared/api/axios';
import Card from '@/shared/components/ui/Card';
import Button from '@/shared/components/ui/Button';

export const MedicationPage = () => {
  const [medicines, setMedicines] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [name, setName] = useState('');
  const [dosage, setDosage] = useState('');
  const [frequency, setFrequency] = useState('Once Daily');
  const [time, setTime] = useState('08:00 AM');
  const [instructions, setInstructions] = useState('');

  const fetchData = async () => {
    try {
      const [medRes, histRes] = await Promise.all([
        apiClient.get('/medication/'),
        apiClient.get('/medication/history')
      ]);
      setMedicines(medRes.data);
      setHistory(histRes.data);
    } catch (err) {
      console.error('Failed to fetch medication data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddMedicine = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/medication/', {
        name,
        dosage,
        frequency,
        times: [time],
        instructions
      });
      setName('');
      setDosage('');
      setInstructions('');
      setShowAddModal(false);
      fetchData();
    } catch (err) {
      console.error('Failed to add medicine:', err);
    }
  };

  const handleLogReminder = async (medId, status) => {
    try {
      await apiClient.post(`/medication/${medId}/log`, { status });
      fetchData();
    } catch (err) {
      console.error('Failed to log reminder status:', err);
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-8 rounded-3xl bg-gradient-to-r from-teal-700 via-teal-600 to-emerald-600 text-white shadow-xl">
        <div className="space-y-2">
          <h1 className="text-3xl font-extrabold tracking-tight">Medication Reminders</h1>
          <p className="text-teal-50/90 text-sm max-w-xl font-medium">
            Schedule prescription reminders, log adherence, and track daily pill history.
          </p>
        </div>
        <Button onClick={() => setShowAddModal(true)} variant="secondary" className="bg-white text-teal-800 hover:bg-slate-50 font-bold border-0 shadow-md">
          <Plus className="h-4 w-4" /> Add Prescription
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Prescriptions List */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Pill className="h-5 w-5 text-teal-600" /> Active Prescriptions
          </h2>

          {loading ? (
            <div className="p-8 text-center text-slate-500 font-medium">Loading prescriptions...</div>
          ) : medicines.length === 0 ? (
            <Card className="text-center py-12 space-y-3">
              <Pill className="h-10 w-10 text-slate-300 mx-auto" />
              <p className="text-slate-600 font-semibold text-sm">No active prescriptions set up.</p>
              <Button onClick={() => setShowAddModal(true)} variant="outline" size="sm">
                Add Your First Medicine
              </Button>
            </Card>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {medicines.map((med) => (
                <Card key={med.id} className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-base">{med.name}</h3>
                      <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200">
                        {med.dosage}
                      </span>
                    </div>
                    <span className="text-xs font-semibold text-slate-500 flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5 text-teal-600" /> {med.times?.join(', ')}
                    </span>
                  </div>

                  {med.instructions && (
                    <p className="text-xs text-slate-500 bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                      {med.instructions}
                    </p>
                  )}

                  <div className="pt-2 flex items-center gap-2">
                    <Button onClick={() => handleLogReminder(med.id, 'Taken')} size="sm" variant="primary" className="flex-1 text-xs font-bold">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Mark Taken
                    </Button>
                    <Button onClick={() => handleLogReminder(med.id, 'Skipped')} size="sm" variant="secondary" className="text-xs font-bold text-slate-600">
                      <XCircle className="h-3.5 w-3.5 text-rose-500" /> Skip
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Reminder History Log */}
        <Card className="lg:col-span-1 space-y-6">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <History className="h-5 w-5 text-teal-600" /> Adherence History Log
          </h2>

          {history.length === 0 ? (
            <p className="text-xs text-slate-400 py-4 text-center">No pill adherence logged today.</p>
          ) : (
            <div className="space-y-3">
              {history.map((log) => (
                <div key={log.id} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                  <div>
                    <p className="font-bold text-slate-800">{log.medicine_name}</p>
                    <p className="text-[11px] text-slate-400">{new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                  </div>
                  <span className={`font-bold px-2 py-0.5 rounded-md ${log.status === 'Taken' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'}`}>
                    {log.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* Add Prescription Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fadeIn">
          <div className="bg-white max-w-md w-full rounded-3xl p-6 sm:p-8 space-y-6 border border-slate-200 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <h3 className="text-xl font-bold text-slate-900">Add New Prescription</h3>
              <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-slate-700 font-bold">✕</button>
            </div>

            <form onSubmit={handleAddMedicine} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Medicine Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Atorvastatin"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 focus:outline-none focus:bg-white focus:border-teal-500 font-medium"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Dosage</label>
                <input
                  type="text"
                  required
                  value={dosage}
                  onChange={(e) => setDosage(e.target.value)}
                  placeholder="e.g. 10mg"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 focus:outline-none focus:bg-white focus:border-teal-500 font-medium"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Frequency</label>
                  <select
                    value={frequency}
                    onChange={(e) => setFrequency(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 text-sm text-slate-800 font-medium"
                  >
                    <option value="Once Daily">Once Daily</option>
                    <option value="Twice Daily">Twice Daily</option>
                    <option value="As Needed">As Needed</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Scheduled Time</label>
                  <input
                    type="text"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                    placeholder="08:00 AM"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 text-sm text-slate-800 font-medium"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Instructions (Optional)</label>
                <input
                  type="text"
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  placeholder="e.g. Take with food"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 font-medium"
                />
              </div>

              <Button type="submit" className="w-full py-3 font-bold shadow-md">
                Save Medicine Reminder
              </Button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicationPage;
