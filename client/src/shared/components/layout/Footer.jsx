import React from 'react';
import { Shield, Heart } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="border-t border-slate-200 bg-white/80 px-8 py-4 text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-4 mt-auto">
      <div className="flex items-center gap-2">
        <Shield className="h-4 w-4 text-teal-600" />
        <span className="font-medium text-slate-600">HIPAA Compliant &amp; End-to-End Encrypted Health Records</span>
      </div>
      <div className="flex items-center gap-1 text-slate-600 font-medium">
        <span>Built with</span>
        <Heart className="h-3.5 w-3.5 text-rose-500 fill-rose-500 inline" />
        <span>for MediSense AI &copy; {new Date().getFullYear()}</span>
      </div>
    </footer>
  );
};

export default Footer;
