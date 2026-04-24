"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { useUserStore } from "@/store/useUserStore";
import { 
  CheckCircle2, 
  User, 
  Briefcase, 
  GraduationCap, 
  Link as LinkIcon, 
  Save, 
  Edit3,
  ChevronRight,
  Sparkles
} from "lucide-react";

export default function ProfileReviewPage() {
  const router = useRouter();
  const { setProfile } = useUserStore();
  const [profile, setProfileData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const data = localStorage.getItem("suggested_profile");
    if (data) {
      setProfileData(JSON.parse(data));
    } else {
      router.push("/onboarding");
    }
  }, [router]);

  const handleConfirm = async () => {
    setLoading(true);
    try {
      const res = await api.post("/onboarding/confirm", profile);
      // Update global user store
      const userRes = await api.get("/user/me");
      setProfile(userRes.data.profile);
      
      router.push("/automation");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!profile) return null;

  return (
    <div className="min-h-screen bg-neutral-950 p-6 md:p-12">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold uppercase tracking-widest mb-4">
              <Sparkles className="w-3 h-3" />
              <span>AI Extraction Complete</span>
            </div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Review Your Identity</h1>
            <p className="text-neutral-400 mt-2">The agent network has synthesized your profile. Verify the details below.</p>
          </div>
          <button 
            onClick={handleConfirm}
            disabled={loading}
            className="flex items-center gap-3 px-8 py-4 bg-violet-600 hover:bg-violet-500 text-white font-bold rounded-2xl shadow-glow transition-all active:scale-[0.98] disabled:opacity-50"
          >
            {loading ? "Syncing..." : "Confirm & Launch OS"}
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Profile Info */}
          <div className="lg:col-span-2 space-y-8">
            {/* Identity Card */}
            <Section icon={<User className="w-5 h-5" />} title="Core Identity">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input label="Full Name" value={profile.full_name} onChange={(v) => setProfileData({...profile, full_name: v})} />
                <Input label="Email" value={profile.email} onChange={(v) => setProfileData({...profile, email: v})} />
                <Input label="Phone" value={profile.phone} onChange={(v) => setProfileData({...profile, phone: v})} />
                <Input label="Location" value={profile.location} onChange={(v) => setProfileData({...profile, location: v})} />
              </div>
              <div className="mt-6">
                <Input label="Target Job Title" value={profile.job_title} onChange={(v) => setProfileData({...profile, job_title: v})} />
              </div>
            </Section>

            {/* Experience */}
            <Section icon={<Briefcase className="w-5 h-5" />} title="Experience">
              <div className="space-y-6">
                {profile.experience?.map((exp: any, i: number) => (
                  <div key={i} className="p-4 rounded-xl bg-neutral-950 border border-neutral-800 relative group">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-bold text-white">{exp.role}</p>
                        <p className="text-sm text-violet-400">{exp.company}</p>
                      </div>
                      <span className="text-[10px] text-neutral-600 font-bold uppercase">{exp.duration}</span>
                    </div>
                    <p className="text-xs text-neutral-500 leading-relaxed">{exp.description}</p>
                  </div>
                ))}
              </div>
            </Section>
          </div>

          {/* Sidebar Info */}
          <div className="space-y-8">
            {/* Skills Card */}
            <Section icon={<Sparkles className="w-5 h-5" />} title="Skill Graph">
              <div className="flex flex-wrap gap-2">
                {profile.skills?.map((skill: string, i: number) => (
                  <span key={i} className="px-3 py-1 rounded-lg bg-violet-500/5 border border-violet-500/20 text-violet-300 text-[10px] font-medium uppercase tracking-wider">
                    {skill}
                  </span>
                ))}
              </div>
            </Section>

            {/* Education */}
            <Section icon={<GraduationCap className="w-5 h-5" />} title="Education">
              <div className="space-y-4">
                {profile.education?.map((edu: any, i: number) => (
                  <div key={i} className="text-sm">
                    <p className="font-bold text-white">{edu.degree}</p>
                    <p className="text-xs text-neutral-500">{edu.institution}</p>
                    <p className="text-[10px] text-neutral-600 mt-1">{edu.year}</p>
                  </div>
                ))}
              </div>
            </Section>

            {/* Links */}
            <Section icon={<LinkIcon className="w-5 h-5" />} title="Digital Presence">
              <div className="space-y-4">
                <Input label="LinkedIn" value={profile.links?.linkedin} onChange={(v) => setProfileData({...profile, links: {...profile.links, linkedin: v}})} />
                <Input label="GitHub" value={profile.links?.github} onChange={(v) => setProfileData({...profile, links: {...profile.links, github: v}})} />
                <Input label="Portfolio" value={profile.links?.portfolio} onChange={(v) => setProfileData({...profile, links: {...profile.links, portfolio: v}})} />
              </div>
            </Section>
          </div>
        </div>
      </div>
    </div>
  );
}

function Section({ icon, title, children }: { icon: any, title: string, children: React.ReactNode }) {
  return (
    <div className="bg-neutral-900/40 border border-neutral-800 rounded-3xl p-6 backdrop-blur-sm overflow-hidden">
      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-neutral-800/50">
        <div className="text-violet-400">{icon}</div>
        <h2 className="font-bold text-white tracking-tight">{title}</h2>
      </div>
      {children}
    </div>
  );
}

function Input({ label, value, onChange }: { label: string, value: string, onChange: (v: string) => void }) {
  return (
    <div className="space-y-1.5 w-full">
      <label className="text-[10px] font-bold text-neutral-600 uppercase tracking-widest ml-1">{label}</label>
      <input 
        type="text" 
        value={value || ""} 
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-neutral-950 border border-neutral-800 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-neutral-700 focus:outline-none focus:border-violet-600/50 transition-all"
      />
    </div>
  );
}
