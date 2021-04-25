import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
import fs from 'fs';
import { ipcRenderer } from 'electron';

/* eslint-disable no-invalid-this */
/**
 * スタートボタン情報クラス
 * @return {void}
 */
class StartButton extends React.Component {
  state = {
    background: '',
  };
  leave = () => {
    this.setState({
      background: '#00ff00',
    });
  };
  enter = () => {
    this.setState({
      background: '#00ffff',
    });
  };

  getWindowPosition = () => {
    try {
      const position = JSON.parse(
        fs.readFileSync('./dist/bounds.json', 'utf8'),
      );
      return position;
    } catch (e) {
      console.log(e);
      return null;
    }
  };

  // 透明部分の左角の座標取得
  getCorner = () => {
    const coordinates = document
      .getElementById('corner')!
      .getBoundingClientRect();
    return {
      x: coordinates.x,
      y: coordinates.y + 10,
    };
  };

  onClickEvent = () => {
    const position = this.getCorner();
    const screen = this.getWindowPosition();
    const window = {
      x: position.x + screen[0],
      y: position.y + screen[1],
    };
    // ウィンドウ操作
    const data = ipcRenderer.invoke('push-start', 'data');
    if (data == null) {
      console.log('error');
    }
    // python を呼び出す
    const command =
      'python ./src/python/tsumu.py SCV42 ' + window.x * 2 + ' ' + window.y * 2;
    ChildProcess.exec(command, { maxBuffer: 1024 * 500 }, (error, stdout, stderr) => {
      if (error != null) {
        ipcRenderer.invoke('pyEnd', error + '');
        // TODO 画面に書き込む処理
        <Logging msg={error + ''} />;
        console.log(error);
        console.log('error');
      } else {
        ipcRenderer.invoke('pyEnd', 'data');
        <Logging msg={stdout + ''} />;
        console.log(stdout);
        console.log('stdout');
      }
    });
  };

  /**
   * レンダー
   * @return {any} button tag
   */
  render() {
    return (
      <span
        className="button"
        onMouseEnter={this.enter}
        onMouseLeave={this.leave}
        onClick={this.onClickEvent}
        style={this.state}>
        start
      </span>
    );
  }
}

/**
 * スタートボタン情報クラス
 * @return {void}
 */
class Logging extends React.Component<{ msg: string }> {
  /**
   * レンダー
   * @return {any} button tag
   */
  render() {
    return this.props.msg;
  }
}

ReactDOM.render(<StartButton />, document.getElementById('startButton'));
ReactDOM.render(<Logging msg={'aa'} />, document.getElementById('messageArea'));
