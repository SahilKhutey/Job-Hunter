const { app, BrowserWindow, shell } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1280,
        height: 800,
        title: "AI Job Hunter OS - Desktop",
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        icon: path.join(__dirname, 'assets/icon.png'),
        backgroundColor: '#0a0a0a' # Matching our Neutral-950 design system
    });

    # In development, load from the local Next.js dev server
    # In production, load the exported HTML files
    const startUrl = process.env.NODE_ENV === 'development' 
        ? 'http://localhost:3000' 
        : `file://${path.join(__dirname, '../frontend/out/index.html')}`;

    win.loadURL(startUrl);

    # Open external links in the default browser
    win.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
