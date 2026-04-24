import Link from 'next/link';
import { Home, Briefcase, FileText, User, Settings, Activity } from 'lucide-react';

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-800 h-screen flex flex-col p-4">
      <div className="flex items-center gap-3 mb-10 px-2">
        <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <span className="text-xl font-bold text-white tracking-tight">AI Job Hunter</span>
      </div>

      <nav className="flex flex-col gap-2 flex-grow">
        <Link href="/" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
          <Home className="w-5 h-5" /> Dashboard
        </Link>
        <Link href="/jobs" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
          <Briefcase className="w-5 h-5" /> Job Feed
        </Link>
        <Link href="/applications" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
          <FileText className="w-5 h-5" /> App Studio
        </Link>
        <Link href="/profile" className="flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors">
          <User className="w-5 h-5" /> Profile Studio
        </Link>
      </nav>

      <div className="mt-auto">
        <Link href="/settings" className="flex items-center gap-3 px-3 py-2 text-gray-500 hover:text-gray-300 rounded-md transition-colors">
          <Settings className="w-5 h-5" /> Settings
        </Link>
      </div>
    </div>
  );
}
