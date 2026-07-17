import { Typography, Tag } from 'antd';

const { Title, Text } = Typography;

function HeaderSection({ backendConnected }) {
  return (
    <div className="header-section">
      <div className="header-title-area">
        <Title level={3}>TIPTOP GP 程式覆核自動化系統</Title>
        <Text type="secondary">MIS 每週定期程序修改查核工具 — 生產正式版</Text>
      </div>
      <div>
        {backendConnected ? (
          <Tag color="success" className="tag-status">● 後端連線正常</Tag>
        ) : (
          <Tag color="error" className="tag-status">● 後端尚未連線</Tag>
        )}
      </div>
    </div>
  );
}

export default HeaderSection;
