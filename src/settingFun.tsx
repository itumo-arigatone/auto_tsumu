import React from 'react';
import ReactDOM from 'react-dom';
import ChildProcess from 'child_process';
import CSS from 'csstype';

/**
 * setting fun position
 * @return {void}
 */
class SetFunPosition extends React.Component {
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
    return <div style={clickAreaStyle}>ファンの場所をクリックしてね。</div>;
  }
}

ReactDOM.render(<SetFunPosition />, document.getElementById('findArea'));
