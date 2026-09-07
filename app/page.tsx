'use client';

import { useEffect, useMemo, useState } from 'react';
import { ArrowRight, ArrowUpRight, Boxes, BrainCircuit, CheckCircle2, CircleDollarSign, CloudCog, FileCheck2, GitBranch, Network, RefreshCw, ShieldCheck, Sparkles, TriangleAlert } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const risks = [
  { id: 'R-014', name: 'Privileged production access', owner: 'Identity Security', exposure: '$1.84M', residual: '$540K', confidence: '82%', status: 'Above tolerance', decision: 'Fund targeted remediation' },
  { id: 'R-022', name: 'AI tool authority expansion', owner: 'AI Platform', exposure: '$920K', residual: '$260K', confidence: '74%', status: 'Decision due', decision: 'Require scoped approval leases' },
  { id: 'R-031', name: 'Customer assurance backlog', owner: 'GRC Operations', exposure: '$3.20M', residual: '$880K', confidence: '89%', status: 'Commercial impact', decision: 'Automate reusable evidence packs' },
];

const frameworks: Array<[string, number]> = [['SOC 2', 96], ['ISO 27001', 91], ['ISO 42001', 78], ['PCI DSS', 88]];

export default function Home() {
  const [activeRisk, setActiveRisk] = useState(risks[0].id);
  const risk = useMemo(() => risks.find((item) => item.id === activeRisk) ?? risks[0], [activeRisk]);

  useEffect(() => {
    const context = document.modelContext;
    if (!context?.registerTool) return;
    const lifecycle = new AbortController();
    void Promise.resolve(context.registerTool({
      name: 'select_material_risk',
      title: 'Select material risk',
      description: 'Select one material risk in the visible board decision queue and return its decision context.',
      inputSchema: { type: 'object', properties: { riskId: { type: 'string', enum: risks.map((item) => item.id) } }, required: ['riskId'], additionalProperties: false },
      annotations: { readOnlyHint: false, untrustedContentHint: false },
      execute(input: unknown) {
        const riskId = typeof input === 'object' && input !== null && 'riskId' in input ? String((input as { riskId: unknown }).riskId) : '';
        const selected = risks.find((item) => item.id === riskId);
        if (!selected) throw new Error('Unknown riskId');
        setActiveRisk(selected.id);
        return { riskId: selected.id, decision: selected.decision, exposure: selected.exposure, residual: selected.residual };
      },
    }, { signal: lifecycle.signal })).catch(() => undefined);
    return () => lifecycle.abort();
  }, []);

  function downloadBoardBrief() {
    const brief = { generated_at: new Date().toISOString(), risk, evidence_boundary: 'Controlled demonstration data; requires accountable-owner approval before external use.', requested_decision: risk.decision };
    const url = URL.createObjectURL(new Blob([JSON.stringify(brief, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = url; link.download = `${risk.id.toLowerCase()}-board-brief.json`; link.click(); URL.revokeObjectURL(url);
  }

  return (
    <main className="min-h-screen bg-[#07100f] text-[#eef8f3]">
      <header className="border-b border-white/10 bg-[#07100f]/95 px-5 py-4 backdrop-blur md:px-8">
        <div className="mx-auto flex max-w-[1500px] items-center justify-between gap-5">
          <div className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-lg border border-emerald-300/30 bg-emerald-300/10 text-emerald-300"><GitBranch size={18} /></div>
            <div><p className="text-base font-semibold tracking-tight">GRC DecisionGraph</p><p className="text-xs text-slate-500">Evidence → risk → economics → decision</p></div>
          </div>
          <div className="flex items-center gap-3">
            <Badge className="hidden border-emerald-300/20 bg-emerald-300/10 text-emerald-200 md:inline-flex">Evaluation healthy</Badge>
            <Button onClick={downloadBoardBrief} className="bg-emerald-300 text-[#07100f] hover:bg-emerald-200">Prepare board brief <ArrowUpRight data-icon="inline-end" /></Button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-[1500px] px-5 py-7 md:px-8">
        <div className="mb-7 flex flex-col justify-between gap-5 border-b border-white/10 pb-7 lg:flex-row lg:items-end">
          <div><p className="mb-2 font-mono text-xs uppercase tracking-[0.18em] text-emerald-300">Executive assurance workspace · 07 Sep 2026</p><h1 className="max-w-4xl text-3xl font-semibold tracking-[-0.04em] text-white md:text-5xl">Decisions backed by control evidence and economic consequence.</h1></div>
          <p className="max-w-xl text-base leading-7 text-slate-400">A traceable operating view for GRC leaders, control owners, auditors and executives. Unknown evidence remains unknown; modeled value never becomes recognized value without confirmation.</p>
        </div>

        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {[
            { label: 'Control confidence', value: '92.4%', note: '+4.8 pts this quarter', icon: ShieldCheck },
            { label: 'P50 cyber exposure', value: '$4.16M', note: '$1.02M reducible', icon: TriangleAlert },
            { label: 'Verified annual value', value: '$684K', note: 'Finance-ready ledger', icon: CircleDollarSign },
            { label: 'GRC-blocked pipeline', value: '$3.20M', note: '3 priority opportunities', icon: Boxes },
          ].map(({ label, value, note, icon: Icon }) => (
            <article key={label} className="metric-card"><div className="flex items-start justify-between"><p className="text-sm text-slate-400">{label}</p><Icon size={17} className="text-emerald-300" /></div><p className="mt-4 font-mono text-3xl tracking-tight text-white">{value}</p><p className="mt-2 text-sm text-slate-500">{note}</p></article>
          ))}
        </div>

        <div className="mt-4 grid gap-4 xl:grid-cols-[1.45fr_0.85fr]">
          <section className="panel overflow-hidden">
            <div className="flex flex-col justify-between gap-3 border-b border-white/10 p-5 md:flex-row md:items-center"><div><p className="section-kicker">Board decision queue</p><h2 className="mt-1 text-xl font-semibold">Material choices awaiting action</h2></div><p className="text-sm text-slate-500">3 of 11 scenarios exceed escalation thresholds</p></div>
            <div className="grid lg:grid-cols-[0.9fr_1.1fr]">
              <div className="border-b border-white/10 p-3 lg:border-b-0 lg:border-r">
                {risks.map((item) => <button key={item.id} onClick={() => setActiveRisk(item.id)} className={`risk-row ${activeRisk === item.id ? 'risk-row-active' : ''}`}><span><span className="font-mono text-xs text-slate-500">{item.id}</span><span className="mt-1 block text-left text-sm font-medium text-slate-200">{item.name}</span></span><span className="font-mono text-sm text-amber-200">{item.exposure}</span></button>)}
              </div>
              <div className="p-5 md:p-6">
                <div className="flex items-center justify-between gap-4"><Badge className="border-amber-300/20 bg-amber-300/10 text-amber-100">{risk.status}</Badge><span className="font-mono text-xs text-slate-500">Confidence {risk.confidence}</span></div>
                <h3 className="mt-5 text-2xl font-semibold tracking-tight text-white">{risk.name}</h3><p className="mt-2 text-sm text-slate-500">Accountable owner · {risk.owner}</p>
                <div className="mt-6 grid grid-cols-2 gap-3"><div className="subpanel"><p className="label">Current P50 exposure</p><p className="mt-2 font-mono text-2xl text-amber-200">{risk.exposure}</p></div><div className="subpanel"><p className="label">After remediation</p><p className="mt-2 font-mono text-2xl text-emerald-200">{risk.residual}</p></div></div>
                <div className="mt-5 border-l-2 border-emerald-300 pl-4"><p className="label">Recommended decision</p><p className="mt-1 text-base font-medium text-white">{risk.decision}</p></div>
              </div>
            </div>
          </section>

          <section className="panel p-5 md:p-6">
            <div className="flex items-center justify-between"><div><p className="section-kicker">Framework assurance</p><h2 className="mt-1 text-xl font-semibold">Evidence coverage</h2></div><FileCheck2 className="text-emerald-300" size={21} /></div>
            <p className="mt-3 text-sm leading-6 text-slate-500">Cross-mapping is separated from evidence qualification. One mapped requirement does not imply that its evidence is fresh, complete or accepted.</p>
            <div className="mt-6 space-y-5">{frameworks.map(([name, coverage]) => <div key={name}><div className="mb-2 flex justify-between text-sm"><span className="text-slate-300">{name}</span><span className="font-mono text-slate-400">{coverage}% qualified</span></div><Progress value={coverage} className="h-1.5 bg-white/10 [&_[data-slot=progress-indicator]]:bg-emerald-300" /></div>)}</div>
            <div className="mt-7 rounded-xl border border-cyan-300/15 bg-cyan-300/[0.05] p-4"><div className="flex gap-3"><Sparkles size={18} className="mt-0.5 shrink-0 text-cyan-300" /><div><p className="text-sm font-medium text-cyan-100">150+ framework integration plane</p><p className="mt-1 text-sm leading-6 text-slate-400">Designed to consume the OSS CISO Assistant framework catalog and qualify reusable evidence through the a2zsoc.com hosted plane.</p></div></div></div>
          </section>
        </div>

        <section className="panel mt-4 overflow-hidden">
          <div className="grid border-b border-white/10 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="p-6 md:p-8"><p className="section-kicker">Cross-mapping without false equivalence</p><h2 className="mt-2 max-w-xl text-3xl font-semibold tracking-[-0.03em]">150+ frameworks, one qualified evidence plane.</h2><p className="mt-4 max-w-2xl text-base leading-7 text-slate-400">The integration contract can ingest the 150+ governance, risk, privacy, security and AI frameworks listed by OSS CISO Assistant. GRC DecisionGraph preserves the upstream framework identity and version, then applies reviewed, directional cross-mappings and evidence qualification on the a2zsoc.com hosted plane.</p></div>
            <div className="grid grid-cols-2 border-t border-white/10 lg:border-l lg:border-t-0">
              {[['Framework catalog', '150+', 'CISO Assistant integration-ready'], ['Mapping modes', '4', 'Exact · substantial · partial · related'], ['Evidence gates', '5', 'Provenance · integrity · freshness · scope · relevance'], ['Transitive claims', '0', 'Never inferred without review']].map(([label, value, note]) => <div key={label} className="border-b border-r border-white/10 p-5 last:border-b-0 md:p-6"><p className="label">{label}</p><p className="mt-3 font-mono text-3xl text-white">{value}</p><p className="mt-2 text-sm leading-6 text-slate-500">{note}</p></div>)}
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[850px] text-left text-sm">
              <thead className="border-b border-white/10 bg-black/15 text-xs uppercase tracking-[0.1em] text-slate-500"><tr><th className="px-6 py-4 font-medium">Source requirement</th><th className="px-6 py-4 font-medium">Target requirement</th><th className="px-6 py-4 font-medium">Strength</th><th className="px-6 py-4 font-medium">Coverage</th><th className="px-6 py-4 font-medium">Evidence state</th></tr></thead>
              <tbody>{[
                ['SOC 2 · CC6.1', 'ISO 27001 · A.5.15', 'Substantial', '85%', 'Qualified'],
                ['SOC 2 · CC7.2', 'ISO 27001 · A.8.16', 'Substantial', '90%', 'Qualified'],
                ['ISO 42001 · A.6.2.6', 'NIST AI RMF · MEASURE 2', 'Partial', '68%', 'Review due'],
                ['PCI DSS · 10.2', 'NIST 800-53 · AU-2', 'Related', '61%', 'Scope gap'],
              ].map((row) => <tr key={row[0]} className="border-b border-white/[0.07] last:border-0"><td className="px-6 py-4 font-medium text-slate-200">{row[0]}</td><td className="px-6 py-4 text-slate-400">{row[1]}</td><td className="px-6 py-4"><Badge variant="outline" className="border-white/10 text-slate-300">{row[2]}</Badge></td><td className="px-6 py-4 font-mono text-slate-300">{row[3]}</td><td className="px-6 py-4 text-emerald-200">{row[4]}</td></tr>)}</tbody>
            </table>
          </div>
        </section>

        <div className="mt-4 grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
          <section className="panel p-6 md:p-8">
            <div className="flex items-start justify-between gap-4"><div><p className="section-kicker">Evaluation & evolution engineering</p><h2 className="mt-2 text-2xl font-semibold">Two loops, one controlled release path</h2></div><RefreshCw className="text-emerald-300" /></div>
            <div className="mt-7 grid gap-4 md:grid-cols-2">
              <div className="subpanel"><p className="font-mono text-xs text-cyan-300">EVALUATION LOOP</p><div className="mt-5 space-y-3">{['Collect signed evidence', 'Qualify five evidence dimensions', 'Evaluate control verdict', 'Quantify loss and uncertainty', 'Compare predicted vs actual'].map((item, index) => <div key={item} className="flex items-center gap-3 text-sm text-slate-300"><span className="grid h-6 w-6 place-items-center rounded-full bg-cyan-300/10 font-mono text-xs text-cyan-200">{index + 1}</span>{item}</div>)}</div></div>
              <div className="subpanel"><p className="font-mono text-xs text-emerald-300">EVOLUTION LOOP</p><div className="mt-5 space-y-3">{['Classify root cause', 'Rank risk-adjusted value', 'Test offline regression suite', 'Canary controlled change', 'Approve, revise or roll back'].map((item, index) => <div key={item} className="flex items-center gap-3 text-sm text-slate-300"><span className="grid h-6 w-6 place-items-center rounded-full bg-emerald-300/10 font-mono text-xs text-emerald-200">{index + 1}</span>{item}</div>)}</div></div>
            </div>
            <div className="mt-5 flex items-center gap-3 rounded-lg border border-amber-300/15 bg-amber-300/[0.04] p-4 text-sm leading-6 text-slate-400"><TriangleAlert size={18} className="shrink-0 text-amber-200" />Agents may recommend changes. They cannot approve material controls, risk acceptance, external assurance or revenue attribution.</div>
          </section>

          <section className="panel p-6 md:p-8">
            <p className="section-kicker">Evidence qualification</p><h2 className="mt-2 text-2xl font-semibold">One receipt, five independent gates</h2>
            <div className="mt-6 space-y-3">{[
              ['Provenance', 'PASS', 'aws-iam-adapter@1.2.0'], ['Integrity', 'PASS', 'SHA-256 receipt reproduced'], ['Freshness', 'PASS', 'Valid for 17h 42m'], ['Scope', 'FAIL', 'Payments account absent'], ['Relevance', 'PASS', 'Objective directly supported'],
            ].map(([name, verdict, detail]) => <div key={name} className="flex items-center justify-between gap-4 border-b border-white/[0.07] py-3"><div className="flex items-center gap-3">{verdict === 'PASS' ? <CheckCircle2 size={17} className="text-emerald-300" /> : <TriangleAlert size={17} className="text-amber-200" />}<span className="text-sm text-slate-200">{name}</span></div><div className="text-right"><span className={`font-mono text-xs ${verdict === 'PASS' ? 'text-emerald-200' : 'text-amber-200'}`}>{verdict}</span><p className="mt-1 text-xs text-slate-500">{detail}</p></div></div>)}
            </div>
            <p className="mt-5 rounded-lg bg-black/20 p-4 text-sm leading-6 text-slate-400"><span className="font-medium text-white">Control result: FAIL.</span> Four passing gates cannot compensate for missing required scope.</p>
          </section>
        </div>

        <section className="panel mt-4 p-6 md:p-8">
          <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end"><div><p className="section-kicker">Unit economics ledger</p><h2 className="mt-2 text-3xl font-semibold tracking-[-0.03em]">Recognized value is narrower than possible value.</h2></div><p className="max-w-xl text-sm leading-6 text-slate-500">Synthetic reference case. Capacity and unconfirmed attribution are visible but excluded from ROI.</p></div>
          <Tabs defaultValue="ledger" className="mt-7">
            <TabsList variant="line" className="border-b border-white/10"><TabsTrigger value="ledger">Value ledger</TabsTrigger><TabsTrigger value="formula">Reconciliation</TabsTrigger><TabsTrigger value="board">Board thresholds</TabsTrigger></TabsList>
            <TabsContent value="ledger" className="pt-6"><div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">{[
              ['Labor savings', '$123,750', 'Recognized'], ['Confirmed direct revenue', '$420,000', 'Recognized'], ['Validated loss reduction', '$180,000', 'Recognized'], ['Contributory pipeline', '$900,000', 'Excluded'], ['Capacity pipeline', '$3.20M', 'Excluded'],
            ].map(([label, value, state]) => <div key={label} className="subpanel"><p className="label">{label}</p><p className="mt-3 font-mono text-2xl text-white">{value}</p><p className={`mt-2 text-xs ${state === 'Recognized' ? 'text-emerald-300' : 'text-slate-500'}`}>{state}</p></div>)}</div></TabsContent>
            <TabsContent value="formula" className="pt-6"><div className="grid gap-4 md:grid-cols-3"><div className="subpanel"><p className="label">Recognized value</p><p className="mt-2 font-mono text-2xl text-white">$723,750</p><p className="mt-2 text-sm text-slate-500">Verified labor + confirmed direct revenue + validated loss reduction</p></div><div className="subpanel"><p className="label">First-year net value</p><p className="mt-2 font-mono text-2xl text-emerald-200">$507,750</p><p className="mt-2 text-sm text-slate-500">Recognized value − $216,000 implementation and platform cost</p></div><div className="subpanel"><p className="label">ROI / payback</p><p className="mt-2 font-mono text-2xl text-white">235% · 3.58 mo</p><p className="mt-2 text-sm text-slate-500">Reconciled from the same versioned input ledger</p></div></div></TabsContent>
            <TabsContent value="board" className="pt-6"><div className="grid gap-3 md:grid-cols-3">{[['Risk escalation', 'P50 exposure exceeds tolerance'], ['Commercial escalation', 'Priority contract is GRC-blocked'], ['Board participation', '2 production loops + accepted economics']].map(([label, value]) => <div key={label} className="subpanel"><p className="label">{label}</p><p className="mt-3 text-base font-medium text-slate-200">{value}</p></div>)}</div></TabsContent>
          </Tabs>
        </section>

        <section className="my-4 grid gap-4 md:grid-cols-4">
          {[{icon:CloudCog,label:'Evidence sources',text:'AWS, Kubernetes, Vanta, Linear, Elastic and VictoriaLogs remain replaceable inputs.'},{icon:Network,label:'Decision graph',text:'Controls, risks, obligations, owners, customers and evidence retain explicit lineage.'},{icon:BrainCircuit,label:'Governed agents',text:'Cited recommendations are evaluated before any material human decision.'},{icon:CircleDollarSign,label:'Business outcomes',text:'Board choices and priority-contract impact reconcile to the value ledger.'}].map(({icon:Icon,label,text}, index) => <article key={label} className="panel p-5"><div className="flex items-center justify-between"><Icon size={20} className="text-emerald-300" /><span className="font-mono text-xs text-slate-600">0{index+1}</span></div><h3 className="mt-6 font-medium text-white">{label}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{text}</p>{index<3 && <ArrowRight className="mt-5 hidden text-slate-700 md:block" size={17}/>}</article>)}
        </section>
        <footer className="flex flex-col justify-between gap-5 border-t border-white/10 py-7 md:flex-row md:items-center">
          <div><p className="font-medium text-white">Portable engine · intended a2zsoc.com qualification plane</p><p className="mt-1 text-sm text-slate-500">Controlled demonstration data. Framework content remains with its authorized source.</p></div>
          <div className="flex flex-wrap gap-3"><Button nativeButton={false} variant="outline" className="border-white/10 bg-transparent text-white hover:bg-white/[0.05]" render={<a href="/api/v1/decisiongraph.json" />}>API contract</Button><Button nativeButton={false} className="bg-white text-[#07100f] hover:bg-slate-200" render={<a href="https://github.com/AAH20/grc-automation-cyber-risk-quantification-platform" target="_blank" rel="noreferrer" />}>Source repository <ArrowUpRight data-icon="inline-end" /></Button></div>
        </footer>
      </section>
    </main>
  );
}
