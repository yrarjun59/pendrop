const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;

function startBackend() {
    const isWin = process.platform === 'win32';
    const pythonCmd = isWin ? 'python' : 'python3';
    
    backendProcess = spawn(pythonCmd, ['backend/main.py'], {
        cwd: app.getAppPath(),
        shell: true,
        detached: true,
        stdio: 'ignore'
    });
    
    backendProcess.unref();
    
    backendProcess.on('error', (err) => {
        console.error('Backend failed to start:', err);
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        },
        show: false
    });

    mainWindow.loadFile(path.join(__dirname, 'index.html'));

    // Open DevTools for debugging
    mainWindow.webContents.openDevTools();

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(() => {
    startBackend();
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