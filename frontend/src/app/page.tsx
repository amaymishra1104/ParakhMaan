'use client';

import React from 'react';
import Link from 'next/link';
import {
  Shield, CheckCircle2, AlertTriangle, Scale, BookOpen,
  ArrowRight, FileText, Layers, Camera, Cpu, Eye, Sparkles
} from 'lucide-react';

export default function HomePage() {
  return (
    <div className="space-y-10 py-4">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-white via-slate-50 to-blue-50/40 rounded-2xl border border-[#e6e6e6] p-8 sm:p-12 shadow-sm text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-blue-100/80 text-[#0075de] border border-blue-200 mb-6">
          <Shield className="w-3.5 h-3.5" />
          <span>PARAKHMAAN (परखमान) • LEGAL METROLOGY & QUALITY INSPECTION AI</span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-[#000000] max-w-3xl mx-auto leading-tight">
          ParakhMaan
          <span className="block text-xl sm:text-2xl font-bold text-[#0075de] mt-2">
            AI-Powered Legal Metrology Compliance & Inspection Platform
          </span>
        </h1>

        <p className="text-sm text-[#615d59] max-w-2xl mx-auto mt-4 leading-relaxed">
          Statutory inspection & automated auditing system for Packaged Commodities Rules (2011).
          Built with deterministic legal engines, dual-path vision OCR, multi-surface contradiction detection,
          industrial defect quality gates, and tamper-evident statutory PDF report generation.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-3 mt-8">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 px-6 py-3 rounded-full text-xs font-bold bg-[#0075de] text-white hover:bg-[#005bab] transition-all shadow-md"
          >
            <Shield className="w-4 h-4" />
            <span>Launch Inspection Command Center</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/inspections/new"
            className="flex items-center gap-2 px-5 py-3 rounded-full text-xs font-semibold bg-white text-[#31302e] border border-[#e6e6e6] hover:bg-[#f6f5f4] transition-all shadow-xs"
          >
            <Camera className="w-4 h-4 text-[#0075de]" />
            <span>Audit New Package</span>
          </Link>
          <Link
            href="/login"
            className="flex items-center gap-2 px-5 py-3 rounded-full text-xs font-semibold bg-white text-[#615d59] border border-[#e6e6e6] hover:text-[#000000] hover:bg-[#f6f5f4] transition-all shadow-xs"
          >
            <span>Officer Sign-In</span>
          </Link>
        </div>
      </div>

      {/* 4 Pillars of Architecture */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-[#e6e6e6] p-5 shadow-xs">
          <div className="w-9 h-9 rounded-lg bg-blue-50 text-[#0075de] flex items-center justify-center mb-3">
            <Camera className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-xs text-[#000000] uppercase tracking-wider">
            1. Multi-Surface Ingestion
          </h3>
          <p className="text-xs text-[#615d59] mt-1.5 leading-relaxed">
            Ingest up to 4 surfaces (Front, Back, Side, Top/Bottom) with OpenCV Laplacian blur detection,
            specular glare gates, and unprinted surface rejection.
          </p>
        </div>

        <div className="bg-white rounded-xl border border-[#e6e6e6] p-5 shadow-xs">
          <div className="w-9 h-9 rounded-lg bg-green-50 text-[#166534] flex items-center justify-center mb-3">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-xs text-[#000000] uppercase tracking-wider">
            2. Local Vision OCR
          </h3>
          <p className="text-xs text-[#615d59] mt-1.5 leading-relaxed">
            CPU-optimized perception with native Windows Media OCR and EasyOCR. Extracts MRP (₹/Rs), Net Qty,
            Dates, Mfg details, and Unit Sale Price.
          </p>
        </div>

        <div className="bg-white rounded-xl border border-[#e6e6e6] p-5 shadow-xs">
          <div className="w-9 h-9 rounded-lg bg-amber-50 text-[#854D0E] flex items-center justify-center mb-3">
            <Scale className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-xs text-[#000000] uppercase tracking-wider">
            3. Deterministic Rule Engine
          </h3>
          <p className="text-xs text-[#615d59] mt-1.5 leading-relaxed">
            Legal Non-Delegation Principle: 40+ statutory rules verify declarations with 100% legal traceability
            to the 2011 Rules and Gazette amendments.
          </p>
        </div>

        <div className="bg-white rounded-xl border border-[#e6e6e6] p-5 shadow-xs">
          <div className="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center mb-3">
            <FileText className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-xs text-[#000000] uppercase tracking-wider">
            4. Statutory Audit & Reports
          </h3>
          <p className="text-xs text-[#615d59] mt-1.5 leading-relaxed">
            Inspector Evidence Canvas with thermal heatmaps, interactive manual override trails, and instant
            downloadable statutory PDF inspection reports.
          </p>
        </div>
      </div>

      {/* Live System Metrics Quick Bar */}
      <div className="bg-white rounded-xl border border-[#e6e6e6] p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse" />
          <div>
            <p className="text-xs font-bold text-[#000000]">System Operational: CPU Mode (Air-Gapped Ready)</p>
            <p className="text-[11px] text-[#615d59]">Ready on Windows 11 • No GPU or external cloud dependencies mandatory</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/rules"
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#f6f5f4] text-[#31302e] hover:bg-slate-200 transition-colors"
          >
            Statutory Calculators & MPE
          </Link>
          <Link
            href="/dashboard"
            className="px-3 py-1.5 rounded-lg text-xs font-bold bg-[#0075de] text-white hover:bg-[#005bab] transition-colors"
          >
            Open Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}
