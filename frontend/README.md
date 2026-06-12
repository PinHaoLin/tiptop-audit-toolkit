# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

本工具為 MIS 每週定期程序修改查核作業的自動化桌面軟體，採用 React (Frontend) + Python Eel (Backend) 架構開發，並封裝為單一獨立 .exe 執行檔，免安裝 Python 環境即可供運維同仁雙擊使用。

🛠️ 開發環境與技術棧
前端介面 (Frontend): React 18+, Vite, Ant Design (UI 組件), Lucide React (圖標)

後端核心 (Backend): Python 3.13+, Eel 框架 (Web GUI 對接)

打包工具: PyInstaller

⚠️ 部署與使用注意事項 (同事交付指南)
當將本工具交付給其他運維同事使用時，請務必提醒以下環境配置：

1. 📂 實體資料夾目錄結構 (關鍵)
   本工具底層邏輯涉及本地端檔案讀寫，使用者電腦必須建立以下一模一樣的目錄結構，否則執行到第三階段抓取 CSV 或產出報告時會拋出路徑找不到的錯誤：

本地工作目錄： D:\1.Tony_Worklog\0.TIPTOP_work\topcust\aud

💡 註：若後續有優化為相對路徑，請依新版調整此說明。

2. 🔐 網路磁碟機 (網碟) 存取權限
   執行第一階段「環境初始化」與第二階段「Diff 自動合併」時，後端會實打實連線至公司內部資料中心網碟。請確保執行電腦具備以下路徑的讀寫權限，且網路連線正常（若在廠外需先連線公司 VPN）：

每週程式修改記錄路徑： \\192.168.1.4\DataCenter\IT\...

GP 程式修改記錄 Excel 源： \\192.168.1.4\DataCenter\IT\...\02.GP程式修改記錄vNEW.xlsx

3. 🛡️ 防毒軟體 / EDR 端點攔截
   由於 PyInstaller 打包的單一 .exe 執行檔在啟動時，會自動將前端網頁資源解壓至系統臨時目錄（Temp/\_MEIxxxx）。部分企業資安軟體或 Windows Defender 可能會將此行為誤判為風險並鎖定檔案，導致啟動時彈出 WinError 5 存取被拒 或無響應。

解決方案： 請將本工具 app.exe 加至防毒軟體的信任白名單，或在打包/執行時暫時關閉即時掃描。

4. 🌐 預設瀏覽器核心
   本工具在 Windows 環境下會自動喚醒作業系統內建的 Microsoft Edge 核心來渲染操作面板，請確保系統未徹底閹割或禁用 Edge 瀏覽器。

🚀 研發維護與二次開發指南
如果你需要修改功能或重新編譯，請依循以下步驟：

1. 前端編譯 (Frontend Build)
   每當修改了 frontend/src/底下的 React 程式碼後，必須重新將其打包成靜態網頁：
   Bash
   cd frontend
   npm run build
   編譯完成後，會在 frontend/ 目錄下生成 dist/ 資料夾。

2. 後端除錯 (Backend Run)
   在開發階段，如果想直接啟動 Python 測試：
   Bash
   cd backend
   python app.py

3. 📦 終極釋放：重新封裝成 .exe
   當前後端皆修改完畢，欲產出正式釋出包時，請至 backend/ 目錄下執行以下強效打包指令。

注意： 打包前請務必先關閉工作管理員中所有殘留的 app.exe 背景程序，避免檔案被佔用導致編譯失敗。

Bash

# 1. 強殺可能殘留的背景程序

taskkill /f /im app.exe

# 2. 清除舊有編譯快取

rmdir /s /q build dist
del app.spec

# 3. 執行 Eel 專用標準封裝

pyinstaller --clean --noconsole --onefile --add-data "../frontend/dist;web" app.py
封裝完成後，全新的獨立執行檔將生成於 backend/dist/app.exe，即可直接複製、建立桌面捷徑或發送給部門同事使用。

📝 每週標準標準查核作業流程 (SOP)
第一階段： 點擊【環境初始化】，系統自動分析網碟、備份 Excel 並更名、自動修改本地 z_chk_all.sh 的覆核日期。

手動檢核 1： 將本地更新好的 z_chk_all.sh 上傳至 Linux 伺服器執行。

第二階段： 點擊【Diff 自動合併】，系統自動讀取本地產出的 4gl/4fd_diff 並寫入網碟附件二，同時自動重構遠端批次檔。

手動檢核 2： 透過 RDP 登入主機執行 rpt_diff.bat 與 xml_diff.bat，將產出的 4 個 CSV 下載回本地 aud 目錄。

第三階段： 點擊【最終比對稽核】，系統自動整合 CSV 至網碟附件三，並自動與 Excel 的紅字修改記錄進行 6 大規則終極比對，於本地產出純文字稽核報告書。
