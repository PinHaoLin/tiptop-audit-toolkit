import React from 'react';
import { Card } from 'antd';

function TerminalLog({ logMessages, logEndRef }) {
  return (
    <div className="log-panel-cell">
      <Card title="📄 系統執行即時日誌" className="card-common" styles={{ body: { padding: '12px' } }}>
        <div className="terminal-box">
          {logMessages.length === 0 ? (
            <span className="terminal-empty">＞ 等待控制台發送指令觸發...</span>
          ) : (
            logMessages.map((log, idx) => {
              let logClass = 'log-line-default';
              if (log.includes('❌')) logClass = 'log-line-error';
              else if (log.includes('🟢')) logClass = 'log-line-info';
              else if (log.includes('🎉')) logClass = 'log-line-success';

              return (
                <div key={idx} className={`log-line ${logClass}`}>
                  {log}
                </div>
              );
            })
          )}
          <div ref={logEndRef} />
        </div>
      </Card>
    </div>
  );
}

export default TerminalLog;
