import { Alert, Button, Card, Descriptions, Space, Typography } from 'antd';
import {
  CheckCircle2,
  ClipboardCheck,
  FileText,
  FolderCheck,
  Network,
  RefreshCw,
  Server,
  UploadCloud,
} from 'lucide-react';

const { Text, Title, Paragraph } = Typography;

const stepCards = [
  {
    title: '環境初始化',
    type: 'info',
    description: '建立本週覆核資料夾、複製 GP 程式修改記錄 Excel，並更新 aud 內的 z_chk_all.sh 日期區間。',
    actionLabel: '執行環境初始化',
    actionKey: 'initialize',
    icon: FolderCheck,
  },
  {
    title: 'TipTop 主機作業',
    type: 'warning',
    description: '將 aud\\z_chk_all.sh 上傳到 TipTop 主機執行，再把 4fd_diff.txt 與 4gl_diff.txt 放回本機 aud。',
    actionLabel: '已完成 TipTop 作業',
    actionKey: 'confirmTipTop',
    icon: Server,
  },
  {
    title: '合併附件二',
    type: 'info',
    description: '讀取 aud 內的 4fd_diff.txt 與 4gl_diff.txt，合併到本週覆核資料夾的附件二。',
    actionLabel: '合併附件二',
    actionKey: 'mergeDiff',
    icon: ClipboardCheck,
  },
  {
    title: 'CR 主機作業',
    type: 'warning',
    description: '將 aud\\rpt_diff.bat 與 aud\\xml_diff.bat 上傳到 CR 主機執行，再把 4 個 CSV 放回本機 aud。',
    actionLabel: '已完成 CR 作業',
    actionKey: 'confirmCr',
    icon: Server,
  },
  {
    title: '合併附件三',
    type: 'info',
    description: '讀取 aud 內的 CSV 檔案，合併到本週覆核資料夾的附件三。',
    actionLabel: '合併附件三',
    actionKey: 'mergeCsv',
    icon: FileText,
  },
  {
    title: '稽核交叉比對',
    type: 'info',
    description: '比對 Excel、附件二與附件三，產出本週稽核比對結果報告。',
    actionLabel: '執行稽核比對',
    actionKey: 'finalAudit',
    icon: ClipboardCheck,
  },
  {
    title: '人工確認',
    type: 'success',
    description: '請開啟下方報告路徑確認內容，確認無誤後再進入上傳步驟。',
    actionLabel: '報告已確認',
    actionKey: 'confirmReport',
    icon: CheckCircle2,
  },
  {
    title: '同步 DataCenter',
    type: 'info',
    description: '將本週覆核資料夾同步到 DataCenter 會計師備查指定位置。',
    actionLabel: '同步至 DataCenter',
    actionKey: 'deploy',
    icon: UploadCloud,
  },
];

function PathLine({ label, value }) {
  return (
    <div className="path-line">
      <span>{label}</span>
      <Text code title={value || ''}>{value || '尚未產生'}</Text>
    </div>
  );
}

function ControlPanel({ currentStep, loading, runtimeInfo, systemState, isDeployed, actions }) {
  const step = stepCards[currentStep] || stepCards[0];
  const Icon = step.icon;
  const action = actions[step.actionKey];
  const audReady = Boolean(runtimeInfo?.aud_exists);
  const disableAction = currentStep === 0 ? !audReady && runtimeInfo !== null : false;

  return (
    <main className="workspace-grid">
      <section className="primary-panel">
        <Card className="panel-card" styles={{ body: { padding: 0 } }}>
          <div className="panel-header">
            <div className="panel-icon">
              <Icon size={26} />
            </div>
            <div>
              <Text type="secondary">目前步驟 {currentStep + 1} / {stepCards.length}</Text>
              <Title level={3}>{step.title}</Title>
            </div>
          </div>

          <Alert
            className="step-alert"
            message={step.title}
            description={step.description}
            type={step.type}
            showIcon
          />

          {currentStep === 0 && !audReady && (
            <Alert
              className="step-alert"
              message="找不到 aud 資料夾"
              description={`請確認 aud 是否存在於專案根目錄。預期路徑：${runtimeInfo?.aud_path || '讀取中'}`}
              type="error"
              showIcon
            />
          )}

          {currentStep === 6 && (
            <PathLine label="稽核報告" value={systemState.reportPath} />
          )}

          {currentStep === 7 && isDeployed ? (
            <div className="done-box">
              <CheckCircle2 size={44} />
              <Title level={4}>本週查核作業已完成</Title>
              <Paragraph>檔案已同步至 DataCenter，可開始下一輪覆核或關閉程式。</Paragraph>
            </div>
          ) : (
            <div className="action-bar">
              <Button
                type="primary"
                size="large"
                icon={<Icon size={18} />}
                loading={loading}
                disabled={disableAction}
                onClick={action}
              >
                {step.actionLabel}
              </Button>
              <Button size="large" icon={<RefreshCw size={18} />} onClick={actions.reset}>
                重置流程
              </Button>
            </div>
          )}
        </Card>
        <Card title="交付提示" className="side-card compact-card delivery-card">
          <Network size={20} />
          <Paragraph>
            ??exe ?曉 dist ?批銵?蝔??蝙?其?銝撅文?獢?桅???aud ?摮??冗嚗?? dist ?批憭遣蝡?
          </Paragraph>
        </Card>
      </section>

      <aside className="side-panel">
        <Card title="執行環境" className="side-card">
          <Descriptions column={1} size="small" bordered>
            <Descriptions.Item label="後端狀態">
              {runtimeInfo ? '已連線' : '讀取中'}
            </Descriptions.Item>
            <Descriptions.Item label="aud">
              {audReady ? '存在' : '未偵測'}
            </Descriptions.Item>
            <Descriptions.Item label="暫存資料夾">
              {runtimeInfo?.review_exists ? '存在' : '未偵測'}
            </Descriptions.Item>
          </Descriptions>

          <Space direction="vertical" className="path-stack">
            <PathLine label="執行根目錄" value={runtimeInfo?.project_root} />
            <PathLine label="aud 路徑" value={runtimeInfo?.aud_path} />
            <PathLine label="暫存路徑" value={runtimeInfo?.review_path} />
            <PathLine label="本週資料夾" value={systemState.folder} />
          </Space>
        </Card>

        <Card title="交付提示" className="side-card compact-card">
          <Network size={20} />
          <Paragraph>
            若 exe 放在 dist 內執行，程式會使用上一層專案根目錄的 aud 與暫存資料夾，不會在 dist 內另外建立。
          </Paragraph>
        </Card>
      </aside>
    </main>
  );
}

export default ControlPanel;
