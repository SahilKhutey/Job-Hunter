export default function ActivityFeed() {
  return (
    <div className="bg-neutral-900 p-6 rounded-xl border border-neutral-800 mt-6 h-64">
      <h3 className="font-bold mb-4">Live Agent Activity</h3>
      <div className="text-sm text-neutral-400 space-y-2">
        <p>[10:45 AM] ExecutionAgent: Flagged job "Senior React Developer" as AUTO_APPLY_READY.</p>
        <p>[10:46 AM] ApplicationAgent: Generated Cover Letter for "Senior React Developer".</p>
        <p>[10:48 AM] System: Waiting for human confirmation to execute apply.</p>
      </div>
    </div>
  );
}
