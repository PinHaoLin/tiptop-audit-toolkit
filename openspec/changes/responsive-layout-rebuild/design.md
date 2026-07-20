# Design

## Container

`.app-shell` 使用 `box-sizing: border-box` 與固定最大內容寬度。所有主要區塊使用 `width: 100%`、`max-width` 與自動左右邊界，避免某一個子元件讓區塊突破共同邊界。

## Grid

桌面工作區使用 `minmax(0, 1fr)` 搭配受限寬度的側欄。所有 Grid 子項目與 Ant Design Card 設置 `min-width: 0`，內容節點使用 `max-width: 100%`。

## Breakpoints

- 981px 以上：主工作卡與執行環境雙欄。
- 721px 至 980px：工作區上下堆疊，保留平板可讀寬度。
- 720px 以下：流程元件可在自己的區域水平捲動，主卡內按鈕與標題改為窄版布局。

## Verification

- 檢查頁面主要區塊的 computed width 不得超過 `.app-shell` 內容寬度。
- 執行 ESLint、Vite production build、Python 編譯與 PyInstaller 打包。
