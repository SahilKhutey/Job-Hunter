interface ResumePreviewProps {
  resumeJson: any;
}

export default function ResumePreview({ resumeJson }: ResumePreviewProps) {
  if (!resumeJson) return <div className="text-gray-500 italic p-4">No resume data generated yet.</div>;

  return (
    <div className="bg-white text-gray-900 p-8 rounded-lg shadow-lg max-w-2xl mx-auto font-sans text-sm h-[800px] overflow-y-auto">
      <h1 className="text-2xl font-bold mb-2 uppercase tracking-wide">{resumeJson.full_name || 'Name'}</h1>
      <div className="flex gap-4 text-gray-600 mb-6 border-b pb-4 text-xs">
        {resumeJson.email && <span>{resumeJson.email}</span>}
        {resumeJson.phone && <span>• {resumeJson.phone}</span>}
        {resumeJson.linkedin && <span>• {resumeJson.linkedin}</span>}
      </div>

      {resumeJson.summary && (
        <div className="mb-6">
          <h2 className="text-sm font-bold text-gray-800 uppercase tracking-wider mb-2">Professional Summary</h2>
          <p className="text-gray-700 leading-relaxed">{resumeJson.summary}</p>
        </div>
      )}

      {resumeJson.skills && (
        <div className="mb-6">
          <h2 className="text-sm font-bold text-gray-800 uppercase tracking-wider mb-2">Core Competencies</h2>
          <p className="text-gray-700">{resumeJson.skills.join(', ')}</p>
        </div>
      )}

      {resumeJson.experience && (
        <div>
          <h2 className="text-sm font-bold text-gray-800 uppercase tracking-wider mb-3">Experience</h2>
          <div className="flex flex-col gap-5">
            {resumeJson.experience.map((exp: any, i: number) => (
              <div key={i}>
                <div className="flex justify-between items-baseline mb-1">
                  <h3 className="font-bold text-gray-900">{exp.role}</h3>
                  <span className="text-gray-500 text-xs">{exp.duration}</span>
                </div>
                <div className="text-gray-700 font-medium mb-2">{exp.company}</div>
                {Array.isArray(exp.description) ? (
                  <ul className="list-disc pl-5 text-gray-700 space-y-1">
                    {exp.description.map((bullet: string, j: number) => (
                      <li key={j}>{bullet}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-700">{exp.description}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
