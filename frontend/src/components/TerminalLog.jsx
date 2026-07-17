import { Card } from 'antd';

function TerminalLog({ logMessages, logEndRef }) {
  return (
    <div className="log-panel-cell">
      <Card title="系統執行即時日誌" className="card-common" styles={{ body: { padding: '12px' } }}   ㄦ>
        <div className="terminal-box">
          {logMessages.length === 0 ? (
            <span className="terminal-empty">＞ 等待控制台發送指令觸發...</span>
          ) : (
            logMessages.map((log, idx) => {
              let logClass = 'log-line-default';
              if (log.includes('失敗') || log.includes('異常') || log.includes('錯誤') || log.includes('未偵測')) {
                logClass = 'log-line-error';
              } else if (log.includes('成功') || log.includes('正常') || log.includes('通過') || log.includes('已成功')) {
                logClass = 'log-line-success';
              } else if (log.includes('提醒') || log.includes('警告')) {
                logClass = 'log-line-info';
              }

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
