import React from 'react';
import { Card, Steps } from 'antd';

function StepProgress({ currentStep }) {
  return (
    <Card className="card-steps">
      <Steps
        current={currentStep}
        items={[
          { title: '環境初始化', description: '建立目錄與備份 Excel' },
          { title: '處理附件二', description: '合併本地 Diff 檔案' },
          { title: '處理附件三', description: 'CSV 稽核與終極比對' },
          { title: '查核圓滿完成', description: '產出報告書' },
        ]}
      />
    </Card>
  );
}

export default StepProgress;
