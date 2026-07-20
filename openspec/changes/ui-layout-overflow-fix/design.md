# Design

## Path Display Contract

`PathLine` 必須在任何父層寬度下保持可縮小。路徑文字使用單行顯示，超出欄位時由元件自身處理水平捲動；不得依內容寬度增加 Grid track 或 Card 寬度。

## Layout Rules

- `.primary-panel`、`.side-panel`、`.path-line` 與路徑文字節點設置 `min-width: 0`。
- 路徑文字節點使用 `display: block`、受限寬度與 `overflow-x: auto`。
- 報告路徑與側欄路徑沿用同一個 `PathLine` 元件，避免不同頁面狀態產生不同寬度行為。
- 桌面版維持左右欄；窄版維持既有上下堆疊行為。

## Verification

- 執行 ESLint。
- 執行 Vite production build。
- 重新封裝 EXE，確認輸出存在且 `dist` 不會新增 `aud` 或暫存覆核資料夾。
