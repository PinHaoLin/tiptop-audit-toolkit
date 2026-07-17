import { useEffect, useRef, useState } from 'react';
import { message, Alert } from 'antd';
import HeaderSection from './components/HeaderSection';
import StepProgress from './components/StepProgress';
import ControlPanel from './components/ControlPanel';
import TerminalLog from './components/TerminalLog';
import './App.css';

const initialSystemState = { todayStr: '', folder: '', reportPath: '' };

function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [logMessages, setLogMessages] = useState(() => [
    window.eel
      ? `[${new Date().toLocaleTimeString()}] 系統提示：成功與 Python Eel 後端建立連線通道！`
      : `[${new Date().toLocaleTimeString()}] 系統提示：未偵測到 Eel 核心，請確保使用 python app.py 啟動。`,
  ]);
  const [backendConnected] = useState(() => Boolean(window.eel));
  const [systemState, setSystemState] = useState(initialSystemState);
  const [isDeployed, setIsDeployed] = useState(false);

  // 本地 aud 資料夾缺失的卡關狀態
  const [audWarning, setAudWarning] = useState(false);

  const logEndRef = useRef(null);

  const addLog = (msg) => {
    setLogMessages((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const runBackendStage = async (stageName, eelMethodName, onSuccess, fallbackErrorMessage) => {
    setLoading(true);
    try {
      const res = await window.eel[eelMethodName]()();
      if (res && res.status === "success") {
        onSuccess(res);
        return;
      }

      message.error(res?.message || fallbackErrorMessage);
    } catch (err) {
      message.error("後端通訊異常");
      addLog(`${stageName} 發生後端通訊異常：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (window.eel) {
      window.eel.add_log_from_backend = (msg) => addLog(msg);
    }
  }, []);

  // 1. 啟動環境初始化 (步驟 1 鋼鐵防線)
  const handleStageInitial = async () => {
    setLoading(true);
    try {
      const res = await window.eel.run_stage_initial()();
      if (res && res.status === "success") {
        setAudWarning(false);
        setCurrentStep(1); // 成功才前往步驟 2（TipTop Shell 中斷點）
        message.success("步驟 1 環境初始化與 Excel 備份成功！已進入步驟 2。");
      } else {
        setAudWarning(true);
        setCurrentStep(0); // 失敗強制留在步驟 1
        message.error("環境檢查異常，流程已強制留置在步驟 1。");
      }
    } catch {
      message.error("後端通訊異常");
    } finally {
      setLoading(false);
    }
  };

  // 步驟 1 的專用【重新檢查】按鈕方法
  const handleRecheckAud = async () => {
    setLoading(true);
    try {
      const res = await window.eel.run_stage_initial()();
      if (res && res.status === "success") {
        setAudWarning(false);
        setCurrentStep(1); // 檢測正確，直接幫他解鎖並跳到步驟 2
        message.success("環境路徑重新檢查通過！已順利解鎖並切換至步驟 2。");
      } else {
        setAudWarning(true);
        setCurrentStep(0); // 不正確就繼續死守步驟 1
        message.warning("重新檢查失敗：系統依舊找不到 'aud' 資料夾。");
      }
    } catch {
      message.error("後端通訊異常");
    } finally {
      setLoading(false);
    }
  };

  // 2. 我已確認 TipTop 主機 shell 執行完畢，前往下一步
  const handleShellExecutedNext = () => {
    setCurrentStep(2); // 前進至步驟 3
    message.info("已記錄 Shell 執行確認，進入步驟 3：合併本地 Diff 差異檔。");
  };

  // 3. 執行合併本地 Diff 差異檔 (步驟 3)
  const handleStageMergeDiff = async () => {
    await runBackendStage(
      "步驟 3",
      "run_stage_merge_diff",
      (res) => {
        setCurrentStep(3); // 前進至步驟 4
        message.success(res.message || "附件二合併成功！進入步驟 4。");
      },
      "附件二合併失敗"
    );
  };

  // 4. 我已確認 CR 主機批次檔執行完畢並放回 CSV，前往下一步
  const handleBatExecutedNext = () => {
    setCurrentStep(4); // 前進至步驟 5
    message.info("已記錄 CR 批次檔確認，進入步驟 5：處理附件三。");
  };

  // 5. 處理附件三 CSV 整合
  const handleStageProcessAttachmentThree = async () => {
    await runBackendStage(
      "步驟 5",
      "run_stage_process_attachment_three",
      (res) => {
        setCurrentStep(5); // 前進至步驟 6
        message.success(res.message || "附件三處理完成！進入步驟 6 交叉大比對。");
      },
      "附件三處理失敗"
    );
  };

  // 6. 啟動稽核交叉大比對
  const handleStageFinalAudit = async () => {
    await runBackendStage(
      "步驟 6",
      "run_stage_final_audit",
      (res) => {
        setSystemState({
          todayStr: res.today_str || '',
          folder: res.folder || '',
          reportPath: res.report_path || ''
        });
        setCurrentStep(6); // 前進至步驟 7
        message.success("稽核大比對完成，產出實體報告！");
      },
      "比對失敗"
    );
  };

  // 7. 人工查核確認完成
  const handleFinalConfirmNext = () => {
    setCurrentStep(7); // 前進至步驟 8
    message.success("報告查核無誤！進入最後步驟 8 同步網碟。");
  };

  // 8. 正式同步發布至網路磁碟
  const handleDeployToNetwork = async () => {
    await runBackendStage(
      "步驟 8",
      "run_stage_deploy_network",
      () => {
        setIsDeployed(true);
        message.success("全量檔案已成功同步至 DataCenter 備查指定目錄！");
      },
      "發布失敗"
    );
  };

  const handleReset = () => {
    setCurrentStep(0);
    setLogMessages([]);
    setIsDeployed(false);
    setAudWarning(false);
    setSystemState(initialSystemState);
    addLog("面板已成功重置，可以開始執行新一輪查核。");
  };

  return (
    <div className="app-container">
      <HeaderSection backendConnected={backendConnected} />

      {audWarning && (
        <div style={{ margin: '12px 24px 0 24px' }}>
          <Alert
            message="本地執行環境異常（核心安全防線鎖定中）"
            description="系統在您的專案根目錄下找不到「aud」資料夾。流程已強制卡死在步驟 1。請手動建立名為 aud 的資料夾，隨後點擊下方操作台的「重新檢查」按鈕解除鎖定。"
            type="error"
            showIcon
          />
        </div>
      )}

      <StepProgress currentStep={currentStep} />

      <div className="main-layout">
        <div className="main-row">
          <ControlPanel
            currentStep={currentStep}
            loading={loading}
            systemState={systemState}
            isDeployed={isDeployed}
            audWarning={audWarning}
            onRecheckAud={handleRecheckAud}
            onStageInitial={handleStageInitial}
            onShellExecutedNext={handleShellExecutedNext}
            onStageMergeDiff={handleStageMergeDiff}
            onBatExecutedNext={handleBatExecutedNext}
            onStageProcessAttachmentThree={handleStageProcessAttachmentThree}
            onStageFinalAudit={handleStageFinalAudit}
            onFinalConfirmNext={handleFinalConfirmNext}
            onDeployToNetwork={handleDeployToNetwork}
            onReset={handleReset}
          />
          <TerminalLog logMessages={logMessages} logEndRef={logEndRef} />
        </div>
      </div>
    </div>
  );
}

export default App;
