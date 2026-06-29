import React from 'react';
import { Card, Steps } from 'antd';

function StepProgress({ currentStep }) {
  return (
    <Card className="card-steps" style={{ marginBottom: '16px' }}>
      <Steps
        current={currentStep}
        size="small"
        labelPlacement="vertical"
        items={[
          { title: '環境初始化', description: '建目錄與複製 Excel' },
          { title: 'TipTop 執行', description: '上傳並執行 shell 檔案' },
          { title: '處理附件二', description: '合併本機 Diff 檔案' },
          { title: 'CR 主機執行', description: '上傳並執行 bat 檔案' },
          { title: '處理附件三', description: '合併本機 CSV 記錄' },
          { title: '稽核比對', description: '交叉核對系統異動與紀錄' },
          { title: '上傳最後確認', description: '最終檢視本次檢核報告' },
          { title: '查核作業完成', description: '上傳至DataCenter' },
        ]}
      />
    </Card>
  );
}

export default StepProgress;
