import { Tag, Typography } from 'antd';
import { ShieldCheck } from 'lucide-react';

const { Title, Text } = Typography;

function HeaderSection({ backendConnected, runtimeInfo }) {
  return (
    <header className="app-header">
      <div className="brand-mark">
        <ShieldCheck size={28} />
      </div>
      <div className="header-copy">
        <Title level={2}>TIPTOP GP 程式覆核工具</Title>
        <Text type="secondary">每週程式修改覆核、附件整合與 DataCenter 同步</Text>
      </div>
      <div className="header-status">
        <Tag color={backendConnected ? 'success' : 'error'}>
          {backendConnected ? '後端已連線' : '後端未連線'}
        </Tag>
        <Tag color={runtimeInfo?.aud_exists ? 'processing' : 'warning'}>
          {runtimeInfo?.aud_exists ? 'aud 已就緒' : 'aud 待確認'}
        </Tag>
      </div>
    </header>
  );
}

export default HeaderSection;
