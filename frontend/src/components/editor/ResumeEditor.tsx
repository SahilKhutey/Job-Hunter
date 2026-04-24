"use client";

import { useState } from "react";
import { useEditor } from "@/store/useEditor";
import { useUserStore } from "@/store/useUserStore";
import { updateProfile } from "@/lib/api";
import BlockEditor from "./Block";

export default function ResumeEditor() {
  const { blocks, addBlock, exportToProfile, currentVariant, setVariant, variants } = useEditor();
  const { profileId, setProfile } = useUserStore();
  const [focusedId, setFocusedId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [showVariants, setShowVariants] = useState(false);

  const handleSave = async () => {
    if (!profileId) return;
    setSaving(true);
    try {
      const data = exportToProfile();
      const result = await updateProfile(profileId, data);
      setProfile(result.profile);
    } catch (e) {
      console.error("Save failed", e);
    }
    setSaving(false);
  };

  const allVariants = ["Standard", ...Object.keys(variants)].filter((v, i, a) => a.indexOf(v) === i);

  return (
    <div className="flex flex-col h-full">
      {/* Toolbar */}
      <div className="border-b border-neutral-800 px-5 py-3 flex items-center justify-between bg-neutral-900 rounded-t-2xl">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="material-icons-round text-violet-400 text-[20px]">description</span>
            <p className="text-sm font-bold text-white">Resume Studio</p>
          </div>

          <div className="h-4 w-px bg-neutral-800 mx-1" />

          {/* Variant Switcher */}
          <div className="relative">
            <button 
              onClick={() => setShowVariants(!showVariants)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-neutral-800 border border-neutral-700 hover:border-violet-500/50 transition-all group"
            >
              <span className="text-[10px] text-neutral-500 uppercase tracking-widest font-bold">Variant:</span>
              <span className="text-xs font-semibold text-violet-300">{currentVariant}</span>
              <span className="material-icons-round text-[16px] text-neutral-600 group-hover:text-violet-400 transition-colors">expand_more</span>
            </button>

            {showVariants && (
              <div className="absolute top-full left-0 mt-2 w-48 bg-neutral-900 border border-neutral-800 rounded-xl shadow-2xl z-50 p-1 animate-slide-up">
                {allVariants.map(v => (
                  <button
                    key={v}
                    onClick={() => {
                      setVariant(v);
                      setShowVariants(false);
                    }}
                    className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                      currentVariant === v ? "bg-violet-600 text-white" : "text-neutral-400 hover:bg-white/5 hover:text-white"
                    }`}
                  >
                    {v}
                  </button>
                ))}
                <div className="h-px bg-neutral-800 my-1" />
                <button 
                  onClick={() => {
                    const name = prompt("Enter variant name (e.g. 'Backend Engineer')");
                    if (name) {
                      setVariant(name);
                      setShowVariants(false);
                    }
                  }}
                  className="w-full text-left px-3 py-2 rounded-lg text-xs font-medium text-violet-400 hover:bg-violet-400/10 flex items-center gap-2"
                >
                  <span className="material-icons-round text-[14px]">add</span>
                  Create Variant
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleSave}
            disabled={saving}
            className="btn-primary text-xs py-1.5 flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 mr-2 shadow-glow-sm"
          >
            <span className="material-icons-round text-[14px]">{saving ? "sync" : "save"}</span> 
            {saving ? "Saving..." : "Save Profile"}
          </button>
          <button
            onClick={() => addBlock()}
            className="btn-secondary text-xs py-1.5 flex items-center gap-1.5"
          >
            <span className="material-icons-round text-[14px]">add</span> Add Block
          </button>
        </div>
      </div>

      {/* White paper editor */}
      <div
        className="flex-1 overflow-y-auto bg-neutral-950 p-10 flex justify-center custom-scrollbar"
        onClick={() => setFocusedId(null)}
      >
        <div
          className="bg-white w-full max-w-2xl p-16 rounded-sm shadow-2xl min-h-full transition-all duration-500 animate-fade-in"
          onClick={(e) => e.stopPropagation()}
        >
          {blocks.map((block) => (
            <BlockEditor
              key={block.id}
              block={block}
              isFocused={focusedId === block.id}
              onFocus={() => setFocusedId(block.id)}
            />
          ))}

          {/* Add block CTA */}
          <button
            onClick={() => addBlock()}
            className="mt-12 w-full text-left text-xs text-gray-300 hover:text-gray-400 border border-dashed border-gray-100 rounded-lg py-4 px-6 transition-all flex items-center gap-2 opacity-40 hover:opacity-100"
          >
            <span className="material-icons-round text-[16px]">add</span>
            Add a block (or press Enter in any block)
          </button>
        </div>
      </div>
    </div>
  );
}
