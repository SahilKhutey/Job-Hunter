# 📱 Cross-Platform Architecture: AI Job Hunter OS

Job Hunter OS is designed as a distributed ecosystem where each platform serves a specific role in the autonomous career lifecycle.

## 🏗️ Platform Mapping

| Feature | Web (Universal) | Mobile (Control) | Desktop (Execution) |
| :--- | :---: | :---: | :---: |
| **Profile & Resume Builder** | ✅ | ✅ | ✅ |
| **Job Feed & Discovery** | ✅ | ✅ | ✅ |
| **Analytics Dashboard** | ✅ | ✅ | ✅ |
| **Automation Monitoring** | ✅ | ✅ | ✅ |
| **Automation Execution** | ❌ (Server-side) | ❌ | ✅ (Local/Power Mode) |
| **Persistent Sessions** | ❌ | ❌ | ✅ |

---

## 🖥️ Desktop (Electron)
**Purpose**: The "Execution Engine."
- **Why**: Desktop environments are the only ones that can reliably run Playwright automation with persistent browser profiles and full OS-level file access for resumes.
- **Stealth**: Harder to detect than server-side automation.
- **Tech Stack**: Electron + Next.js (Wrapped).

## 📱 Mobile (React Native + Expo)
**Purpose**: "Mission Control."
- **Why**: Used for real-time notifications when an agent finds a match or completes an application.
- **Control**: Start/Stop agents and review AI-generated tailored resumes on the go.
- **Tech Stack**: React Native, Expo, Reanimated.

## 🌐 Web (Next.js)
**Purpose**: "Universal Hub."
- **Why**: SEO-friendly landing pages, user acquisition, and a fallback for users without the desktop app.
- **Tech Stack**: Next.js 15, Tailwind CSS, Framer Motion.

---

## 🚀 Rollout Roadmap
1. **Web**: Core dashboard and profile hydration.
2. **Desktop**: Playwright agent execution and local storage.
3. **Mobile**: Real-time observability and remote agent triggering.
