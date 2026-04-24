import { create } from "zustand";
import { v4 as uuid } from "uuid";
import { ProfileData, JobData } from "@/lib/api";

export type BlockType = "heading1" | "heading2" | "text" | "bullet" | "divider";

export interface Block {
  id: string;
  type: BlockType;
  content: string;
}

interface EditorState {
  blocks: Block[];
  currentVariant: string;
  variants: Record<string, Block[]>;
  rewritingId: string | null;
  activeJob: JobData | null;
  
  updateBlock: (id: string, content: string) => void;
  updateBlockType: (id: string, type: BlockType) => void;
  addBlock: (afterId?: string, type?: BlockType) => void;
  removeBlock: (id: string) => void;
  moveBlock: (id: string, direction: "up" | "down") => void;
  setRewriting: (id: string | null) => void;
  setActiveJob: (job: JobData | null) => void;
  
  setVariant: (name: string) => void;
  initializeFromProfile: (profile: ProfileData) => void;
  exportToProfile: () => Partial<ProfileData>;
  clear: () => void;
}

export const useEditor = create<EditorState>((set, get) => ({
  blocks: [],
  currentVariant: "Standard",
  variants: {},
  rewritingId: null,
  activeJob: null,

  setActiveJob: (activeJob) => set({ activeJob }),

  updateBlock: (id, content) =>
    set((s) => ({ blocks: s.blocks.map((b) => (b.id === id ? { ...b, content } : b)) })),

  updateBlockType: (id, type) =>
    set((s) => ({ blocks: s.blocks.map((b) => (b.id === id ? { ...b, type } : b)) })),

  addBlock: (afterId, type = "text") =>
    set((s) => {
      const newBlock: Block = { id: uuid(), type, content: "" };
      if (!afterId) return { blocks: [...s.blocks, newBlock] };
      const idx = s.blocks.findIndex((b) => b.id === afterId);
      const updated = [...s.blocks];
      updated.splice(idx + 1, 0, newBlock);
      return { blocks: updated };
    }),

  removeBlock: (id) =>
    set((s) => ({ blocks: s.blocks.filter((b) => b.id !== id) })),

  moveBlock: (id, direction) =>
    set((s) => {
      const idx = s.blocks.findIndex((b) => b.id === id);
      if (idx === -1) return s;
      const updated = [...s.blocks];
      const target = direction === "up" ? idx - 1 : idx + 1;
      if (target < 0 || target >= updated.length) return s;
      [updated[idx], updated[target]] = [updated[target], updated[idx]];
      return { blocks: updated };
    }),

  setRewriting: (id) => set({ rewritingId: id }),

  setVariant: (name) => {
    const { variants, blocks, currentVariant } = get();
    // Save current blocks to old variant
    const updatedVariants = { ...variants, [currentVariant]: blocks };
    // Load new blocks
    const newBlocks = variants[name] || blocks;
    set({ variants: updatedVariants, currentVariant: name, blocks: newBlocks });
  },

  initializeFromProfile: (profile) => {
    const blocks: Block[] = [];

    // Header
    blocks.push({ id: uuid(), type: "heading1", content: profile.full_name });
    if (profile.job_title) {
      blocks.push({ id: uuid(), type: "text", content: profile.job_title });
    }
    
    // Summary
    if (profile.summary) {
      blocks.push({ id: uuid(), type: "text", content: profile.summary });
    } else if (profile.years_experience > 0) {
      blocks.push({ id: uuid(), type: "text", content: `Professional with ${profile.years_experience}+ years of experience.` });
    }

    // Experience
    if (profile.experience && profile.experience.length > 0) {
      blocks.push({ id: uuid(), type: "heading2", content: "Experience" });
      profile.experience.forEach(exp => {
        blocks.push({ id: uuid(), type: "text", content: `${exp.title} · ${exp.company} · ${exp.duration}` });
        if (exp.bullets) {
          exp.bullets.forEach(bullet => {
            blocks.push({ id: uuid(), type: "bullet", content: bullet });
          });
        }
      });
    }

    // Skills
    if (profile.skills && profile.skills.length > 0) {
      blocks.push({ id: uuid(), type: "heading2", content: "Skills" });
      blocks.push({ id: uuid(), type: "text", content: profile.skills.join(" · ") });
    }

    // Education
    if (profile.education && profile.education.length > 0) {
      blocks.push({ id: uuid(), type: "heading2", content: "Education" });
      profile.education.forEach(edu => {
        blocks.push({ id: uuid(), type: "text", content: `${edu.degree} · ${edu.institute} · ${edu.year}` });
      });
    }

    // Load from profile variants if they exist
    const variants: Record<string, Block[]> = {};
    if (profile.resume_variants) {
        Object.entries(profile.resume_variants).forEach(([name, b]) => {
            variants[name] = b as Block[];
        });
    }

    set({ blocks, variants, currentVariant: "Standard" });
  },

  exportToProfile: () => {
    const { blocks, variants, currentVariant } = get();
    const updatedVariants = { ...variants, [currentVariant]: blocks };
    
    const profile: any = {
      skills: [],
      experience: [],
      education: [],
      resume_variants: updatedVariants
    };

    let currentSection: "experience" | "education" | "skills" | null = null;
    let currentExp: any = null;

    blocks.forEach((b) => {
      if (b.type === "heading1") {
        profile.full_name = b.content;
      } else if (b.type === "heading2") {
        const lower = b.content.toLowerCase();
        if (lower.includes("experience")) {
          currentSection = "experience";
        } else if (lower.includes("education")) {
          currentSection = "education";
        } else if (lower.includes("skills")) {
          currentSection = "skills";
        } else {
          currentSection = null;
        }
      } else if (b.type === "text") {
        if (currentSection === "experience") {
          const parts = b.content.split("·").map((s) => s.trim());
          currentExp = { title: parts[0] || "", company: parts[1] || "", duration: parts[2] || "", bullets: [] };
          profile.experience.push(currentExp);
        } else if (currentSection === "education") {
          const parts = b.content.split("·").map((s) => s.trim());
          profile.education.push({ degree: parts[0] || "", institute: parts[1] || "", year: parts[2] || "" });
        } else if (currentSection === "skills") {
          profile.skills = b.content.split("·").map((s) => s.trim()).filter(Boolean);
        } else if (!profile.job_title && !profile.summary) {
           profile.job_title = b.content;
        } else if (!profile.summary) {
           profile.summary = b.content;
        }
      } else if (b.type === "bullet") {
        if (currentSection === "experience" && currentExp) {
          currentExp.bullets.push(b.content);
        }
      }
    });

    return profile;
  },

  clear: () => set({ blocks: [], variants: {}, currentVariant: "Standard" }),
}));
