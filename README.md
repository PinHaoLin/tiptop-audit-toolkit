# TIPTOP GP 程式覆核自動化系統

這個工具用來協助 MIS 每週執行 TIPTOP GP 程式修改覆核作業，包含建立本週覆核資料夾、更新查核腳本日期、合併附件二/附件三資料、交叉比對 Excel 紀錄，最後將成果同步到 DataCenter 指定路徑。

## 給同事使用

直接使用下列檔案即可：

```text
dist\TIPTOP_Audit_Toolkit.exe
```

目前 `.exe` 已套用原創網通覆核圖示，設計方向參考 Edimax 官網的網路設備、無線 AP、交換器與企業網通產品語彙；圖示檔保留於 `backend\edimax_audit.ico`。

第一次執行時，程式會自動在 `.exe` 同層建立必要資料夾：

```text
aud
程式修改週覆核記錄(暫存)
```

請不要刪除這兩個資料夾。`aud` 用來放置 `z_chk_all.sh`、diff 結果、CSV 與稽核報告；`程式修改週覆核記錄(暫存)` 用來存放每週產出的覆核資料。

若 `.exe` 放在 `dist` 內執行，程式會使用上一層專案根目錄的 `aud` 與 `程式修改週覆核記錄(暫存)`，不會在 `dist` 內另外建立資料夾。

## 使用流程

1. 執行 `TIPTOP_Audit_Toolkit.exe`。
2. 步驟 1 建立本週覆核資料夾，並複製 GP 程式修改記錄 Excel。
3. 將 `aud\z_chk_all.sh` 上傳到 TipTop 主機並執行。
4. 將 TipTop 產出的 `4fd_diff.txt`、`4gl_diff.txt` 放回本機 `aud`。
5. 執行附件二合併。
6. 將 `aud\rpt_diff.bat`、`aud\xml_diff.bat` 上傳到 CR 主機執行。
7. 將產出的 4 個 CSV 放回本機 `aud`。
8. 執行附件三合併與 Excel 交叉比對。
9. 人工確認稽核報告無誤後，上傳至 DataCenter。

## 重要資料夾

```text
aud
```

本機查核工作資料夾，包含 shell/bat 腳本、diff 檔、CSV 檔與稽核報告。

```text
程式修改週覆核記錄(暫存)
```

本機每週覆核暫存區，程式會依日期建立 `程式修改週覆核記錄-YYYYMMDD` 子資料夾。

```text
dist
```

打包後的交付資料夾，目前最終交付檔為 `TIPTOP_Audit_Toolkit.exe`。

## 開發與重新打包

需要修改程式後重新打包時，請先安裝前端依賴：

```powershell
cd frontend
npm install
npm.cmd run build
cd ..
pyinstaller --clean --noconfirm app.spec
```

重新打包完成後，新的交付檔會出現在：

```text
dist\TIPTOP_Audit_Toolkit.exe
```

## 專案瘦身說明

為了方便交付，專案已移除不影響執行的 PyInstaller 快取與舊建置資料，例如：

```text
backend\build
backend\dist
backend\__pycache__
```

`frontend\node_modules` 目前保留，方便後續修改 UI 後直接重新 build 與打包。

