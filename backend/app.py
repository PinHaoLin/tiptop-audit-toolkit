import eel
import os
import sys
import core_logic
from datetime import datetime

# 🎯 1. 動態取得網頁資源絕對路徑 (前端打包相容)
if getattr(sys, 'frozen', False):
    base_path = os.path.join(sys._MEIPASS, 'web')
else:
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/dist')

eel.init(base_path)

# 🎯 2. 動態取得目前專案資料夾「tiptop-audit-toolkit」的絕對路徑
if getattr(sys, 'frozen', False):
    PROJECT_ROOT_DIR = os.path.dirname(sys.executable)
else:
    PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 🎯 明確定義跟 z_chk_all.sh 絕對同級的核心 aud 資料夾路徑
AUD_DIR_PATH = os.path.join(PROJECT_ROOT_DIR, "aud")
SH_TARGET_DIR = PROJECT_ROOT_DIR
SH_FILENAME = "z_chk_all.sh"

state = {
    "generated_folder": None,
    "target_att_two_name": None,
    "target_att_three_name": None,
    "current_today_str": None,
    "actual_excel_path": None
}

BASE_DIRECTORY = r"\\192.168.1.4\DataCenter\IT\IT部門內專用\ALL-系統及設備設定異動紀錄表\會計師查核用\1.每週程式修改記錄\2026\00.僅MIS內部參考(不對外提供)"
EXCEL_SOURCE = r"\\192.168.1.4\DataCenter\IT\IT部門內專用\系統-資訊系統及需求記錄\E.Tiptop GP\02.GP程式修改記錄vNEW.xlsx"
EXCEL_BASE_NAME = r"02.GP程式修改記錄vNEW.xlsx"
REMOTE_NETWORK_BASE_DIR = BASE_DIRECTORY

