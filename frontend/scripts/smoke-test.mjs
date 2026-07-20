import { readFile } from 'node:fs/promises';
import path from 'node:path';

const rootDir = path.resolve(import.meta.dirname, '..');

async function readProjectFile(relativePath) {
  return readFile(path.join(rootDir, relativePath), 'utf8');
}

const checks = [
  {
    name: 'App keeps shared backend stage handling',
    run: async () => {
      const app = await readProjectFile('src/App.jsx');
      return app.includes('runBackendStage') && app.includes('run_stage_merge_diff');
    },
  },
  {
    name: 'App renders the audit workflow panels',
    run: async () => {
      const app = await readProjectFile('src/App.jsx');
      return ['HeaderSection', 'StepProgress', 'ControlPanel', 'TerminalLog']
        .every((needle) => app.includes(needle));
    },
  },
  {
    name: 'Responsive workflow layout styling exists',
    run: async () => {
      const css = await readProjectFile('src/App.css');
      return css.includes('.main-row') && css.includes('@media screen and (max-width: 1100px)');
    },
  },
];

let failed = 0;

for (const check of checks) {
  const passed = await check.run();
  const marker = passed ? 'PASS' : 'FAIL';
  console.log(`${marker} ${check.name}`);
  if (!passed) {
    failed += 1;
  }
}

if (failed > 0) {
  console.error(`Smoke test failed: ${failed}/${checks.length} checks did not pass.`);
  process.exit(1);
}

console.log(`Smoke test passed: ${checks.length}/${checks.length} checks passed.`);
