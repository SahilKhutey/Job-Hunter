export default function StatsCard({ title, value }: any) {
  return (
    <div className="bg-neutral-900 p-6 rounded-xl border border-neutral-800">
      <p className="text-sm text-neutral-400">{title}</p>
      <h2 className="text-2xl font-bold">{value}</h2>
    </div>
  );
}