@eel.expose
def run_stage_initial():
    try:
        print("\n============================================================", flush=True)
        print("🚀 核心防線檢查：正在即時偵測 'aud' 資料夾是否存在...", flush=True)
        print("============================================================", flush=True)

        # 🎯 自動計算真正的專案根目錄 (確保不論是在 backend 還是根目錄執行都能對齊)
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(current_file_dir) == "backend":
            real_project_root = os.path.abspath(os.path.join(current_file_dir, ".."))
        else:
            real_project_root = current_file_dir

        # 🎯 重新定義精準的實體 aud 路徑
        resolved_aud_path = os.path.join(real_project_root, "aud")

        print(f"🔎 Python 正在檢查的實體絕對路徑為:\n👉 {resolved_aud_path}", flush=True)

        # 🎯 實時偵測實體硬碟路徑
        if not os.path.exists(resolved_aud_path):
            print(f"❌ 偵測失敗：該實體路徑在硬碟上不存在！", flush=True)
            return {
                "status": "error",
                "error_type": "AUD_MISSING",
                "message": f"環境初始化失敗：找不到關鍵的 'aud' 資料夾。\n系統預期路徑：{resolved_aud_path}"
            }

        print(f"✅ 偵測成功：'aud' 資料夾實體存在！放行進入內部邏輯。", flush=True)

        # 🟢 【精準對齊】接收來自 core_logic 回傳的 5 個核心參數
        res_folder, att_two, att_three, t_str, aud_warn = core_logic.backup_and_rename_by_latest_folder(excel_source_path=EXCEL_SOURCE)

        # 🎯 【核心修正】將初始化後的狀態，完整刷新回 app.py 的全局變數 state 中
        state["current_today_str"] = t_str
        state["generated_folder"] = res_folder
        state["target_att_two_name"] = att_two
        state["target_att_three_name"] = att_three

        # 🎯 根據動態日期計算，精準還原備份在本機的 Excel 實體檔案路徑 (提供給後續大比對步驟使用)
        expected_excel_name = f"02.GP程式修改記錄v{t_str}.xlsx"
        state["actual_excel_path"] = os.path.join(res_folder, expected_excel_name)

        print(f"📌 狀態同步成功：", flush=True)
        print(f"   ↳ 今日工作區: {state['generated_folder']}", flush=True)
        print(f"   ↳ 本機備份 Excel 鎖定: {state['actual_excel_path']}", flush=True)

        return {"status": "success", "message": "環境初始化成功！"}

    except Exception as e:
        print(f"  ❌ 發生未知嚴重錯誤: {str(e)}\n", flush=True)
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_merge_diff():
    try:
        print("\n============================================================", flush=True)
        print("🚀 第三階段：開始讀取本地 Diff 檔案並寫入網碟附件二...", flush=True)
        print("============================================================", flush=True)

        if not state["generated_folder"]:
            return {"status": "error", "message": "核心遺失今日資料夾狀態，請重置並重新執行步驟一。"}

        core_logic.merge_diff_files_to_attachment(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_two_name"]
        )
        core_logic.modify_bat_scripts(SH_TARGET_DIR)

        print("  🟢 Diff 檔案合併與本地 bat 重構完成。", flush=True)
        return {"status": "success", "message": "Diff 合併成功"}
    except Exception as e:
        print(f"  ❌ 發生嚴重錯誤: {str(e)}", flush=True)
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_process_attachment_three():
    """ 🎯 補上漏掉的步驟 5 接口：整合 RDP 產出的 4 個 CSV 到附件三文字檔 """
    try:
        print("\n============================================================", flush=True)
        print("🚀 第五階段：開始自本地核心 aud 目錄抓取 CSV 並整合至附件三...", flush=True)
        print("============================================================", flush=True)

        if not state["generated_folder"]:
            return {"status": "error", "message": "核心遺失今日資料夾狀態，請重置並重新執行步驟一。"}

        # 將 RDP 撈回來的 CSV 資料精準寫入今日覆核區的附件三
        core_logic.merge_csv_files_to_attachment_three(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_three_name"],
            today_str=state["current_today_str"]
        )

        print("  🟢 附件三 CSV 資料整合重組完成。", flush=True)
        return {"status": "success", "message": "附件三處理完成！"}
    except Exception as e:
        print(f"  ❌ 步驟五發生嚴重錯誤: {str(e)}", flush=True)
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_final_audit():
    """ 🎯 步驟 6 接口：專注於 Excel 與異動檔案的終極稽核交叉大比對 """
    try:
        print("\n============================================================", flush=True)
        print("🚀 第六階段：執行 Tiptop GP 異動單據與簽核檔案終極稽核大比對...", flush=True)
        print("============================================================", flush=True)

        if not state["actual_excel_path"] or not os.path.exists(state["actual_excel_path"]):
            return {"status": "error", "message": "找不到本機備份 Excel，無法執行比對。"}

        # 專注於產出交叉稽核比對報告
        core_logic.audit_and_compare_logs(
            excel_path=state["actual_excel_path"],
            att_two_path=os.path.join(state["generated_folder"], state["target_att_two_name"]),
            att_three_path=os.path.join(state["generated_folder"], state["target_att_three_name"]),
            output_log_dir=AUD_DIR_PATH,
            today_str=state["current_today_str"]
        )

        report_file_name = f"{state['current_today_str']}_稽核比對結果報告.txt"
        report_full_path = os.path.join(AUD_DIR_PATH, report_file_name)

        print(f"\n🛑 [人工覆核中斷點] 本機暫存稽核報告已順利產出至核心目錄：{report_full_path}", flush=True)
        return {
            "status": "success",
            "report_path": report_full_path,
            "folder": state["generated_folder"],
            "today_str": state["current_today_str"]  # 💡 補上 res.today_str 回傳給前端 App.jsx 使用
        }
    except Exception as e:
        print(f"  ❌ 步驟六發生嚴重錯誤: {str(e)}\n", flush=True)
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_deploy_network():
    try:
        print("\n============================================================", flush=True)
        print("🚀 第體階段：放行訊號確認，開始全量同步至網路共用磁碟...", flush=True)
        print("============================================================", flush=True)

        core_logic.deploy_local_folder_to_network_share(state["generated_folder"], REMOTE_NETWORK_BASE_DIR)

        print("\n🎉 🎉 【大功告成】每週定期程序修改查核作業與網碟發布圓滿結束！", flush=True)
        return {"status": "success", "message": "網碟全量同步派送成功"}
    except Exception as e:
        print(f"  ❌ 網碟同步失敗: {str(e)}", flush=True)
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    try:
        eel.start('index.html', mode='edge', size=(1280, 800))
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
