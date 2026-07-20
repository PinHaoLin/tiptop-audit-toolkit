import { Card, Steps } from 'antd';

const items = [
  { title: '初始化', description: '建立工作區' },
  { title: 'TipTop', description: '執行 shell' },
  { title: '附件二', description: '合併 Diff' },
  { title: 'CR 主機', description: '執行 bat' },
  { title: '附件三', description: '合併 CSV' },
  { title: '比對', description: '產出報告' },
  { title: '確認', description: '人工覆核' },
  { title: '同步', description: 'DataCenter' },
];

function StepProgress({ currentStep }) {
  return (
    <Card className="steps-card">
      <Steps current={currentStep} size="small" labelPlacement="vertical" items={items} />
    </Card>
  );
}

export default StepProgress;
