import React from 'react';
import { Card, Space, Button, Alert, Typography } from 'antd';
import { PlayCircle, UploadCloud, Terminal, CheckCircle2, FileText, AlertTriangle, RefreshCw } from 'lucide-react';

const { Title, Text, Paragraph } = Typography;

function ControlPanel({
  currentStep,
  loading,
  systemState,
  isDeployed,
  onStageInitial,
  onStageMergeDiff,
  onStageFinalAudit,
  onDeployToNetwork,
  onReset
}) {
  return (
    <div className="control-panel-cell">
      <Card title="🎮 核心操作主控台" className="card-common">

        {/* 步驟 0：環境初始化 */}
        {currentStep === 0 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert message="步驟一：環境初始化" description="系統將自動連線網碟，找出上週最新的目錄並建立今日新目錄、過濾並備份 GP 程式修改記錄 Excel，最後自動重寫本地 z_chk_all.sh 的覆核日期區間。" type="info" showIcon />
            <div className="action-center">
              <Button type="primary" size="large" icon={<PlayCircle size={18} />} loading={loading} onClick={onStageInitial} className="btn-primary-large">
                啟動第一階段環境初始化
              </Button>
            </div>
          </Space>
        )}

        {/* 步驟 1：處理附件二 */}
        {currentStep === 1 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="【手動操作檢查哨 1】請先執行以下操作再繼續："
              description={
                <Paragraph className="alert-paragraph-spacing">
                  1. 請將已自動更新日期的 <Text code>z_chk_all.sh</Text> 手動上傳至 Linux 遠端伺服器。<br />
                  2. 確保 Linux 端傳檔完畢後，點擊下方按鈕，系統將自動進行本地端 <Text bold>4gl_diff / 4fd_diff</Text> 的合併並寫入網碟附件二。
                </Paragraph>
              }
              type="warning"
              showIcon
              icon={<UploadCloud size={20} />}
            />
            <div className="action-center-orange">
              <Button type="primary" size="large" icon={<Terminal size={18} />} loading={loading} onClick={onStageMergeDiff} className="btn-orange-large">
                我已手動上傳 sh，執行 Diff 檔案自動合併
              </Button>
            </div>
          </Space>
        )}

        {/* 步驟 2：處理附件三 */}
        {currentStep === 2 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="【手動操作檢查哨 2】請透過遠端桌面 (RDP) 擷取資料："
              description={
                <Paragraph className="alert-paragraph-spacing">
                  1. 請登入遠端主機，執行已被重構的 <Text bold>rpt_diff.bat</Text> 與 <Text bold>xml_diff.bat</Text>。<br />
                  2. 將產生的 <Text type="danger" bold>4 個 CSV 檔案</Text> 下載並放回本機 <Text code>D:\...\aud</Text> 目錄下。<br />
                  3. 確保檔案皆已放入後，點擊下方按鈕啟動最終比對。
                </Paragraph>
              }
              type="warning"
              showIcon
              icon={<AlertTriangle size={20} />}
            />
            <div className="action-center-orange">
              <Button type="primary" size="large" icon={<CheckCircle2 size={18} />} loading={loading} onClick={onStageFinalAudit} className="btn-green-large">
                確認 4 個 CSV 已就位，啟動最終比對稽核
              </Button>
            </div>
          </Space>
        )}

        {/* 步驟 3：查核圓滿完成 (狀態 A & B) */}
        {currentStep === 3 && (
          <div className="success-result-area">
            {!isDeployed ? (
              <>
                <AlertTriangle size={56} className="icon-indicator-warning" />
                <Title level={4} className="audit-lock-title">🛑 人工核心稽核防線已鎖定</Title>
                <Paragraph className="desc-text mb-sm">
                  本機暫存區之覆核表 Docx 與附件二、三已建置完成。請先開啟並確認內容是否無誤：
                </Paragraph>
                <Paragraph className="desc-text">所有檔案皆已通過覆核，並已生成純文字比對報告：</Paragraph>
                <div className="report-code-box">
                  <Text code className="code-text-dark">
                    {systemState.reportPath || "D:\\1.Tony_Worklog\\0.TIPTOP_work\\topcust\\aud\\..._稽核比對結果報告.txt"}
                  </Text>
                </div>
                <div className="action-space-top">
                  <Space size="middle">
                    <Button onClick={onReset} type="text" danger>放棄並重置</Button>
                    <Button type="primary" size="large" icon={<UploadCloud size={18} />} loading={loading} onClick={onDeployToNetwork} className="btn-deploy">
                      確認檔案無誤，正式同步至網路磁碟 (第7階段)
                    </Button>
                  </Space>
                </div>
              </>
            ) : (
              <>
                <CheckCircle2 size={56} className="icon-indicator-success" />
                <Title level={4} className="success-result-title">🎉 本週定期稽核作業全數圓滿完成！</Title>
                <Paragraph className="desc-text">所有檔案皆已通過覆核，並全量成功發布至遠端會計師備查網碟目錄中。</Paragraph>
                <div className="report-code-box">
                  <Text code className="code-text-normal">
                    {systemState.folder || "已同步發布至遠端會計師備查網碟目錄中"}
                  </Text>
                </div>
                <div>
                  <Space size="middle">
                    <Button icon={<FileText size={16} />} type="primary" ghost>如何檢視報告</Button>
                    <Button icon={<RefreshCw size={16} />} type="dashed" onClick={onReset}>執行新一輪覆核</Button>
                  </Space>
                </div>
              </>
            )}
          </div>
        )}
      </Card>
    </div>
  );
}

export default ControlPanel;
