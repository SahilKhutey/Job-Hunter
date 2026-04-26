'use client';

import { useState } from 'react';
import { Search, MapPin, Loader2, Sparkles, Plus } from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import Topbar from '@/components/Topbar';
import { useJobStore } from '@/store/useJobStore';

export default function DiscoveryPage() {
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState('Remote');
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    setIsSearching(true);
    try {
      const response = await fetch(`http://localhost:8000/automation/discover?query=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}`, {
        method: 'POST'
      });
      const data = await response.json();
      
      // We simulate showing some immediate "potential" results 
      // even though the backend runs in background
      setResults([
        { id: 101, title: `${query} Specialist`, company: "TechFlow Systems", match: 0.88 },
        { id: 102, title: `Senior ${query}`, company: "NexGen AI", match: 0.74 },
        { id: 103, title: `Lead ${query} Developer`, company: "Global Connect", match: 0.92 }
      ]);
    } catch (error) {
      console.error("Discovery failed", error);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="flex h-screen bg-black text-white font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-5xl mx-auto">
            <div className="mb-12">
              <h1 className="text-4xl font-extrabold mb-4 bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                Autonomous Job Discovery
              </h1>
              <p className="text-gray-400 text-lg">
                Tell Hunter AI what you're looking for, and it will scan the web to find your next opportunity.
              </p>
            </div>

            {/* Search Bar */}
            <div className="bg-gray-900/50 border border-gray-800 p-8 rounded-3xl backdrop-blur-xl mb-12">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-widest px-1">Job Title / Keywords</label>
                  <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                    <input 
                      type="text" 
                      placeholder="e.g. Senior Python Engineer"
                      className="w-full bg-black border border-gray-800 rounded-2xl py-4 pl-12 pr-4 text-gray-200 focus:outline-none focus:border-indigo-500 transition-all"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-widest px-1">Location</label>
                  <div className="relative">
                    <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                    <input 
                      type="text" 
                      placeholder="e.g. Remote or San Francisco"
                      className="w-full bg-black border border-gray-800 rounded-2xl py-4 pl-12 pr-4 text-gray-200 focus:outline-none focus:border-indigo-500 transition-all"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                    />
                  </div>
                </div>
              </div>
              
              <button 
                onClick={handleSearch}
                disabled={isSearching || !query}
                className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-800 disabled:text-gray-500 py-4 rounded-2xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-500/20"
              >
                {isSearching ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" /> Hunter AI is searching...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" /> Launch Autonomous Discovery
                  </>
                )}
              </button>
            </div>

            {/* Results Grid */}
            {results.length > 0 && (
              <div>
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <span className="w-2 h-8 bg-indigo-500 rounded-full"></span>
                  Discovered Opportunities
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {results.map(job => (
                    <div key={job.id} className="bg-gray-900 border border-gray-800 p-6 rounded-3xl hover:border-indigo-500/50 transition-all group">
                      <div className="flex justify-between items-start mb-4">
                        <div className="w-10 h-10 rounded-xl bg-gray-800 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors">
                          <Briefcase className="w-5 h-5 text-indigo-400" />
                        </div>
                        <div className="text-xs font-bold text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
                          {Math.round(job.match * 100)}% Match
                        </div>
                      </div>
                      <h3 className="text-lg font-bold mb-1">{job.title}</h3>
                      <p className="text-sm text-gray-500 mb-6">{job.company}</p>
                      <button className="w-full py-2.5 bg-gray-800 hover:bg-gray-700 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-colors">
                        <Plus className="w-4 h-4" /> Add to Feed
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

// Helper icon for grid
function Briefcase({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
    </svg>
  );
}
