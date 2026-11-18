'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import {
  Shield, Lock, Mail, UserCheck, AlertCircle, ArrowRight,
  CheckCircle2, Scale, BookOpen, Layers
} from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('inspector@gov.in');
  const [password, setPassword] = useState('demo');
  const [role, setRole] = useState<'INSPECTOR' | 'SUPERVISOR' | 'ADMIN'>('INSPECTOR');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRoleSelect = (selectedRole: 'INSPECTOR' | 'SUPERVISOR' | 'ADMIN') => {
    setRole(selectedRole);
    if (selectedRole === 'INSPECTOR') setEmail('inspector@gov.in');
    else if (selectedRole === 'SUPERVISOR') setEmail('supervisor@gov.in');
    else setEmail('admin@gov.in');
    setPassword('demo');
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await api.login(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-8">
      {/* Institutional Header */}
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-[#0075de] text-white shadow-md mb-3">
          <Shield className="w-8 h-8" />
        </div>
        <h1 className="text-xl font-bold tracking-tight text-[#000000]">
          Legal Metrology Officer Portal
        </h1>
        <p className="text-xs text-[#615d59] mt-1">
          Government of India • Ministry of Consumer Affairs, Food & Public Distribution
        </p>
        <div className="flex items-center justify-center gap-2 mt-2">
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-[#0075de] border border-blue-200">
            PCR 2011 Enforcement
          </span>
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-green-50 text-[#166534] border border-green-200">
            SIH26034 v2.4
          </span>
        </div>
      </div>

      {/* Login Card */}
      <div className="bg-white rounded-2xl border border-[#e6e6e6] p-6 shadow-sm">
        {/* Role Quick Selector */}
        <div className="mb-5">
          <label className="block text-xs font-semibold text-[#615d59] mb-2">
            Select Officer Designation / Role:
          </label>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={() => handleRoleSelect('INSPECTOR')}
              className={`px-2.5 py-2 rounded-lg text-xs font-medium border text-center transition-all ${
                role === 'INSPECTOR'
                  ? 'bg-blue-50 border-[#0075de] text-[#0075de] font-bold shadow-xs'
                  : 'border-[#e6e6e6] text-[#31302e] hover:bg-[#f6f5f4]'
              }`}
            >
              Field Inspector
            </button>
            <button
              type="button"
              onClick={() => handleRoleSelect('SUPERVISOR')}
              className={`px-2.5 py-2 rounded-lg text-xs font-medium border text-center transition-all ${
                role === 'SUPERVISOR'
                  ? 'bg-blue-50 border-[#0075de] text-[#0075de] font-bold shadow-xs'
                  : 'border-[#e6e6e6] text-[#31302e] hover:bg-[#f6f5f4]'
              }`}
            >
              Supervisor
            </button>
            <button
              type="button"
              onClick={() => handleRoleSelect('ADMIN')}
              className={`px-2.5 py-2 rounded-lg text-xs font-medium border text-center transition-all ${
                role === 'ADMIN'
                  ? 'bg-blue-50 border-[#0075de] text-[#0075de] font-bold shadow-xs'
                  : 'border-[#e6e6e6] text-[#31302e] hover:bg-[#f6f5f4]'
              }`}
            >
              Admin
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 flex items-center gap-2 text-xs text-[#991B1B]">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-[#31302e] mb-1">
              Government Official Email
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-[#615d59] absolute left-3 top-2.5" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-[#e6e6e6] focus:border-[#0075de] focus:outline-none"
                placeholder="officer@gov.in"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#31302e] mb-1">
              Inspection Key / Security Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#615d59] absolute left-3 top-2.5" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-[#e6e6e6] focus:border-[#0075de] focus:outline-none"
                placeholder="••••••••"
              />
            </div>
            <p className="text-[10px] text-[#615d59] mt-1">
              Default demo credential key: <code className="bg-slate-100 px-1 py-0.5 rounded font-mono">demo</code>
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 rounded-xl text-xs font-bold bg-[#0075de] text-white hover:bg-[#005bab] transition-all flex items-center justify-center gap-2 shadow-sm disabled:opacity-60"
          >
            {loading ? (
              <span>Authenticating Officer...</span>
            ) : (
              <>
                <UserCheck className="w-4 h-4" />
                <span>Sign In to Enforcement Dashboard</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </form>

        <div className="mt-5 pt-4 border-t border-[#e6e6e6] flex items-center justify-between text-xs">
          <Link
            href="/dashboard"
            className="text-[#0075de] font-semibold hover:underline flex items-center gap-1"
          >
            <span>Continue as Guest Officer</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
          <Link
            href="/rules"
            className="text-[#615d59] hover:text-[#000000]"
          >
            View Statutory Rules
          </Link>
        </div>
      </div>

      {/* Security Notice */}
      <div className="mt-6 text-center text-[11px] text-[#615d59] space-y-1">
        <p className="font-semibold text-[#31302e]">
          Official Notice under Section 36 of Legal Metrology Act, 2009
        </p>
        <p>
          Authorized access only. System activity is logged under statutory audit trails.
        </p>
      </div>
    </div>
  );
}
