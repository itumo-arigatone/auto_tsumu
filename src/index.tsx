import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
import { ipcRenderer } from 'electron';
import CSS from 'csstype';
import { Scrollbar } from 'react-scrollbars-custom';
import Path from 'path';
import StartButtonImg from './style/images/start_button.png';
import backgroudImg from './style/images/wallpaper.png';
import WindowImg from './style/images/window.png';

const clearTextStyleconst: CSS.Properties = {
  textIndent: '100%',
  whiteSpace: 'nowrap',
  overflow: 'hidden',
};

/* eslint-disable no-invalid-this */
/**
 * スタートボタン情報クラス
 * @return {void}
 */
class StartButton extends React.Component<{ windowName: string }> {
  state = {
    style: {
      width: '100px',
      height: '60px',
      margin: '20px auto',
    },
    logging: '',
  };
  leave = () => {
    this.setState({
      style: {
        width: 100,
        height: 60,
        margin: '20px auto',
      },
    });
  };
  enter = () => {
    this.setState({
      style: {
        width: 115,
        height: 69,
        margin: 'auto',
        marginTop: 15,
      },
    });
  };

  onClickEvent = () => {
    const data = ipcRenderer.invoke('push-start', 'data');
    if (data == null) {
      console.log('error');
    }
    // SetWindowNameBoxから値を取得する
    const windowName = this.props.windowName;

    // python を呼び出す
    console.log(process.env.NODE_ENV);
    const isDevelopment = process.env.NODE_ENV === 'development';
    // pyファイルのパスを取得
    const pythonPath = isDevelopment
      ? './src/python/tsumu.py'
      : Path.join(__dirname, '../../src/python/tsumu.py');
    // 画像格納先パスを取得
    const imagePath = isDevelopment
      ? './img/window.png'
      : Path.join(__dirname, '../../img/window.png');
    // ログファイル格納先パスを取得
    const logPath = isDevelopment
      ? './dist/logger.log'
      : Path.join(__dirname, '../../log/logger.log');
    // python処理実行 python {パス} {Vysorウィンドウ名} {画像格納先パス} {logファイルの格納先パス}
    const command = `python ${pythonPath} ${windowName} ${imagePath} ${logPath}`;
    ChildProcess.exec(
      command,
      { maxBuffer: 1024 * 500 },
      (error, stdout, stderr) => {
        if (error != null) {
          ipcRenderer.invoke('pyEnd', error + '');
          this.setState({
            logging: 'error:' + error,
          });
        } else {
          ipcRenderer.invoke('pyEnd', 'data');
          this.setState({
            logging: 'info:' + stdout,
          });
        }
      },
    );
  };

  /**
   * レンダー
   * @return {any} button tag
   */
  render() {
    const buttonOutStyle: CSS.Properties = {
      width: '340px',
      height: '100px',
      top: '50px',
      margin: 'auto',
      position: 'absolute',
    };
    const buttonStyle: CSS.Properties = {
      backgroundImage: `url(${StartButtonImg})`,
      backgroundSize: 'contain',
      right: '0',
      left: '0',
      position: 'absolute',
    };
    return (
      <>
        <div id="button_out" style={buttonOutStyle}>
          <span
            className="button clearText"
            onMouseEnter={this.enter}
            onMouseLeave={this.leave}
            onClick={this.onClickEvent}
            style={Object.assign(
              {},
              clearTextStyleconst,
              buttonStyle,
              this.state.style,
            )}>
            start
          </span>
        </div>
        <Logging msg={this.state.logging} />
      </>
    );
  }
}

/**
 * log情報クラス
 * @return {void}
 */
class Logging extends React.Component<{ msg: string }> {
  /**
   * レンダー
   * @return {any} button tag
   */
  render() {
    const messageAreaStyle: CSS.Properties = {
      backgroundColor: '#00000000',
      width: '320px',
      height: '145px',
      position: 'absolute',
      top: '140px',
      right: '0',
      left: '0',
      margin: 'auto',
    };
    const messageStyle: CSS.Properties = {
      color: '#ff0000',
    };
    return (
      <Scrollbar style={messageAreaStyle}>
        <div className="message" style={messageStyle}>
          {this.props.msg}
        </div>
      </Scrollbar>
    );
  }
}

/**
 * input window name
 * @param {string} e inputed message
 * @return {void}
 */
class SetWindowNameBox extends React.Component {
  state = {
    inputValue: '',
    placeholder: 'input window name',
  };
  handleOnChange = (e: any) => {
    this.setState({ inputValue: e.target.value });
    ipcRenderer.invoke('set-name', e.target.value);
  };
  /**
   * レンダー
   * @return {any} input tag
   */
  render() {
    document.body.style.backgroundImage = `url(${backgroudImg})`;
    document.body.style.backgroundSize = 'cover';
    const outWindowStyle: CSS.Properties = {
      backgroundImage: `url(${WindowImg})`,
      width: '340px',
      height: '290px',
      margin: 'auto',
    };
    const setWindowNameStyle: CSS.Properties = {
      textAlign: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0)',
      color: '#ffffff',
      borderWidth: '0px',
      outline: 'none',
      right: 0,
      left: 0,
      margin: '20px auto',
      position: 'absolute',
    };
    const boxOutStyle: CSS.Properties = {
      width: '340px',
      height: '20px',
      margin: 'auto',
      position: 'absolute',
    };
    return (
      <div id="out_window" style={outWindowStyle}>
        <div id="box_out" style={boxOutStyle}>
          <input
            type="text"
            value={this.state.inputValue}
            placeholder={this.state.placeholder}
            onChange={e => this.handleOnChange(e)}
            className="set_window_name"
            style={setWindowNameStyle}
          />
        </div>
        <StartButton windowName={this.state.inputValue} />
      </div>
    );
  }
}

ReactDOM.render(<SetWindowNameBox />, document.getElementById('findWindow'));
