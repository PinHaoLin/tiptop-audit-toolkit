import eel
import os
import sys
import core_logic

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

# 🎯 【關鍵修正】明確定義跟 z_chk_all.sh 絕對同級的核心 aud 資料夾路徑
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
        print("🚀 第一、二階段：開始執行環境初始化與 z_chk_all.sh 日期更新...", flush=True)
        print("============================================================", flush=True)

        # 1. 初始化本機工作目錄 (解構出 aud_warning)
        gen_folder, att_two, att_three, today_str, aud_warning = core_logic.backup_and_rename_by_latest_folder()

        if not gen_folder:
            return {"status": "error", "message": "本機工作暫存區建立失敗。"}

        state["generated_folder"] = gen_folder
        state["target_att_two_name"] = att_two
        state["target_att_three_name"] = att_three
        state["current_today_str"] = today_str

        # 2. 從遠端網碟備份 Excel 到本機今日工作區
        print("⏳ 正在連線遠端網路磁碟，備份最新修改記錄 Excel...", flush=True)
        copied_excel = core_logic.copy_and_rename_file(EXCEL_SOURCE, gen_folder, EXCEL_BASE_NAME)

        if not copied_excel:
            return {"status": "error", "message": "無法讀取網碟 Excel，請確認網路磁碟連線是否正常！"}

        state["actual_excel_path"] = copied_excel

        # 3. 更新本地的 Linux 查核腳本日期
        core_logic.modify_sh_script(SH_TARGET_DIR, SH_FILENAME)

        print(f"  🟢 成功辨識基準日：[{today_str}]，本機工作區準備就緒。", flush=True)
        return {
            "status": "success",
            "message": "初始化成功",
            "data": {
                "today_str": today_str,
                "folder": gen_folder,
                "aud_warning": aud_warning
            }
        }
    except Exception as e:
        print(f"  ❌ 發生嚴重錯誤: {str(e)}", flush=True)
        return {"status": "error", "message": str(e)}

@eel.expose
def recheck_aud_folder():
    """ 🎯 提供前端單獨、重複點擊重新檢查的功能 """
    try:
        exists = os.path.exists(AUD_DIR_PATH)
        print(f"🔄 接收到前端重新檢查訊號。檢測路徑: {AUD_DIR_PATH} ｜ 狀態: {'存在' if exists else '不存在'}", flush=True)
        return {"status": "success", "aud_exists": exists}
    except Exception as e:
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
def run_stage_final_audit():
    try:
        print("\n============================================================", flush=True)
        print("🚀 第四、五、六階段：整合遠端桌面 CSV 資料並執行終極稽核大比對...", flush=True)
        print("============================================================", flush=True)

        if not state["actual_excel_path"] or not os.path.exists(state["actual_excel_path"]):
            return {"status": "error", "message": "找不到本機備份 Excel，無法執行比對。"}

        core_logic.merge_csv_files_to_attachment_three(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_three_name"],
            today_str=state["current_today_str"]
        )

        # 🎯【核心修正】將輸出目錄徹底換成 AUD_DIR_PATH，不再使用舊的 SH_TARGET_DIR
        core_logic.audit_and_compare_logs(
            excel_path=state["actual_excel_path"],
            att_two_path=os.path.join(state["generated_folder"], state["target_att_two_name"]),
            att_three_path=os.path.join(state["generated_folder"], state["target_att_three_name"]),
            output_log_dir=AUD_DIR_PATH,
            today_str=state["current_today_str"]
        )

        # 🎯【核心修正】確保前端主控台點選複製與呈現的路徑也是完全切換至 aud 資料夾
        report_file_name = f"{state['current_today_str']}_稽核比對結果報告.txt"
        report_full_path = os.path.join(AUD_DIR_PATH, report_file_name)

        print(f"\n🛑 [人工覆核中斷點] 本機暫存稽核報告已順利產出至核心目錄：{report_full_path}", flush=True)
        return {"status": "success", "report_path": report_full_path, "folder": state["generated_folder"]}
    except Exception as e:
        print(f"  ❌ 發生嚴重錯誤: {str(e)}\n", flush=True)
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
