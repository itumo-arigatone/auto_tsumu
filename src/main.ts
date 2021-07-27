import {app, BrowserWindow, ipcMain} from 'electron';
import fs from 'fs';

// セキュアな Electron の構成
// 参考: https://qiita.com/pochman/items/64b34e9827866664d436
let win:any
const createWindow = (): void => {
  // レンダープロセスとなる、ウィンドウオブジェクトを作成する。
  win = new BrowserWindow({
    width: 900,
    height: 500,
    frame: true,
    resizable: true,
    webPreferences: {
      // ローカルで完結するためtrueにする
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  // 読み込む index.html。
  // tsc でコンパイルするので、出力先の dist の相対パスで指定する。
  win.loadFile('./index.html');

  // 開発者ツールを起動する
  win.webContents.openDevTools();
  win.setPosition(10, 0);
};

// Electronの起動準備が終わったら、ウィンドウを作成する。
app.whenReady().then(createWindow);

// すべての ウィンドウ が閉じたときの処理
app.on('window-all-closed', () => {
  // macOS 以外では、メインプロセスを停止する
  // macOS では、ウインドウが閉じてもメインプロセスは停止せず
  // ドックから再度ウインドウが表示されるようにする。
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // macOS では、ウインドウが閉じてもメインプロセスは停止せず
  // ドックから再度ウインドウが表示されるようにする。
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.handle('push-start', (event, message) => {
  win.setIgnoreMouseEvents(true);
  return 'ok';
})

ipcMain.handle('pyEnd', (event, error) => {
  console.log(error);
  win.setIgnoreMouseEvents(false);
  return;
})

ipcMain.handle('logger', (event, str) => {
  console.log(str);
  return;
})
