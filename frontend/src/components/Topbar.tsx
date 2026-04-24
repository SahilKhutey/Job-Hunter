import { Bell, Search, UserCircle } from 'lucide-react';
import { useUserStore } from '../store/useUserStore';

export default function Topbar() {
  const user = useUserStore((state) => state.user);

  return (
    <header className="h-16 border-b border-gray-800 bg-gray-950 flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-4 w-1/3">
        <div className="relative w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
          <input 
            type="text" 
            placeholder="Search jobs, skills, or companies..." 
            className="w-full bg-gray-900 border border-gray-800 rounded-full py-1.5 pl-10 pr-4 text-sm text-gray-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>
      </div>

      <div className="flex items-center gap-5">
        <button className="relative text-gray-400 hover:text-white transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-indigo-500 rounded-full border-2 border-gray-950"></span>
        </button>
        
        <div className="flex items-center gap-3 pl-5 border-l border-gray-800">
          <div className="text-right">
            <p className="text-sm font-medium text-white">{user?.full_name || 'Guest'}</p>
            <p className="text-xs text-indigo-400">Copilot Active</p>
          </div>
          <UserCircle className="w-8 h-8 text-gray-400" />
        </div>
      </div>
    </header>
  );
}
