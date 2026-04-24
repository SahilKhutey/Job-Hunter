const { contextBridge, ipcRenderer } = require('electron');

# Expose protected APIs to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {
    platform: process.platform,
    runLocalAutomation: (jobUrl, profileData, resumePath) => {
        return ipcRenderer.invoke('run-automation', { jobUrl, profileData, resumePath });
    },
    onAgentUpdate: (callback) => {
        ipcRenderer.on('agent-update', (event, data) => callback(data));
    }
});
