import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
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

  onClickEvent = () => {
    // ウィンドウ操作
    const data = ipcRenderer.invoke('push-start', 'data');
    if (data == null) {
      console.log('error');
    }
    // python を呼び出す
    const command = 'python ./src/python/tsumu.py SCV42';
    ChildProcess.exec(
      command,
      { maxBuffer: 1024 * 500 },
      (error, stdout, stderr) => {
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
      },
    );
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
 * log情報クラス
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

/**
 * input window name
 * @param {string} e inputed message
 * @return {void}
 */
class SetWindowNameBox extends React.Component {
  state = {
    inputValue: '',
    placeholder: 'input window name',
    styles: {
      left: '20px',
    },
  };
  handleOnChange = (e: any) => {
    this.setState({ inputValue: e.target.value });
  };
  /**
   * レンダー
   * @return {any} input tag
   */
  render() {
    return (
      <input
        type="text"
        value={this.state.inputValue}
        placeholder={this.state.placeholder}
        onChange={e => this.handleOnChange(e)}
        style={this.state.styles}
      />
    );
  }
}

ReactDOM.render(<StartButton />, document.getElementById('startButton'));
ReactDOM.render(<Logging msg={'aa'} />, document.getElementById('messageArea'));
ReactDOM.render(<SetWindowNameBox />, document.getElementById('findWindow'));
