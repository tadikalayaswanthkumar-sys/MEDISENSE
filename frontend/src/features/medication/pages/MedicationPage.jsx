import React, { useState, useEffect, useRef } from 'react';
import { Pill, Plus, CheckCircle2, XCircle, Clock, Bell, Volume2, History, Trash2, BellRing, AlertTriangle } from 'lucide-react';
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
  const [time, setTime] = useState('08:00'); // 24-hr time input format
  const [instructions, setInstructions] = useState('');

  // Active Alarm State
  const [activeAlarm, setActiveAlarm] = useState(null); // { medicine, triggerTime }
  const audioCtxRef = useRef(null);
  const triggeredAlarmsRef = useRef(new Set()); // Prevents double ringing in same minute

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
    // Request notification permission if supported
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  // Web Audio API Synthesizer Alarm Sound Chime
  const playAlarmChime = () => {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;

      const ctx = new AudioContext();
      audioCtxRef.current = ctx;

      // Play 4 rhythmic alarm beeps (high clarity 880Hz / A5 chime)
      const times = [0, 0.25, 0.5, 0.75, 1.0, 1.25];
      times.forEach((t) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(880, ctx.currentTime + t);

        gain.gain.setValueAtTime(0.4, ctx.currentTime + t);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + t + 0.2);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(ctx.currentTime + t);
        osc.stop(ctx.currentTime + t + 0.22);
      });
    } catch (err) {
      console.error('Failed to play alarm chime:', err);
    }
  };

  // Real-time Alarm Check Loop
  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const currentHours = String(now.getHours()).padStart(2, '0');
      const currentMinutes = String(now.getMinutes()).padStart(2, '0');
      const currentTimeStr = `${currentHours}:${currentMinutes}`;

      medicines.forEach((med) => {
        if (!med.times || med.times.length === 0) return;

        med.times.forEach((scheduledTime) => {
          // Normalize scheduled time string (handles both "08:00" and "08:00 AM")
          let normScheduled = scheduledTime;
          if (scheduledTime.includes('AM') || scheduledTime.includes('PM')) {
            const [t, modifier] = scheduledTime.split(' ');
            let [h, m] = t.split(':');
            if (modifier === 'PM' && h !== '12') h = String(parseInt(h, 10) + 12);
            if (modifier === 'AM' && h === '12') h = '00';
            normScheduled = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
          }

          const alarmKey = `${med.id}_${normScheduled}_${now.toDateString()}_${currentTimeStr}`;

          if (currentTimeStr === normScheduled && !triggeredAlarmsRef.current.has(alarmKey)) {
            triggeredAlarmsRef.current.add(alarmKey);
            setActiveAlarm({ medicine: med, triggerTime: currentTimeStr });
            playAlarmChime();

            // Browser Notification Popup
            if ('Notification' in window && Notification.permission === 'granted') {
              new Notification(`🚨 MEDICATION ALARM: ${med.name}`, {
                body: `Time to take ${med.dosage} of ${med.name}! Instructions: ${med.instructions || 'None'}`,
                icon: '/favicon.ico'
              });
            }
          }
        });
      });
    }, 5000); // Check every 5 seconds

    return () => clearInterval(interval);
  }, [medicines]);

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
      if (activeAlarm && activeAlarm.medicine.id === medId) {
        setActiveAlarm(null);
      }
      fetchData();
    } catch (err) {
      console.error('Failed to log reminder status:', err);
    }
  };

  const handleDeleteMedicine = async (medId) => {
    if (!window.confirm('Are you sure you want to delete this prescription reminder?')) return;
    try {
      await apiClient.delete(`/medication/${medId}`);
      fetchData();
    } catch (err) {
      console.error('Failed to delete medicine:', err);
    }
  };

  const formatDisplayTime = (timeStr) => {
    if (!timeStr) return '';
    if (timeStr.includes('AM') || timeStr.includes('PM')) return timeStr;
    const [h, m] = timeStr.split(':');
    const hourNum = parseInt(h, 10);
    const ampm = hourNum >= 12 ? 'PM' : 'AM';
    const displayHour = hourNum % 12 || 12;
    return `${displayHour}:${m} ${ampm}`;
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-8 rounded-3xl bg-gradient-to-r from-teal-700 via-teal-600 to-emerald-600 text-white shadow-xl">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold">
            <BellRing className="h-3.5 w-3.5 animate-bounce" /> Live Alarm &amp; Audio Reminder System
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight">Medication Reminders</h1>
          <p className="text-teal-50/90 text-sm max-w-xl font-medium">
            Schedule precise prescription alarms, hear audio chimes, and track daily pill adherence.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button onClick={playAlarmChime} variant="secondary" className="bg-white/10 hover:bg-white/20 text-white border-white/20 text-xs font-bold">
            <Volume2 className="h-4 w-4" /> Test Alarm Sound
          </Button>
          <Button onClick={() => setShowAddModal(true)} variant="secondary" className="bg-white text-teal-800 hover:bg-slate-50 font-bold border-0 shadow-md">
            <Plus className="h-4 w-4" /> Add Prescription
          </Button>
        </div>
      </div>

      {/* Active Triggered Alarm Modal Dialog */}
      {activeAlarm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md animate-fadeIn">
          <div className="bg-white max-w-md w-full rounded-3xl p-6 sm:p-8 space-y-6 border-2 border-rose-500 shadow-2xl text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-rose-500 via-amber-500 to-rose-500 animate-pulse" />

            <div className="mx-auto w-16 h-16 rounded-full bg-rose-100 flex items-center justify-center text-rose-600 animate-bounce">
              <Bell className="h-8 w-8" />
            </div>

            <div className="space-y-2">
              <span className="inline-block px-3 py-1 rounded-full bg-rose-100 text-rose-700 text-xs font-extrabold tracking-wider uppercase">
                🚨 PRESCRIPTION ALARM RINGING
              </span>
              <h2 className="text-2xl font-black text-slate-900">{activeAlarm.medicine.name}</h2>
              <p className="text-sm font-bold text-teal-700">{activeAlarm.medicine.dosage} • Scheduled for {formatDisplayTime(activeAlarm.triggerTime)}</p>
              {activeAlarm.medicine.instructions && (
                <p className="text-xs text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-200 mt-2 font-medium">
                  Instruction: {activeAlarm.medicine.instructions}
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <Button
                onClick={() => handleLogReminder(activeAlarm.medicine.id, 'Taken')}
                className="py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-sm shadow-lg"
              >
                <CheckCircle2 className="h-4 w-4" /> Mark Taken
              </Button>
              <Button
                onClick={() => handleLogReminder(activeAlarm.medicine.id, 'Skipped')}
                className="py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold text-sm border border-slate-200"
              >
                <XCircle className="h-4 w-4 text-rose-500" /> Skip / Dismiss
              </Button>
            </div>
          </div>
        </div>
      )}

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
                <Card key={med.id} className="space-y-4 relative group">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-base">{med.name}</h3>
                      <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200">
                        {med.dosage}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-700 flex items-center gap-1 bg-slate-100 px-2 py-1 rounded-lg border border-slate-200">
                        <Clock className="h-3.5 w-3.5 text-teal-600" /> {med.times?.map(formatDisplayTime).join(', ')}
                      </span>
                      <button
                        type="button"
                        onClick={() => handleDeleteMedicine(med.id)}
                        className="p-1 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                        title="Delete Prescription"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
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
              <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Bell className="h-5 w-5 text-teal-600" /> Add Prescription Alarm
              </h3>
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
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Alarm Time</label>
                  <input
                    type="time"
                    required
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
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
                Set Prescription Alarm
              </Button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicationPage;
