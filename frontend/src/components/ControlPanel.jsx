import React from 'react';
import { Card, Space, Button, Alert, Typography } from 'antd';
import { PlayCircle, UploadCloud, CheckCircle2, FileText, RefreshCw, Terminal } from 'lucide-react';

const { Title, Text, Paragraph } = Typography;

function ControlPanel({
  currentStep,
  loading,
  systemState,
  isDeployed,
  audWarning,
  onRecheckAud,
  onStageInitial,
  onShellExecutedNext,
  onStageMergeDiff,
  onBatExecutedNext,
  onStageProcessAttachmentThree,
  onStageFinalAudit,
  onFinalConfirmNext,
  onDeployToNetwork,
  onReset
}) {
  return (
    <div className="control-panel-cell">
      <Card title="🎮 核心操作主控台" className="card-common">

        {/* ================= 1. 環境初始化 (Index 0) ================= */}
        {currentStep === 0 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 1：環境初始化"
              description="系統將自動找出上週最新的目錄並建立今日新目錄、過頻並備份 GP 程式修改記錄 Excel，最後自動重寫本地 z_chk_all.sh 的覆核日期區間。"
              type="info"
              showIcon
            />

            {audWarning && (
              <Alert
                message="【環境檢查異常】系統查詢不到 aud 資料夾"
                description={
                  <div>
                    <p>請手動在專案根目錄下建立 <Text code>aud</Text> 資料夾。</p>
                    <p style={{ fontWeight: 'bold', color: '#ff4d4f' }}>⚠️ 流程已在步驟 1 實施強制留置。您必須點擊下方按鈕重新檢測，通過後才能前往步驟 2。</p>
                  </div>
                }
                type="error"
                showIcon
              />
            )}

            <div className="action-center" style={{ width: '100%', textAlign: 'center' }}>
              {audWarning ? (
                <Button
                  type="primary"
                  danger
                  size="large"
                  icon={<RefreshCw size={18} />}
                  loading={loading}
                  onClick={() => { if (onRecheckAud) onRecheckAud(); }}
                  style={{ width: '100%', backgroundColor: '#ff4d4f', borderColor: '#ff4d4f', height: '48px', fontSize: '16px' }}
                >
                  點此【重新檢查環境路徑並解鎖】
                </Button>
              ) : (
                <Button
                  type="primary"
                  size="large"
                  icon={<PlayCircle size={18} />}
                  loading={loading}
                  onClick={onStageInitial}
                  className="btn-primary-large"
                  style={{ width: '100%' }}
                >
                  啟動第一階段環境初始化
                </Button>
              )}
            </div>
          </Space>
        )}

        {/* ================= 2. TipTop主機 shell 檔案 (Index 1) ================= */}
        {currentStep === 1 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 2：TipTop 主機上傳並執行 shell 檔案"
              description={
                <div>
                  <p>請開啟 SSH，將 <Text code>...aud/z_chk_all.sh</Text> 上傳至 TipTop 主機 aud 資料夾底下。</p>
                  <p>請開啟本地終端機使用 topgp 帳號，切換至 aud 路徑底下執行 <Text code>z_chk_all.sh</Text> 檔案。</p>
                  <p>執行成功後，TipTop 會自動產出最新的異動檔，請確保將結果傳回至本地專案的 <Text code>aud</Text> 資料夾內。</p>
                </div>
              }
              type="warning"
              showIcon
            />
            <div className="action-center">
              <Button
                type="primary"
                size="large"
                icon={<CheckCircle2 size={18} />}
                onClick={onShellExecutedNext}
                className="btn-primary-large btn-orange-glow"
                style={{ width: '100%' }}
                disabled={audWarning}
              >
                {audWarning ? "❌ 步驟 1 環境異常未解除，按鈕鎖定" : "我已確認 TipTop 主機 shell 執行完畢，前往下一步"}
              </Button>
            </div>
          </Space>
        )}

        {/* ================= 3. 處理附件二 (Index 2) ================= */}
        {currentStep === 2 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 3：處理附件二"
              description="系統將自動讀取本地 aud 目錄下的 4fd_diff.txt 與 4gl_diff.txt 檔案，並自動合併至今日覆核區的附件二檔案中。"
              type="info"
              showIcon
            />
            <div className="action-center">
              <Button
                type="primary"
                size="large"
                icon={<Terminal size={18} />}
                loading={loading}
                onClick={onStageMergeDiff}
                className="btn-primary-large"
                style={{ width: '100%' }}
                disabled={audWarning}
              >
                {audWarning ? "❌ 步驟 1 環境異常未解除，按鈕鎖定" : "執行附件二：合併本地 Diff 差異檔"}
              </Button>
            </div>
          </Space>
        )}

        {/* ================= 4. CR主機批次檔 (Index 3) ================= */}
        {currentStep === 3 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 4：CR 主機上傳並執行 bat 檔案"
              description={
                <div>
                  <p>系統已於本地更新 <Text code>rpt_diff.bat</Text> 與 <Text code>xml_diff.bat</Text>。</p>
                  <p>請手動將這兩個檔案上傳至您的 CR 報表主機執行。執行完畢後，會生成對應的 4 個 CSV 稽核記錄，請手動將產出的 CSV 下載放回到本地專案的 <Text code>aud</Text> 資料夾中。</p>
                </div>
              }
              type="warning"
              showIcon
            />
            <div className="action-center">
              <Button
                type="primary"
                size="large"
                icon={<CheckCircle2 size={18} />}
                onClick={onBatExecutedNext}
                className="btn-primary-large btn-orange-glow"
                style={{ width: '100%' }}
                disabled={audWarning}
              >
                {audWarning ? "❌ 步驟 1 環境異常未解除，按鈕鎖定" : "我已確認 CR 主機批次檔執行完畢並放回 CSV，前往下一步"}
              </Button>
            </div>
          </Space>
        )}

        {/* ================= 5. 處理附件三 (Index 4) ================= */}
        {currentStep === 4 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 5：處理附件三"
              description="準備進入附件三 CSV 整合階段。系統將讀取您放回的 CSV 異動摘要，並將資料合併至今日覆核區的附件三檔案中。"
              type="info"
              showIcon
            />
            <div className="action-center">
              <Button
                type="primary"
                size="large"
                icon={<PlayCircle size={18} />}
                loading={loading}
                onClick={onStageProcessAttachmentThree}
                className="btn-primary-large"
                style={{ width: '100%' }}
                disabled={audWarning}
              >
                {audWarning ? "❌ 步驟 1 環境異常未解除，按鈕鎖定" : "準備就緒，前往附件三彙整與大比對"}
              </Button>
            </div>
          </Space>
        )}

        {/* ================= 6. 交叉大比對 (Index 5) ================= */}
        {currentStep === 5 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 6：比對附件二、三與程式修改紀錄"
              description="比對本週程式修改紀錄 Excel、附件二及附件三。進行交叉比對，並產出稽核覆核結果文字檔。"
              type="info"
              showIcon
            />
            <div className="action-center">
              <Button
                type="primary"
                size="large"
                icon={<Terminal size={18} />}
                loading={loading}
                onClick={onStageFinalAudit}
                className="btn-primary-large"
                style={{ width: '100%' }}
                disabled={audWarning}
              >
                {audWarning ? "❌ 步驟 1 環境異常未解除，按鈕鎖定" : "啟動稽核交叉比對"}
              </Button>
            </div>
          </Space>
        )}

        {/* ================= 7. 人工查核確認 (Index 6) ================= */}
        {currentStep === 6 && (
          <Space direction="vertical" size="large" className="full-width-space">
            <Alert
              message="步驟 7：上傳前最後確認 (人工核對審查)"
              type="success"
              showIcon
              description="比對已完成！系統已產出實體比對結果。請依下方路徑，手動開啟報告確認是否有無錯誤。"
            />
            <div className="report-code-box">
              <Text code className="code-text-normal">
                {systemState.reportPath || "找不到報告路徑，請檢查後端日誌。"}
              </Text>
            </div>
            <div className="action-center">
              <Button
                type="primary"
                size="large"
                icon={<CheckCircle2 size={18} />}
                onClick={onFinalConfirmNext}
                className="btn-primary-large btn-success-glow"
                style={{ width: '100%' }}
                disabled={audWarning}
              >
                {audWarning ? "❌ 步驟 1 環境異常未解除，按鈕鎖定" : "人工查核完成"}
              </Button>
            </div>
          </Space>
        )}

        {/* ================= 8. 同步網碟完成 (Index 7) ================= */}
        {currentStep === 7 && (
          <div className="full-width-space">
            {!isDeployed ? (
              <>
                <Alert
                  message="步驟 8：查核作業最終回傳至 DataCenter"
                  description="確認上傳！點擊下方按鈕，系統將把今日建立之本機本週的程式修改週覆核記錄資料夾，複製至 DataCenter 中會計師備查專用路徑下。"
                  type="info"
                  showIcon
                />
                <div className="report-code-box" style={{ marginTop: '16px' }}>
                  <Text code className="code-text-normal">
                    本機來源：{systemState.folder || "未定義獨立目錄"}
                  </Text>
                </div>
                <div className="action-space-top" style={{ marginTop: '24px', textAlign: 'center' }}>
                  <Space size="middle">
                    <Button onClick={onReset} type="text" danger>放棄並重置</Button>
                    <Button
                      type="primary"
                      size="large"
                      icon={<UploadCloud size={18} />}
                      loading={loading}
                      onClick={onDeployToNetwork}
                      className="btn-deploy"
                      disabled={audWarning}
                    >
                      確認檔案無誤，正式同步至網路磁碟
                    </Button>
                  </Space>
                </div>
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: '16px 0' }}>
                <CheckCircle2 size={56} style={{ color: '#52c41a', marginBottom: '16px' }} />
                <Title level={4}>🎉 本週定期稽核作業全數圓滿完成！</Title>
                <Paragraph>所有檔案皆已通過覆核，並成功複製至 DataCenter 會計師備查指定目錄下。</Paragraph>
                <div className="report-code-box" style={{ marginBottom: '24px' }}>
                  <Text code className="code-text-normal">
                    本週目標：{systemState.folder ? `程式修改週覆核記錄(暫存)/${systemState.folder.split(/[\\/]/).pop()}` : "已發布至指定備查目錄"}
                  </Text>
                </div>
                <div>
                  <Space size="middle">
                    <Button icon={<FileText size={16} />} type="primary" ghost>如何檢視報告</Button>
                    <Button icon={<RefreshCw size={16} />} type="dashed" onClick={onReset}>執行新一輪覆核</Button>
                  </Space>
                </div>
              </div>
            )}
          </div>
        )}

      </Card>
    </div>
  );
}

export default ControlPanel;
