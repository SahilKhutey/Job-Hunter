"use client";

import { useEffect, useRef, useState } from "react";
import { useUserStore } from "@/store/useUserStore";
import { uploadResume, updateProfile, ProfileData } from "@/lib/api";

function Skeleton({ className }: { className?: string }) {
  return <div className={`bg-neutral-800 rounded-xl animate-pulse ${className}`} />;
}

function InfoChip({ icon, label }: { icon: string; label?: string }) {
  if (!label) return null;
  return (
    <div className="flex items-center gap-1.5 text-xs text-neutral-400">
      <span className="material-icons-round text-[14px] text-neutral-600">{icon}</span>
      {label}
    </div>
  );
}

function SkillBadge({ skill }: { skill: string }) {
  return (
    <span className="px-2.5 py-1 bg-violet-500/10 border border-violet-500/20 text-violet-300 rounded-lg text-xs font-medium">
      {skill}
    </span>
  );
}

function ScoreRing({ score, label }: { score: number; label: string }) {
  const r = 32, c = 2 * Math.PI * r;
  const offset = c - (score / 100) * c;
  return (
    <div className="flex flex-col items-center gap-1.5">
      <div className="relative w-20 h-20">
        <svg width="80" height="80" className="rotate-[-90deg]">
          <circle cx="40" cy="40" r={r} fill="none" stroke="#262626" strokeWidth="6" />
          <circle
            cx="40" cy="40" r={r} fill="none"
            stroke="url(#vg)" strokeWidth="6"
            strokeDasharray={c} strokeDashoffset={offset}
            strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 1s ease" }}
          />
          <defs>
            <linearGradient id="vg" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#7c3aed" />
              <stop offset="100%" stopColor="#a78bfa" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-bold text-white">{score}</span>
        </div>
      </div>
      <p className="text-[10px] text-neutral-500 text-center">{label}</p>
    </div>
  );
}

function computeCompleteness(profile: ProfileData): number {
  let score = 0;
  if (profile.full_name) score += 15;
  if (profile.email) score += 10;
  if (profile.phone) score += 5;
  if (profile.location) score += 5;
  if (profile.has_resume) score += 20;
  if ((profile.skills?.length ?? 0) > 3) score += 15;
  if ((profile.experience?.length ?? 0) > 0) score += 15;
  if ((profile.education?.length ?? 0) > 0) score += 10;
  if (profile.links?.github || profile.links?.linkedin) score += 5;
  return Math.min(score, 100);
}

