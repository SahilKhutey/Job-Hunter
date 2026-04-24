"use client";

import { useState } from 'react';
import ResumePreview from '@/components/ResumePreview';
import { useUserStore } from '@/store/useUserStore';
import { FileText, MessageSquare, Save, Play } from 'lucide-react';

export default function ApplicationStudio() {
  const [activeTab, setActiveTab] = useState<'resume' | 'cover_letter'>('resume');
  const user = useUserStore((state) => state.user);

  // Mock JSON resume for UI
  const mockResume = {
    full_name: user?.full_name || "Sahil Khutey",
    skills: user?.skills || ["Python", "React", "Docker"],
    experience: [
      { role: "Senior Engineer", company: "TechCorp", duration: "2021 - Present", description: "Led backend team building FastAPI microservices." }
    ]
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <FileText className="w-6 h-6 text-indigo-500" /> Application Studio
          </h1>
          <p className="text-sm text-gray-400 mt-1">Reviewing tailored assets for: <strong className="text-white">Senior Python Engineer @ StartupX</strong></p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors border border-gray-700">
            <Save className="w-4 h-4" /> Save Draft
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium transition-colors shadow-lg shadow-indigo-500/20">
            <Play className="w-4 h-4" /> Execute Auto-Apply
          </button>
        </div>
      </div>

      <div className="flex-1 flex gap-6 overflow-hidden">
        {/* Editor Panel */}
        <div className="w-1/3 flex flex-col gap-4">
          <div className="flex bg-gray-900 p-1 rounded-lg border border-gray-800">
            <button 
              onClick={() => setActiveTab('resume')}
              className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'resume' ? 'bg-gray-800 text-white shadow-sm' : 'text-gray-400 hover:text-gray-200'}`}
            >
              Resume JSON
            </button>
            <button 
              onClick={() => setActiveTab('cover_letter')}
              className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'cover_letter' ? 'bg-gray-800 text-white shadow-sm' : 'text-gray-400 hover:text-gray-200'}`}
            >
              Cover Letter
            </button>
          </div>

          <div className="flex-1 bg-[#1E1E1E] border border-gray-800 rounded-xl p-4 overflow-y-auto font-mono text-sm text-gray-300">
            {activeTab === 'resume' ? (
              <pre>{JSON.stringify(mockResume, null, 2)}</pre>
            ) : (
              <div className="whitespace-pre-wrap font-sans text-base leading-relaxed text-gray-300">
                Dear Hiring Manager,\n\nI am thrilled to apply for the Senior Python Engineer role at StartupX. My background in building high-performance APIs directly aligns with your current infrastructure goals...
              </div>
            )}
          </div>
          
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
             <div className="flex items-center gap-2 mb-3 text-indigo-400 text-sm font-medium">
               <MessageSquare className="w-4 h-4" /> AI Adjustments
             </div>
             <input type="text" placeholder="E.g. Make the cover letter shorter..." className="w-full bg-gray-950 border border-gray-800 rounded-lg py-2 px-3 text-sm text-gray-200 focus:outline-none focus:border-indigo-500" />
          </div>
        </div>

        {/* Visual Preview Panel */}
        <div className="w-2/3 bg-gray-300 rounded-xl overflow-hidden flex items-center justify-center p-8 relative">
          <div className="absolute top-4 left-4 bg-gray-900 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg">
            Live PDF Preview
          </div>
          {activeTab === 'resume' ? (
             <ResumePreview resumeJson={mockResume} />
          ) : (
            <div className="bg-white text-gray-900 p-12 rounded-lg shadow-xl w-[80%] max-w-2xl h-[800px] overflow-y-auto">
               <h1 className="text-xl font-bold mb-8">{mockResume.full_name}</h1>
               <p className="whitespace-pre-wrap leading-relaxed text-gray-700">
                  Dear Hiring Manager,\n\nI am thrilled to apply for the Senior Python Engineer role at StartupX. My background in building high-performance APIs directly aligns with your current infrastructure goals.\n\nThank you for your time.\n\nBest,\n{mockResume.full_name}
               </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
