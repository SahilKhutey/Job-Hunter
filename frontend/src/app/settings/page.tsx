"use client";

import { useEffect, useState } from "react";
import { useUserStore } from "@/store/useUserStore";
import { updateProfile } from "@/lib/api";

type Tab = "profile" | "ai" | "security" | "notifications";

function SectionHeader({ icon, title, desc }: { icon: string; title: string; desc: string }) {
  return (
    <div className="flex items-start gap-4 pb-5 mb-5 border-b border-neutral-800">
      <div className="w-9 h-9 rounded-xl bg-violet-500/10 flex items-center justify-center shrink-0">
        <span className="material-icons-round text-violet-400 text-[18px]">{icon}</span>
      </div>
      <div>
        <h2 className="font-semibold text-white text-sm">{title}</h2>
        <p className="text-xs text-neutral-500 mt-0.5">{desc}</p>
      </div>
    </div>
  );
}

function Toggle({ label, sub, checked, onChange }: { label: string; sub?: string; checked: boolean; onChange: () => void }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-neutral-800/60 last:border-0">
      <div>
        <p className="text-sm text-white">{label}</p>
        {sub && <p className="text-xs text-neutral-500 mt-0.5">{sub}</p>}
      </div>
      <button
        onClick={onChange}
        className={`relative w-10 h-5 rounded-full transition-colors duration-200 ${checked ? "bg-violet-600" : "bg-neutral-700"}`}
      >
        <span className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform duration-200 ${checked ? "translate-x-5" : "translate-x-0.5"}`} />
      </button>
    </div>
  );
}

function Field({ label, value, onChange, type = "text", placeholder }: {
  label: string; value: string; onChange: (v: string) => void; type?: string; placeholder?: string;
}) {
  return (
    <div className="space-y-1.5">
      <label className="text-xs font-medium text-neutral-400">{label}</label>
      <input
        type={type} value={value} onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-neutral-900 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder:text-neutral-600 focus:outline-none focus:border-violet-500/50 transition-colors"
      />
    </div>
  );
}

function SelectField({ label, value, options, onChange }: {
  label: string; value: string; options: string[]; onChange: (v: string) => void;
}) {
  return (
    <div className="space-y-1.5">
      <label className="text-xs font-medium text-neutral-400">{label}</label>
      <select
        value={value} onChange={(e) => onChange(e.target.value)}
        className="w-full bg-neutral-900 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-violet-500/50 transition-colors cursor-pointer"
      >
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  );
}

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: "profile", label: "Profile", icon: "account_circle" },
  { id: "ai", label: "AI & Automation", icon: "smart_toy" },
  { id: "security", label: "Security", icon: "lock" },
  { id: "notifications", label: "Notifications", icon: "notifications" },
];

export default function SettingsPage() {
  const { profile, profileId, setProfile } = useUserStore();
  const [tab, setTab] = useState<Tab>("profile");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Profile fields — pre-filled from real profile
  const [fullName, setFullName] = useState(profile?.full_name ?? "");
  const [email, setEmail] = useState(profile?.email ?? "");
  const [phone, setPhone] = useState(profile?.phone ?? "");
  const [location, setLocation] = useState(profile?.location ?? "");
  const [jobTitle, setJobTitle] = useState(profile?.job_title ?? "");
  const [github, setGithub] = useState(profile?.github_username ?? "");
  const [linkedin, setLinkedin] = useState(profile?.linkedin_url ?? "");
  const [portfolio, setPortfolio] = useState(profile?.portfolio_url ?? "");

  // AI preferences
  const sd = profile?.structured_data ?? {};
  const [matchThreshold, setMatchThreshold] = useState(String(sd.match_threshold ?? profile?.match_threshold ?? 80) + "%");
  const [tone, setTone] = useState(sd.cover_letter_tone ?? "Professional & Confident");
  const [dailyLimit, setDailyLimit] = useState(sd.daily_limit ?? "50 applications/day");
  const [autoApply, setAutoApply] = useState(sd.auto_apply ?? false);
  const [autoTailor, setAutoTailor] = useState(sd.auto_tailor ?? true);
  const [notifyBeforeApply, setNotifyBeforeApply] = useState(sd.notify_before_apply ?? true);

  // Security
  const [vaultEnabled, setVaultEnabled] = useState(true);
  const [sessionReuse, setSessionReuse] = useState(true);
  const [humanLoop, setHumanLoop] = useState(true);
  const [apiKey, setApiKey] = useState("sk-...");

  // Notifications
  const [matchNotif, setMatchNotif] = useState(true);
  const [appStatus, setAppStatus] = useState(true);
  const [captchaAlert, setCaptchaAlert] = useState(true);
  const [weeklyDigest, setWeeklyDigest] = useState(false);

  // Sync if profile loads after mount
  useEffect(() => {
    if (profile) {
      setFullName(profile.full_name ?? "");
      setEmail(profile.email ?? "");
      setPhone(profile.phone ?? "");
      setLocation(profile.location ?? "");
      setJobTitle(profile.job_title ?? "");
      setGithub(profile.github_username ?? "");
      setLinkedin(profile.linkedin_url ?? "");
      setPortfolio(profile.portfolio_url ?? "");
      const s = profile.structured_data ?? {};
      setMatchThreshold(String(s.match_threshold ?? profile.match_threshold ?? 80) + "%");
      setTone(s.cover_letter_tone ?? "Professional & Confident");
      setDailyLimit(s.daily_limit ?? "50 applications/day");
      setAutoApply(s.auto_apply ?? false);
      setAutoTailor(s.auto_tailor ?? true);
      setNotifyBeforeApply(s.notify_before_apply ?? true);
    }
  }, [profile]);

  const handleSave = async () => {
    if (!profileId) return;
    setSaving(true);
    setError(null);
    try {
      const threshold = parseInt(matchThreshold.replace("%", "")) || 80;
      const result = await updateProfile(profileId, {
        full_name: fullName,
        email,
        phone,
        location,
        job_title: jobTitle,
        github_username: github,
        linkedin_url: linkedin,
        portfolio_url: portfolio,
        match_threshold: threshold,
      });
      setProfile(result.profile);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Save failed. Please try again.");
    }
    setSaving(false);
  };

  return (
    <div className="max-w-4xl mx-auto animate-fade-in space-y-6">
      <div>
        <h1 className="text-xl font-bold text-white">Settings</h1>
        <p className="text-xs text-neutral-500 mt-1">Manage your AI Job Hunter OS configuration</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-neutral-800">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-t-lg transition-all duration-150 border-b-2 -mb-px ${
              tab === t.id
                ? "text-violet-400 border-violet-500"
                : "text-neutral-500 border-transparent hover:text-neutral-300"
            }`}
          >
            <span className="material-icons-round text-[16px]">{t.icon}</span>
            {t.label}
          </button>
        ))}
      </div>

      <div className="card p-6">
        {/* Profile Tab */}
        {tab === "profile" && (
          <>
            <SectionHeader icon="account_circle" title="Identity Profile" desc="Your information used by AI agents across all applications." />
            <div className="grid grid-cols-2 gap-4">
              <Field label="Full Name" value={fullName} onChange={setFullName} placeholder="Alex Johnson" />
              <Field label="Email" type="email" value={email} onChange={setEmail} placeholder="alex@gmail.com" />
              <Field label="Phone" type="tel" value={phone} onChange={setPhone} placeholder="+1 555 000 0000" />
              <Field label="Location" value={location} onChange={setLocation} placeholder="San Francisco, CA" />
              <div className="col-span-2">
                <Field label="Current / Target Job Title" value={jobTitle} onChange={setJobTitle} placeholder="e.g. Senior Software Engineer" />
              </div>
              <Field label="GitHub Username" value={github} onChange={setGithub} placeholder="your-username" />
              <Field label="Portfolio URL" value={portfolio} onChange={setPortfolio} placeholder="yoursite.dev" />
              <div className="col-span-2">
                <Field label="LinkedIn URL" value={linkedin} onChange={setLinkedin} placeholder="linkedin.com/in/yourprofile" />
              </div>
            </div>
          </>
        )}

        {/* AI Tab */}
        {tab === "ai" && (
          <>
            <SectionHeader icon="smart_toy" title="AI & Automation Settings" desc="Control how the Hunter AI analyzes jobs and submits applications." />
            <div className="grid grid-cols-2 gap-4 mb-6">
              <SelectField
                label="Match Score Threshold"
                value={matchThreshold}
                options={["60%", "70%", "75%", "80%", "85%", "90%", "95%"]}
                onChange={setMatchThreshold}
              />
              <SelectField
                label="Cover Letter Tone"
                value={tone}
                options={["Professional & Confident", "Enthusiastic", "Formal", "Concise & Direct", "Creative"]}
                onChange={setTone}
              />
              <SelectField
                label="Daily Application Limit"
                value={dailyLimit}
                options={["10 applications/day", "25 applications/day", "50 applications/day", "100 applications/day", "Unlimited"]}
                onChange={setDailyLimit}
              />
            </div>
            <div className="space-y-1">
              <Toggle label="Auto-Apply Mode" sub="Automatically queue jobs above the match threshold" checked={autoApply} onChange={() => setAutoApply(!autoApply)} />
              <Toggle label="Auto-Tailor Resume" sub="Dynamically rewrite resume bullets for each job" checked={autoTailor} onChange={() => setAutoTailor(!autoTailor)} />
              <Toggle label="Confirm Before Submitting" sub="Pause and notify before final submission" checked={notifyBeforeApply} onChange={() => setNotifyBeforeApply(!notifyBeforeApply)} />
            </div>
          </>
        )}

        {/* Security Tab */}
        {tab === "security" && (
          <>
            <SectionHeader icon="lock" title="Security & Privacy" desc="Manage how credentials and sessions are stored." />
            <div className="mb-6 space-y-1">
              <Toggle label="Encrypted Credential Vault" sub="Credentials stored using AES-256 Fernet encryption" checked={vaultEnabled} onChange={() => setVaultEnabled(!vaultEnabled)} />
              <Toggle label="Session Reuse" sub="Reuse authenticated browser contexts to avoid repeated logins" checked={sessionReuse} onChange={() => setSessionReuse(!sessionReuse)} />
              <Toggle label="Human-in-the-Loop" sub="Always pause and notify you before final form submission" checked={humanLoop} onChange={() => setHumanLoop(!humanLoop)} />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-neutral-400">OpenAI API Key</label>
              <div className="flex gap-2">
                <input
                  type="password" value={apiKey} onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="flex-1 bg-neutral-900 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder:text-neutral-600 focus:outline-none focus:border-violet-500/50 font-mono"
                />
                <button className="btn-secondary text-xs px-3">Verify</button>
              </div>
              <p className="text-[10px] text-neutral-600">Key is read from your .env file at startup. This field is for reference only.</p>
            </div>
          </>
        )}

        {/* Notifications Tab */}
        {tab === "notifications" && (
          <>
            <SectionHeader icon="notifications" title="Notification Preferences" desc="Control when the Hunter AI alerts you." />
            <div className="space-y-1">
              <Toggle label="High Match Found" sub="Alert when a new job exceeds your match threshold" checked={matchNotif} onChange={() => setMatchNotif(!matchNotif)} />
              <Toggle label="Application Status Changed" sub="Notify when a submitted application status updates" checked={appStatus} onChange={() => setAppStatus(!appStatus)} />
              <Toggle label="CAPTCHA / Human Review Required" sub="Alert when the automation engine needs your help" checked={captchaAlert} onChange={() => setCaptchaAlert(!captchaAlert)} />
              <Toggle label="Weekly Performance Digest" sub="Summary each Monday" checked={weeklyDigest} onChange={() => setWeeklyDigest(!weeklyDigest)} />
            </div>
          </>
        )}
      </div>

      {/* Save Footer */}
      <div className="flex items-center justify-end gap-3">
        {error && (
          <span className="text-red-400 text-xs">{error}</span>
        )}
        {saved && (
          <span className="flex items-center gap-1.5 text-emerald-400 text-sm animate-fade-in">
            <span className="material-icons-round text-[16px]">check_circle</span>
            Saved successfully
          </span>
        )}
        <button onClick={handleSave} disabled={saving} className="btn-primary flex items-center gap-2">
          {saving ? (
            <><span className="material-icons-round text-[16px] animate-spin-slow">sync</span> Saving...</>
          ) : (
            <><span className="material-icons-round text-[16px]">save</span> Save Changes</>
          )}
        </button>
      </div>
    </div>
  );
}
