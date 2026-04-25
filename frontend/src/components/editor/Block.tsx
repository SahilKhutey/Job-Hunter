"use client";

import { useRef, KeyboardEvent } from "react";
import { useEditor, Block, BlockType } from "@/store/useEditor";
import { rewriteBlock } from "@/lib/ai";

const BLOCK_STYLES: Record<BlockType, string> = {
  heading1: "text-2xl font-bold text-gray-900 w-full bg-transparent outline-none resize-none",
  heading2: "text-base font-bold text-gray-700 uppercase tracking-widest w-full bg-transparent outline-none resize-none",
  text: "text-sm text-gray-700 leading-relaxed w-full bg-transparent outline-none resize-none",
  bullet: "text-sm text-gray-700 leading-relaxed w-full bg-transparent outline-none resize-none pl-2",
  divider: "w-full h-px bg-gray-200 my-2 cursor-default",
};

const BLOCK_TYPE_LABELS: Record<BlockType, string> = {
  heading1: "H1", heading2: "H2", text: "P", bullet: "•", divider: "—",
};

interface BlockProps {
  block: Block;
  isFocused: boolean;
  onFocus: () => void;
}

export default function BlockEditor({ block, isFocused, onFocus }: BlockProps) {
  const { updateBlock, updateBlockType, addBlock, removeBlock, moveBlock, setRewriting, rewritingId } = useEditor();
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isRewriting = rewritingId === block.id;

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      addBlock(block.id, block.type === "bullet" ? "bullet" : "text");
    }
    if (e.key === "Backspace" && block.content === "") {
      e.preventDefault();
      removeBlock(block.id);
    }
  };

  const handleAIRewrite = async () => {
    if (!block.content.trim()) return;
    setRewriting(block.id);
    try {
      const rewritten = await rewriteBlock(block.content);
      updateBlock(block.id, rewritten);
    } finally {
      setRewriting(null);
    }
  };

  if (block.type === "divider") {
    return <hr className="border-gray-200 my-3" />;
  }

  return (
    <div
      className={`group relative flex gap-2 items-start py-1 px-2 rounded-lg transition-all border border-transparent ${isFocused ? "bg-violet-50/50 border-violet-100 shadow-sm" : "hover:bg-neutral-50 hover:border-neutral-100"}`}
      onClick={onFocus}
    >
      {/* Bullet marker */}
      {block.type === "bullet" && (
        <span className="shrink-0 text-gray-400 text-sm mt-0.5 ml-1 select-none">•</span>
      )}

      {/* Content textarea */}
      <textarea
        ref={textareaRef}
        value={block.content}
        rows={1}
        onChange={(e) => {
          updateBlock(block.id, e.target.value);
          // Auto-resize
          e.target.style.height = "auto";
          e.target.style.height = e.target.scrollHeight + "px";
        }}
        onKeyDown={handleKeyDown}
        onFocus={onFocus}
        placeholder={
          block.type === "heading1" ? "Name" :
          block.type === "heading2" ? "Section heading..." :
          block.type === "bullet" ? "List item..." : "Write something..."
        }
        className={`${BLOCK_STYLES[block.type]} overflow-hidden`}
        style={{ height: "auto" }}
      />

      {/* Floating toolbar (shows on focus) */}
      {isFocused && (
        <div className="absolute right-0 -top-8 flex items-center gap-1 bg-white border border-gray-200 rounded-lg shadow-xl px-1.5 py-1 z-50 animate-slide-up border-b-2 border-b-violet-500">
          {/* Block type picker */}
          <select
            value={block.type}
            onChange={(e) => updateBlockType(block.id, e.target.value as BlockType)}
            className="text-[10px] font-bold text-violet-600 bg-transparent border-none outline-none cursor-pointer uppercase tracking-tighter"
          >
            {(Object.keys(BLOCK_TYPE_LABELS) as BlockType[]).map((t) => (
              <option key={t} value={t}>{BLOCK_TYPE_LABELS[t]}</option>
            ))}
          </select>
          <div className="w-px h-4 bg-gray-200 mx-1" />
          {/* Move */}
          <button onClick={() => moveBlock(block.id, "up")} className="text-gray-400 hover:text-violet-600 p-0.5" title="Move up">
            <span className="material-icons-round text-[14px]">expand_less</span>
          </button>
          <button onClick={() => moveBlock(block.id, "down")} className="text-gray-400 hover:text-violet-600 p-0.5" title="Move down">
            <span className="material-icons-round text-[14px]">expand_more</span>
          </button>
          <div className="w-px h-4 bg-gray-200 mx-1" />
          {/* AI Rewrite */}
          <button
            onClick={handleAIRewrite}
            disabled={isRewriting}
            className="flex items-center gap-1 text-[10px] font-bold text-violet-600 hover:text-violet-800 disabled:opacity-50 px-1.5 py-0.5 rounded-md bg-violet-50"
          >
            <span className="material-icons-round text-[12px]">{isRewriting ? "sync" : "auto_fix_high"}</span>
            {isRewriting ? "REWRITING..." : "AI TAILOR"}
          </button>
          <div className="w-px h-4 bg-gray-200 mx-1" />
          {/* Delete */}
          <button onClick={() => removeBlock(block.id)} className="text-gray-300 hover:text-red-500 transition-colors p-0.5" title="Delete block">
            <span className="material-icons-round text-[14px]">delete</span>
          </button>
        </div>
      )}
    </div>
  );
}
