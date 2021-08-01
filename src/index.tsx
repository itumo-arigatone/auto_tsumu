import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
import { ipcRenderer } from 'electron';

/* eslint-disable no-invalid-this */
/**
 * スタートボタン情報クラス
 * @return {void}
 */
class StartButton extends React.Component<{ windowName: string }> {
  state = {
    style: {
      background: '',
    },
    logging: '',
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
    const data = ipcRenderer.invoke('push-start', 'data');
    if (data == null) {
      console.log('error');
    }
    // SetWindowNameBoxから値を取得する
    console.log(this.props.windowName);
    const windowName = this.props.windowName;

    // python を呼び出す
    const command = 'python ./src/python/tsumu.py ' + windowName;
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
    return (
      <>
        <span
          className="button clearText"
          onMouseEnter={this.enter}
          onMouseLeave={this.leave}
          onClick={this.onClickEvent}
          style={this.state.style}>
          start
        </span>
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
    return (
      <div id="messageArea">
        <div className="message">{this.props.msg}</div>
      </div>
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
  };
  /**
   * レンダー
   * @return {any} input tag
   */
  render() {
    return (
      <div>
        <input
          type="text"
          value={this.state.inputValue}
          placeholder={this.state.placeholder}
          onChange={e => this.handleOnChange(e)}
          className="set_window_name"
        />
        <StartButton windowName={this.state.inputValue} />
      </div>
    );
  }
}

ReactDOM.render(<SetWindowNameBox />, document.getElementById('findWindow'));
