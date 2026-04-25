const { chromium } = require('playwright');

/**
 * Local Execution Engine
 * Runs Playwright locally in the user's desktop environment.
 */
async function runAutomation(event, jobUrl, profileData, resumePath) {
    const sendUpdate = (msg) => {
        event.sender.send('agent-update', { 
            agent: "DesktopAgent", 
            status: "running", 
            message: msg,
            timestamp: new Date().toISOString()
        });
    };

    console.log(`Starting local automation for: ${jobUrl}`);
    sendUpdate(`Initializing local browser for ${jobUrl}...`);
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 100 
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });

    const page = await context.newPage();

    try {
        sendUpdate("Navigating to job page...");
        await page.goto(jobUrl, { waitUntil: 'networkidle' });
        
        sendUpdate("Page loaded. Analyzing form elements...");
        await page.waitForTimeout(2000);
        
        sendUpdate("Mapping profile fields locally...");
        # Here we could also call a local LLM or the same backend API for mapping
        
        await page.screenshot({ path: `automation_run_${Date.now()}.png` });
        sendUpdate("Application flow simulated. Screenshot captured.");

        return { success: true, message: "Local automation completed." };
    } catch (error) {
        sendUpdate(`Error: ${error.message}`);
        return { success: false, error: error.message };
    } finally {
        setTimeout(async () => {
            await browser.close();
        }, 5000);
    }
}

module.exports = { runAutomation };
