import React from "react";

interface StepIndicatorProps {
  currentStep: number;
  steps: string[];
}

export default function StepIndicator({ currentStep, steps }: StepIndicatorProps) {
  return (
    <div className="flex items-center justify-between w-full max-w-2xl mx-auto mb-12">
      {steps.map((step, index) => {
        const isCompleted = index < currentStep - 1;
        const isActive = index === currentStep - 1;

        return (
          <React.Fragment key={index}>
            <div className="flex flex-col items-center relative">
              <div 
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500 shadow-lg ${
                  isCompleted ? "bg-emerald-500 border-emerald-500" : 
                  isActive ? "bg-violet-600 border-violet-600 scale-110" : 
                  "bg-neutral-900 border-neutral-800"
                }`}
              >
                {isCompleted ? (
                  <span className="material-icons-round text-white text-xl">check</span>
                ) : (
                  <span className={`text-xs font-bold ${isActive ? "text-white" : "text-neutral-500"}`}>
                    {index + 1}
                  </span>
                )}
              </div>
              <p 
                className={`absolute top-12 text-[10px] font-bold uppercase tracking-widest whitespace-nowrap transition-colors duration-500 ${
                  isActive ? "text-violet-400" : isCompleted ? "text-emerald-400" : "text-neutral-600"
                }`}
              >
                {step}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div className="flex-1 h-[2px] bg-neutral-800 mx-4 relative overflow-hidden">
                <div 
                  className="absolute inset-0 bg-gradient-to-r from-violet-600 to-emerald-500 transition-transform duration-1000 origin-left"
                  style={{ transform: `scaleX(${isCompleted ? 1 : 0})` }}
                />
              </div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}
