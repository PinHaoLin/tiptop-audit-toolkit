import { Card, Empty } from 'antd';

function TerminalLog({ logMessages = [], logEndRef }) {
  return (
    <Card title="執行紀錄" className="side-card">
      <div className="terminal-box">
        {logMessages.length === 0 ? (
          <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="尚無紀錄" />
        ) : (
          logMessages.map((log, idx) => (
            <div key={`${idx}-${log}`} className="log-line">
              {log}
            </div>
          ))
        )}
        <div ref={logEndRef} />
      </div>
    </Card>
  );
}

export default TerminalLog;
