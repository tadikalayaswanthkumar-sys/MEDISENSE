import React, { useState, useEffect } from 'react';
import { FileText, Upload, Sparkles, AlertCircle, CheckCircle2, FileUp, Loader2, Info, ChevronRight, Activity } from 'lucide-react';
import apiClient from '@/shared/api/axios';
import Card from '@/shared/components/ui/Card';
import Button from '@/shared/components/ui/Button';

export const ReportsPage = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [title, setTitle] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedReport, setSelectedReport] = useState(null);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const fetchReports = async () => {
    try {
      const res = await apiClient.get('/reports/');
      setReports(res.data);
    } catch (err) {
      console.error('Failed to fetch reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select a medical report file (Image or PDF).');
      return;
    }

    setError('');
    setSuccessMsg('');
    setUploading(true);

    const formData = new FormData();
    formData.append('title', title || selectedFile.name);
    formData.append('file', selectedFile);

    try {
      const res = await apiClient.post('/reports/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSuccessMsg('Report analyzed successfully with Gemini AI!');
      setTitle('');
      setSelectedFile(null);
      fetchReports();
      setSelectedReport(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process medical report.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-8 rounded-3xl bg-gradient-to-r from-teal-700 via-teal-600 to-emerald-600 text-white shadow-xl">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold">
            <Sparkles className="h-3.5 w-3.5" /> Automated OCR &amp; Disease Risk Analysis
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight">Medical Reports Hub</h1>
          <p className="text-teal-50/90 text-sm max-w-xl font-medium">
            Upload diagnostic lab reports (PDF/Image) for text extraction, AI disease prediction, and health scoring.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* File Upload Section */}
        <Card className="lg:col-span-1 space-y-6">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Upload className="h-5 w-5 text-teal-600" /> Upload Lab Report
          </h2>

          {error && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" /> {error}
            </div>
          )}

          {successMsg && (
            <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 shrink-0" /> {successMsg}
            </div>
          )}

          <form onSubmit={handleUpload} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Report Title (Optional)</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Comprehensive Blood Panel"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 focus:outline-none focus:bg-white focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 font-medium"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-600">Report File (PDF / Image)</label>
              <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-2xl p-6 bg-slate-50 hover:bg-teal-50/50 hover:border-teal-400 transition-all cursor-pointer text-center">
                <FileUp className="h-8 w-8 text-teal-600 mb-2" />
                <span className="text-xs font-bold text-slate-700">
                  {selectedFile ? selectedFile.name : 'Click to select or drop file'}
                </span>
                <span className="text-[11px] text-slate-400 mt-1">Supports PDF, PNG, JPG (Max 10MB)</span>
                <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={handleFileChange} className="hidden" />
              </label>
            </div>

            <Button type="submit" disabled={uploading} className="w-full py-3 font-bold shadow-md">
              {uploading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> OCR &amp; AI Processing...
                </>
              ) : (
                'Analyze & Save Report'
              )}
            </Button>
          </form>
        </Card>

        {/* Reports History & Analysis Details */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <FileText className="h-5 w-5 text-teal-600" /> Uploaded Reports History
          </h2>

          {loading ? (
            <div className="p-8 text-center text-slate-500 font-medium">Loading medical reports...</div>
          ) : reports.length === 0 ? (
            <Card className="text-center py-12 space-y-3">
              <Info className="h-10 w-10 text-slate-300 mx-auto" />
              <p className="text-slate-600 font-semibold text-sm">No medical reports uploaded yet.</p>
              <p className="text-xs text-slate-400">Upload your first lab report on the left panel to begin AI analysis.</p>
            </Card>
          ) : (
            <div className="space-y-4">
              {reports.map((report) => (
                <Card
                  key={report.id}
                  className="hover:border-teal-400 transition-all cursor-pointer"
                  onClick={() => setSelectedReport(report)}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900 text-base">{report.title}</span>
                        <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                          {new Date(report.upload_date).toLocaleDateString()}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 line-clamp-1">{report.summary}</p>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      <div className="text-right">
                        <span className="text-xs font-bold text-slate-400 block">Health Score</span>
                        <span className="text-lg font-extrabold text-teal-700">{report.health_score}/100</span>
                      </div>
                      <ChevronRight className="h-5 w-5 text-slate-400" />
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Report Analysis Detail Modal */}
      {selectedReport && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fadeIn">
          <div className="bg-white max-w-2xl w-full rounded-3xl p-6 sm:p-8 space-y-6 max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-xl font-bold text-slate-900">{selectedReport.title}</h3>
                <p className="text-xs text-slate-500">Uploaded on {new Date(selectedReport.upload_date).toLocaleString()}</p>
              </div>
              <button
                onClick={() => setSelectedReport(null)}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            {/* AI Health Score Banner */}
            <div className="p-4 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-teal-700 uppercase tracking-wider">Calculated AI Health Score</span>
                <p className="text-xs text-slate-600 mt-0.5">{selectedReport.summary}</p>
              </div>
              <span className="text-3xl font-black text-teal-700 shrink-0">{selectedReport.health_score}/100</span>
            </div>

            {/* Disease Risk Assessment */}
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Activity className="h-4 w-4 text-teal-600" /> AI Disease Risk Predictions
              </h4>
              <div className="space-y-2">
                {selectedReport.risk_assessment?.map((risk, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-slate-800">{risk.condition}</span>
                      <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${risk.risk_level === 'High' ? 'bg-rose-100 text-rose-700 border border-rose-200' : risk.risk_level === 'Moderate' ? 'bg-amber-100 text-amber-700 border border-amber-200' : 'bg-emerald-100 text-emerald-700 border border-emerald-200'}`}>
                        {risk.risk_level} Risk
                      </span>
                    </div>
                    <p className="text-xs text-slate-600">{risk.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Extracted Biomarkers Table */}
            {Object.keys(selectedReport.biomarkers || {}).length > 0 && (
              <div className="space-y-3">
                <h4 className="text-sm font-bold text-slate-900">Extracted Lab Biomarkers</h4>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {Object.entries(selectedReport.biomarkers).map(([key, val]) => (
                    <div key={key} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                      <span className="text-slate-500 capitalize block">{key}</span>
                      <span className="font-bold text-slate-800">{val.val} {val.unit}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            <div className="space-y-2">
              <h4 className="text-sm font-bold text-slate-900">AI Health Recommendations</h4>
              <ul className="list-disc list-inside text-xs text-slate-600 space-y-1">
                {selectedReport.recommendations?.map((rec, i) => (
                  <li key={i}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportsPage;
