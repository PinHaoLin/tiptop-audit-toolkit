import React, { useState, useEffect, useRef } from 'react';
import { message } from 'antd';
import HeaderSection from './components/HeaderSection';
import StepProgress from './components/StepProgress';
import ControlPanel from './components/ControlPanel';
import TerminalLog from './components/TerminalLog';
import './App.css';

function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [logMessages, setLogMessages] = useState([]);
  const [backendConnected, setBackendConnected] = useState(false);
  const [systemState, setSystemState] = useState({ todayStr: '', folder: '', reportPath: '' });
  const [isDeployed, setIsDeployed] = useState(false);

  const logEndRef = useRef(null);

  const addLog = (msg) => {
    setLogMessages((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  // 監聽 Eel 即時日誌
  useEffect(() => {
    if (window.eel) {
      setBackendConnected(true);
      addLog("🟢 系統提示：成功與 Python Eel 後端建立連線通道！");
      window.eel.add_log_from_backend = (msg) => addLog(msg);
    } else {
      setBackendConnected(false);
      addLog("❌ 系統提示：未偵測到 Eel 核心，請確保使用 python app.py 啟動。");
    }
  }, []);

  const checkEelConnection = () => {
    if (!window.eel) {
      message.error("後端通訊管道未建立！");
      return false;
    }
    return true;
  };

  // 階段 1 與 2：環境初始化
  const handleStageInitial = async () => {
    if (!checkEelConnection()) return;
    setLoading(true);
    addLog("⏳ 已向後端發送【環境初始化】指令，正在連線網碟處理中...");
    try {
      const res = await window.eel.run_stage_initial()();
      if (res && res.status === 'success') {
        setSystemState((prev) => ({ ...prev, todayStr: res.data.todayStr, folder: res.data.folder }));
        setCurrentStep(1);
        message.success("環境初始化成功！");
      } else {
        message.error(res ? res.message : "執行失敗");
      }
    } catch (err) {
      addLog("❌ 通訊異常: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 階段 3：合併 Diff
  const handleStageMergeDiff = async () => {
    if (!checkEelConnection()) return;
    setLoading(true);
    addLog("⏳ 已向後端發送【Diff 自動合併】指令...");
    try {
      const res = await window.eel.run_stage_merge_diff()();
      if (res && res.status === 'success') {
        setCurrentStep(2);
        message.success("Diff 合併完成！");
      } else {
        message.error(res ? res.message : "執行失敗");
      }
    } catch (err) {
      addLog("❌ 通訊異常: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 階段 4, 5, 6：大比對
  const handleStageFinalAudit = async () => {
    if (!checkEelConnection()) return;
    setLoading(true);
    addLog("⏳ 已向後端發送【最終比對稽核】指令，檔案較大請稍候...");
    try {
      const res = await window.eel.run_stage_final_audit()();
      if (res && res.status === 'success') {
        setSystemState((prev) => ({ ...prev, reportPath: res.report_path, folder: res.folder }));
        setCurrentStep(3);
        message.success("本機稽核與報告書產出成功！");
      } else {
        message.error(res ? res.message : "執行失敗");
      }
    } catch (err) {
      addLog("❌ 通訊異常: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 階段 7：派送同步網碟
  const handleDeployToNetwork = async () => {
    if (!checkEelConnection()) return;
    setLoading(true);
    addLog("🚀 收到放行訊號！第七階段啟動：開始全量同步至網路共用磁碟...");
    try {
      const res = await window.eel.run_stage_deploy_network()();
      if (res && res.status === 'success') {
        setIsDeployed(true);
        message.success("網碟全量同步派送成功！");
      } else {
        message.error(res ? res.message : "同步網碟失敗");
      }
    } catch (err) {
      addLog("❌ 網碟通訊異常: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setCurrentStep(0);
    setLogMessages([]);
    setIsDeployed(false);
    setSystemState({ todayStr: '', folder: '', reportPath: '' });
    addLog("🔄 面板已成功重置，可以開始執行新一輪查核。");
  };

  return (
    <div className="app-container">
      <HeaderSection backendConnected={backendConnected} />
      <StepProgress currentStep={currentStep} />

      <div className="main-layout">
        <div className="main-row">
          <ControlPanel
            currentStep={currentStep}
            loading={loading}
            systemState={systemState}
            isDeployed={isDeployed}
            onStageInitial={handleStageInitial}
            onStageMergeDiff={handleStageMergeDiff}
            onStageFinalAudit={handleStageFinalAudit}
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
