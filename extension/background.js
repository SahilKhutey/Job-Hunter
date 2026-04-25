// HunterOS Extension Background Service Worker
const BASE_URL = "http://localhost:8000";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "ANALYZE_JOB") {
    handleJobAnalysis(request.jobData).then(sendResponse);
    return true; // Keep channel open for async response
  }
});

async function handleJobAnalysis(jobData) {
  try {
    const { extensionToken } = await chrome.storage.local.get("extensionToken");
    
    if (!extensionToken) {
      return { error: "AUTH_REQUIRED", message: "Please set your Handshake Token in the extension settings." };
    }

    const response = await fetch(`${BASE_URL}/extension/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-HOS-Extension-Token": extensionToken
      },
      body: JSON.stringify(jobData)
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Analysis Error:", error);
    return { error: "ANALYSIS_FAILED", message: error.message };
  }
}
