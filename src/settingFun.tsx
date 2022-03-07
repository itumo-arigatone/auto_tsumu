import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
import { ipcRenderer } from 'electron';
import Path from 'path';
import CSS from 'csstype';
import Fs from 'fs';
import Util from 'util';
const exec = Util.promisify(ChildProcess.exec);
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
    const isDevelopment = process.env.NODE_ENV === 'development';
    const pythonPath = isDevelopment
      ? './src/python/getWindow.py'
      : Path.join(__dirname, '../../src/python/getWindow.py');
    const command = `python ${pythonPath} ${windowName}`;
    let positionArray: Array<string> = [];
    const res = await exec(command, { maxBuffer: 1024 * 500 });
    console.log(res.stdout);
    positionArray = res.stdout.split(' ');
    const settingPath = Path.join(__dirname, './setting.json');
    console.log(positionArray);
    const funPosition = {
      funX: event.clientX - parseInt(positionArray[0], 10),
      funY: event.clientY - parseInt(positionArray[1], 10),
    };
    Fs.writeFile(settingPath, JSON.stringify(funPosition), function (err) {
      if (err) {
        throw err;
      }
    });
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
