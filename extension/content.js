// HunterOS Heads-Up Display (HUD) Content Script

function injectHUD() {
  if (document.getElementById("hos-hud")) return;

  const hud = document.createElement("div");
  hud.id = "hos-hud";
  hud.innerHTML = `
    <div class="hos-hud-content">
      <div class="hos-hud-header">
        <span class="hos-hud-logo">HOS Intelligence</span>
        <div class="hos-hud-status" id="hos-status-dot"></div>
      </div>
      <div id="hos-hud-body">
        <p class="hos-hud-msg">Analyzing current listing...</p>
      </div>
      <div class="hos-hud-footer">
        <button id="hos-sync-btn">Force Sync</button>
      </div>
    </div>
  `;
  document.body.appendChild(hud);
  
  // Start Analysis
  analyzeCurrentPage();
}

async function analyzeCurrentPage() {
  const body = document.getElementById("hos-hud-body");
  const statusDot = document.getElementById("hos-status-dot");
  
  // Basic scraping for LinkedIn/Indeed
  const jobDescription = document.querySelector(".jobs-description__container, #jobDescriptionText")?.innerText;
  const jobTitle = document.querySelector(".jobs-unified-top-card__job-title, .jobsearch-JobInfoHeader-title")?.innerText;

  if (!jobDescription) {
    body.innerHTML = "<p class='hos-hud-msg'>Navigate to a job detail page to begin analysis.</p>";
    return;
  }

  statusDot.className = "hos-hud-status hos-status-busy";
  
  chrome.runtime.sendMessage({ 
    type: "ANALYZE_JOB", 
    jobData: { 
      description: jobDescription,
      title: jobTitle,
      url: window.location.href
    } 
  }, (response) => {
    if (response.error) {
      statusDot.className = "hos-hud-status hos-status-error";
      body.innerHTML = `<p class='hos-hud-error'>${response.message}</p>`;
    } else {
      statusDot.className = "hos-hud-status hos-status-ready";
      renderAnalysis(response);
    }
  });
}

function renderAnalysis(data) {
  const body = document.getElementById("hos-hud-body");
  const score = data.match_score || 0;
  const scoreColor = score > 80 ? "#10b981" : score > 60 ? "#f59e0b" : "#ef4444";

  body.innerHTML = `
    <div class="hos-analysis">
      <div class="hos-score-circle" style="border-color: ${scoreColor}">
        <span class="hos-score-val">${score}%</span>
      </div>
      <div class="hos-skill-section">
        <p class="hos-section-label">Missing Skills</p>
        <div class="hos-skill-list">
          ${(data.missing_skills || []).map(s => `<span class="hos-skill-tag">${s}</span>`).join("")}
        </div>
      </div>
      <div class="hos-action-section">
        <p class="hos-advice">${data.upskill_advice || "Ready for deployment."}</p>
      </div>
    </div>
  `;
}

// Initialize
setTimeout(injectHUD, 2000);
