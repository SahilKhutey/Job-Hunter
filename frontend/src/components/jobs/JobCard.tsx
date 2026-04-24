export default function JobCard({ job }: any) {
  return (
    <div className="bg-neutral-900 p-4 rounded-xl border border-neutral-800 hover:scale-[1.02] transition">
      <h3 className="font-bold">{job.title}</h3>
      <p className="text-sm text-neutral-400">{job.company}</p>
      <div className="mt-4 flex gap-2">
        <button className="bg-indigo-600 px-3 py-1 rounded">
          Apply
        </button>
        <button className="bg-neutral-700 px-3 py-1 rounded">
          Save
        </button>
      </div>
    </div>
  );
}
