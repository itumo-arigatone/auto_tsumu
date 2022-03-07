import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
import { ipcRenderer } from 'electron';
import Path from 'path';
import CSS from 'csstype';

/**
 * setting fun position
 * @return {void}
 */
class SetFunPosition extends React.Component {
  /**
   * レンダー
   * @param {any} event
   * @return {void}
   */
  onClickEvent = async (event: any) => {
    let windowName = '';
    windowName = await ipcRenderer.invoke('get-fun', '');
    console.log(windowName);
    const isDevelopment = process.env.NODE_ENV === 'development';
    const pythonPath = isDevelopment
      ? './src/python/getWindow.py'
      : Path.join(__dirname, '../../src/python/getWindow.py');
    const command = `python ${pythonPath} ${windowName}`;
    let positionArray: Array<String> = [];
    await ChildProcess.exec(
      command,
      { maxBuffer: 1024 * 500 },
      (error, stdout, stderr) => {
        if (error != null) {
          console.log(error);
        } else {
          console.log(stdout);
          positionArray = stdout.split(" ");
        }
      },
    );
    const positionX = event.clientX;
    const positionY = event.clientY;
    // ファンの位置を設定したらウィンドウを閉じる
    window.close();
  };
  /**
   * レンダー
   * @return {any} input tag
   */
  render() {
    document.body.style.background = 'rgba(0, 0, 0, 0.4)';
    document.body.style.margin = '0';
    document.body.style.height = '100%';
    document.body.style.width = '100%';
    const clickAreaStyle: CSS.Properties = {
      width: '100%',
      height: '100%',
      color: '#ffffff',
    };
    return (
      <div style={clickAreaStyle} onClick={this.onClickEvent}>
        ファンの場所をクリックしてね。
      </div>
    );
  }
}

ReactDOM.render(<SetFunPosition />, document.getElementById('findArea'));
