import { Terminal, XCircle, CheckCircle, Loader2 } from 'lucide-react';
import { useAgentStore } from '../store/useAgentStore';

export default function AgentTerminal() {
  const { logs, status } = useAgentStore();

  return (
    <div className="bg-[#0D0D12] border border-gray-800 rounded-xl overflow-hidden flex flex-col h-64 font-mono text-sm">
      <div className="bg-gray-900 border-b border-gray-800 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-2 text-gray-400 text-xs">
          <Terminal className="w-4 h-4" />
          <span>Agent Execution Log</span>
        </div>
        <div className="flex items-center gap-2">
          {status === 'running' && <Loader2 className="w-3.5 h-3.5 text-indigo-400 animate-spin" />}
          {status === 'completed' && <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />}
          {status === 'error' && <XCircle className="w-3.5 h-3.5 text-red-400" />}
        </div>
      </div>
      
      <div className="p-4 overflow-y-auto flex-grow flex flex-col gap-1.5">
        {logs.length === 0 ? (
          <div className="text-gray-600 italic">Awaiting commands...</div>
        ) : (
          logs.map((log) => (
            <div key={log.id} className="flex items-start gap-3">
              <span className="text-gray-600 shrink-0">[{log.timestamp}]</span>
              <span className="text-indigo-400 shrink-0">[{log.agent}]</span>
              <span className="text-gray-300 break-words">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