export default function ProfileStudioPage() {
  const { profile, profileId, setProfile, loadProfile } = useUserStore();
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!profile && profileId) loadProfile(profileId);
  }, [profileId]);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !profileId) return;
    setUploading(true);
    setUploadMsg(null);
    try {
      const result = await uploadResume(profileId, file);
      setProfile(result.profile);
      setUploadMsg({ type: "success", text: "Resume extracted. Profile intelligence updated." });
    } catch (err: any) {
      setUploadMsg({
        type: "error",
        text: err?.response?.data?.detail ?? "Extraction failed. Check if your OPENAI_API_KEY is configured.",
      });
    }
    setUploading(false);
  };

  if (!profile) {
    return (
      <div className="max-w-5xl mx-auto space-y-5 animate-fade-in">
        <div className="grid grid-cols-3 gap-5">
          <div className="col-span-1 card p-5 space-y-4">
            <Skeleton className="w-16 h-16 rounded-2xl mx-auto" />
            <Skeleton className="h-4 w-32 mx-auto" />
            <Skeleton className="h-3 w-24 mx-auto" />
          </div>
          <div className="col-span-2 space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="card p-5 space-y-3">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-3 w-full" />
                <Skeleton className="h-3 w-3/4" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const completeness = computeCompleteness(profile);
  const atsScore = profile.has_resume ? Math.min(completeness + 10, 95) : 40;

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Profile Intelligence Studio</h1>
          <p className="text-xs text-neutral-500 mt-1">Your AI-structured knowledge graph that powers every application</p>
        </div>
        <div className="flex gap-2">
          <input ref={fileRef} type="file" className="hidden" accept=".pdf,.docx" onChange={handleUpload} />
          <button
            onClick={() => fileRef.current?.click()}
            disabled={uploading}
            className="btn-secondary flex items-center gap-2 text-sm"
          >
            {uploading ? (
              <><span className="material-icons-round text-[16px] animate-spin-slow">sync</span> Extracting...</>
            ) : (
              <><span className="material-icons-round text-[16px]">upload_file</span>
                {profile.has_resume ? "Re-upload Resume" : "Upload Resume"}</>
            )}
          </button>
          <button className="btn-primary flex items-center gap-2 text-sm">
            <span className="material-icons-round text-[16px]">auto_awesome</span>
            Re-analyze with AI
          </button>
        </div>
      </div>

      {uploadMsg && (
        <div className={`p-3 border rounded-xl text-sm flex items-center gap-2 animate-slide-up ${
          uploadMsg.type === "success"
            ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
            : "bg-amber-500/10 border-amber-500/20 text-amber-400"
        }`}>
          <span className="material-icons-round text-[16px]">
            {uploadMsg.type === "success" ? "check_circle" : "warning"}
          </span>
          {uploadMsg.text}
        </div>
      )}

      {!profile.has_resume && (
        <div
          onClick={() => fileRef.current?.click()}
          className="border-2 border-dashed border-violet-500/30 bg-violet-500/5 rounded-2xl p-6 flex items-center gap-4 cursor-pointer hover:border-violet-500/50 hover:bg-violet-500/10 transition-all"
        >
          <span className="material-icons-round text-violet-400 text-[32px]">upload_file</span>
          <div>
            <p className="font-semibold text-white text-sm">Upload your resume to unlock AI intelligence</p>
            <p className="text-xs text-neutral-500 mt-0.5">PDF or DOCX — skills, experience, and education are extracted automatically</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-5">
        {/* Identity Card */}
        <div className="col-span-1 card p-5 flex flex-col gap-4">
          <div className="flex flex-col items-center text-center gap-2 pb-4 border-b border-neutral-800">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-700 flex items-center justify-center text-2xl font-bold text-white shadow-glow-sm">
              {profile.full_name?.charAt(0)?.toUpperCase() ?? "?"}
            </div>
            <div>
              <h2 className="font-bold text-white">{profile.full_name}</h2>
              <p className="text-xs text-neutral-500 mt-0.5">
                {profile.job_title ?? "No title set"} · {profile.location ?? "No location"}
              </p>
            </div>
          </div>

          <div className="space-y-2.5">
            <InfoChip icon="email" label={profile.email} />
            <InfoChip icon="phone" label={profile.phone} />
            <InfoChip icon="location_on" label={profile.location} />
            {profile.links?.github && <InfoChip icon="link" label={profile.links.github} />}
            {profile.links?.linkedin && <InfoChip icon="work_outline" label={profile.links.linkedin} />}
            {profile.links?.portfolio && <InfoChip icon="language" label={profile.links.portfolio} />}
          </div>

          <div className="pt-4 border-t border-neutral-800">
            <p className="text-[10px] uppercase tracking-wider text-neutral-600 font-semibold mb-3">AI Profile Scores</p>
            <div className="flex justify-around">
              <ScoreRing score={completeness} label="Completeness" />
              <ScoreRing score={atsScore} label="ATS Score" />
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="col-span-2 space-y-4">
          {/* Skills */}
          <div className="card p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-white text-sm">Extracted Skills</h3>
              <span className="text-[10px] text-neutral-600">
                {profile.skills?.length ?? 0} detected
              </span>
            </div>
            {(profile.skills?.length ?? 0) > 0 ? (
              <div className="flex flex-wrap gap-2">
                {profile.skills.map((s) => <SkillBadge key={s} skill={s} />)}
              </div>
            ) : (
              <p className="text-xs text-neutral-600">No skills detected yet — upload your resume to extract them automatically.</p>
            )}
          </div>

          {/* Experience */}
          <div className="card p-5">
            <h3 className="font-semibold text-white text-sm mb-4">Work Experience</h3>
            {(profile.experience?.length ?? 0) > 0 ? (
              <div className="space-y-4">
                {profile.experience.map((exp, i) => (
                  <div key={i} className="flex gap-4 pb-4 border-b border-neutral-800/60 last:border-0 last:pb-0">
                    <div className="w-8 h-8 rounded-xl bg-violet-500/10 flex items-center justify-center shrink-0 mt-0.5">
                      <span className="material-icons-round text-violet-400 text-[16px]">business</span>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-baseline justify-between gap-2">
                        <p className="font-semibold text-sm text-white">{exp.title}</p>
                        <span className="text-[10px] text-neutral-600 shrink-0">{exp.duration}</span>
                      </div>
                      <p className="text-xs text-neutral-500 mb-2">{exp.company}</p>
                      {exp.bullets?.length > 0 && (
                        <ul className="space-y-1">
                          {exp.bullets.map((b, j) => (
                            <li key={j} className="text-xs text-neutral-400 flex items-start gap-2">
                              <span className="w-1 h-1 rounded-full bg-violet-500 mt-1.5 shrink-0" />
                              {b}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-neutral-600">No experience extracted. Upload your resume to populate this section.</p>
            )}
          </div>

          {/* Education */}
          <div className="card p-5">
            <h3 className="font-semibold text-white text-sm mb-4">Education</h3>
            {(profile.education?.length ?? 0) > 0 ? (
              profile.education.map((edu, i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-xl bg-sky-500/10 flex items-center justify-center shrink-0">
                    <span className="material-icons-round text-sky-400 text-[16px]">school</span>
                  </div>
                  <div>
                    <p className="font-semibold text-sm text-white">{edu.degree}</p>
                    <p className="text-xs text-neutral-500">{edu.institute} · {edu.year}</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-neutral-600">No education data yet. Upload your resume to extract it.</p>
            )}
          </div>

          {/* Preferences */}
          <div className="card p-5">
            <h3 className="font-semibold text-white text-sm mb-4">Job Preferences</h3>
            <div className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm">
              <div>
                <p className="text-[10px] text-neutral-600 uppercase tracking-wider">Target Roles</p>
                <p className="text-neutral-300 mt-1">
                  {profile.target_roles?.length > 0 ? profile.target_roles.join(", ") : "Not set"}
                </p>
              </div>
              <div>
                <p className="text-[10px] text-neutral-600 uppercase tracking-wider">Remote Preference</p>
                <p className="text-neutral-300 mt-1">{profile.remote_preference ?? "Any"}</p>
              </div>
              <div>
                <p className="text-[10px] text-neutral-600 uppercase tracking-wider">Match Threshold</p>
                <p className="text-violet-400 font-bold mt-1">{profile.match_threshold ?? 80}%</p>
              </div>
              <div>
                <p className="text-[10px] text-neutral-600 uppercase tracking-wider">Preferred Locations</p>
                <p className="text-neutral-300 mt-1">
                  {profile.preferred_locations?.length > 0 ? profile.preferred_locations.join(", ") : "Any"}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
