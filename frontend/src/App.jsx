import { useEffect, useMemo, useState } from 'react';
import { Alert, message } from 'antd';
import HeaderSection from './components/HeaderSection';
import StepProgress from './components/StepProgress';
import ControlPanel from './components/ControlPanel';
import './App.css';

const initialSystemState = {
  todayStr: '',
  folder: '',
  reportPath: '',
};

function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [runtimeInfo, setRuntimeInfo] = useState(null);
  const [systemState, setSystemState] = useState(initialSystemState);
  const [isDeployed, setIsDeployed] = useState(false);
  const [lastError, setLastError] = useState('');

  const backendConnected = useMemo(() => Boolean(window.eel), []);

  const refreshRuntimeInfo = async () => {
    if (!window.eel?.get_runtime_info) return;
    try {
      const info = await window.eel.get_runtime_info()();
      setRuntimeInfo(info);
    } catch {
      setRuntimeInfo(null);
    }
  };

  useEffect(() => {
    const timer = window.setTimeout(() => {
      refreshRuntimeInfo();
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  const runBackendStage = async (stageFn, onSuccess) => {
    if (!window.eel?.[stageFn]) {
      message.error('後端尚未連線，請從 exe 啟動程式。');
      return;
    }

    setLoading(true);
    setLastError('');
    try {
      const result = await window.eel[stageFn]()();
      await refreshRuntimeInfo();

      if (result?.status === 'success') {
        onSuccess?.(result);
        message.success(result.message || '作業完成');
      } else {
        const errMessage = result?.message || '作業失敗';
        setLastError(errMessage);
        message.error(errMessage);
      }
    } catch {
      const errMessage = '後端通訊異常，請重新啟動程式後再試。';
      setLastError(errMessage);
      message.error(errMessage);
    } finally {
      setLoading(false);
    }
  };

  const actions = {
    initialize: () =>
      runBackendStage('run_stage_initial', (result) => {
        setSystemState((prev) => ({
          ...prev,
          todayStr: result.today_str || '',
          folder: result.folder || '',
        }));
        setCurrentStep(1);
      }),
    confirmTipTop: () => {
      setCurrentStep(2);
      message.info('已記錄 TipTop 執行完成，請繼續合併附件二。');
    },
    mergeDiff: () =>
      runBackendStage('run_stage_merge_diff', () => {
        setCurrentStep(3);
      }),
    confirmCr: () => {
      setCurrentStep(4);
      message.info('已記錄 CR 主機執行完成，請繼續合併附件三。');
    },
    mergeCsv: () =>
      runBackendStage('run_stage_process_attachment_three', () => {
        setCurrentStep(5);
      }),
    finalAudit: () =>
      runBackendStage('run_stage_final_audit', (result) => {
        setSystemState({
          todayStr: result.today_str || '',
          folder: result.folder || '',
          reportPath: result.report_path || '',
        });
        setCurrentStep(6);
      }),
    confirmReport: () => {
      setCurrentStep(7);
      message.success('已確認報告，準備同步至 DataCenter。');
    },
    deploy: () =>
      runBackendStage('run_stage_deploy_network', () => {
        setIsDeployed(true);
      }),
    reset: () => {
      setCurrentStep(0);
      setSystemState(initialSystemState);
      setIsDeployed(false);
      setLastError('');
      refreshRuntimeInfo();
    },
  };

  return (
    <div className="app-shell">
      <HeaderSection backendConnected={backendConnected} runtimeInfo={runtimeInfo} />

      {!backendConnected && (
        <Alert
          className="top-alert"
          message="後端尚未連線"
          description="請使用打包後的 exe 啟動，不要直接開啟前端頁面。"
          type="error"
          showIcon
        />
      )}

      {lastError && (
        <Alert
          className="top-alert"
          message="目前作業未完成"
          description={lastError}
          type="error"
          showIcon
        />
      )}

      <StepProgress currentStep={currentStep} />

      <ControlPanel
        currentStep={currentStep}
        loading={loading}
        runtimeInfo={runtimeInfo}
        systemState={systemState}
        isDeployed={isDeployed}
        actions={actions}
      />
    </div>
  );
}

export default App;
