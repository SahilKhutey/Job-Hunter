import { Play, FileText, CheckCircle2 } from 'lucide-react';
import { useJobStore } from '../store/useJobStore';

interface JobCardProps {
  job: {
    id: number;
    title: string;
    company: string;
    url: string;
    match_score: number;
    ai_decision: string;
  };
}

export default function JobCard({ job }: JobCardProps) {
  const setActiveJob = useJobStore((state) => state.setActiveJob);
  const isAutoApply = job.ai_decision === 'AUTO_APPLY_READY';

  return (
    <div 
      onClick={() => setActiveJob(job)}
      className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-indigo-500/50 cursor-pointer transition-all group relative overflow-hidden"
    >
      {/* Background Gradient Hint */}
      {isAutoApply && (
        <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 blur-3xl -mr-10 -mt-10 pointer-events-none"></div>
      )}

      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-100 group-hover:text-indigo-400 transition-colors">{job.title}</h3>
          <p className="text-sm text-gray-500">{job.company}</p>
        </div>
        <div className={`px-2.5 py-1 rounded-md text-xs font-bold border ${isAutoApply ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' : 'bg-gray-800 text-gray-400 border-gray-700'}`}>
          {(job.match_score * 100).toFixed(0)}% Match
        </div>
      </div>

      {job.match_analytics && job.match_analytics.missing_skills.length > 0 && (
        <div className="mb-4">
          <p className="text-[10px] uppercase tracking-wider text-gray-500 font-bold mb-2">Missing Skills</p>
          <div className="flex flex-wrap gap-1.5">
            {job.match_analytics.missing_skills.slice(0, 3).map(skill => (
              <span key={skill} className="px-1.5 py-0.5 bg-red-500/10 text-red-400 text-[10px] rounded border border-red-500/20">
                {skill}
              </span>
            ))}
            {job.match_analytics.missing_skills.length > 3 && (
              <span className="text-[10px] text-gray-500 mt-0.5">+{job.match_analytics.missing_skills.length - 3} more</span>
            )}
          </div>
        </div>
      )}

      <div className="flex items-center justify-between mt-6">
        <div className="flex items-center gap-2">
          {isAutoApply ? (
            <span className="flex items-center gap-1.5 text-xs font-medium text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
              <CheckCircle2 className="w-3.5 h-3.5" /> Ready to Apply
            </span>
          ) : (
            <span className="text-xs font-medium text-gray-500 bg-gray-800 px-2 py-1 rounded">
              Needs Review
            </span>
          )}
        </div>
        
        <div className="flex gap-2">
          <button className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
            <FileText className="w-4 h-4" />
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg transition-colors">
            <Play className="w-3.5 h-3.5" /> Start
          </button>
        </div>
      </div>
    </div>
  );
}
