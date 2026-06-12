import eel
import os
import sys
import core_logic

# 🎯 動態取得網頁資源絕對路徑
if getattr(sys, 'frozen', False):
    base_path = os.path.join(sys._MEIPASS, 'web')
else:
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/dist')

eel.init(base_path)

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
SH_TARGET_DIR = r"D:\1.Tony_Worklog\0.TIPTOP_work\topcust\aud"
SH_FILENAME = "z_chk_all.sh"

def log_to_frontend(msg):
    """ 在各關卡開始前與終端機印出提示 """
    print(f"[Backend Log] {msg}", flush=True)
    if hasattr(eel, 'add_log_from_backend'):
        eel.add_log_from_backend(msg)()

@eel.expose
def run_stage_initial():
    try:
        log_to_frontend("============================================================")
        log_to_frontend("🚀 第一、二階段：開始執行環境初始化與 z_chk_all.sh 日期更新...")
        log_to_frontend("============================================================")

        gen_folder, att_two, att_three, today_str = core_logic.backup_and_rename_by_latest_folder(BASE_DIRECTORY)

        if not gen_folder:
            return {"status": "error", "message": "找不到母資料夾或網路路徑無法連線。"}

        state["generated_folder"] = gen_folder
        state["target_att_two_name"] = att_two
        state["target_att_three_name"] = att_three
        state["current_today_str"] = today_str

        log_to_frontend(f"  🟢 成功辨識基準日：[{today_str}]，備份 Excel 與更新 sh 完成。")
        return {
            "status": "success",
            "message": "初始化成功",
            "data": {"today_str": today_str, "folder": gen_folder}
        }
    except Exception as e:
        log_to_frontend(f"  ❌ 發生嚴重錯誤: {str(e)}")
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_merge_diff():
    try:
        log_to_frontend("============================================================")
        log_to_frontend("🚀 第三階段：開始讀取本地 Diff 檔案並寫入網碟附件二...")
        log_to_frontend("============================================================")

        core_logic.merge_diff_files_to_attachment(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_two_name"]
        )
        core_logic.modify_bat_scripts(SH_TARGET_DIR)

        log_to_frontend("  🟢 Diff 檔案合併與本地 bat 重構完成。")
        return {"status": "success", "message": "Diff 合併成功"}
    except Exception as e:
        log_to_frontend(f"  ❌ 發生嚴重錯誤: {str(e)}")
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_final_audit():
    try:
        log_to_frontend("============================================================")
        log_to_frontend("🚀 第四、五、六階段：整合遠端桌面 CSV 資料並執行終極稽核大比對...")
        log_to_frontend("============================================================")

        # 1. 整合 CSV 到附件三
        core_logic.merge_csv_files_to_attachment_three(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_three_name"],
            today_str=state["current_today_str"]
        )

        # 2. 執行核心比對 (走純 Python 同步，速度最快！)
        core_logic.audit_and_compare_logs(
            excel_path=state["actual_excel_path"],
            att_two_path=os.path.join(state["generated_folder"], state["target_att_two_name"]),
            att_three_path=os.path.join(state["generated_folder"], state["target_att_three_name"]),
            output_log_dir=SH_TARGET_DIR,
            today_str=state["current_today_str"]
        )

        report_file_name = f"{state['current_today_str']}_稽核比對結果報告.txt"
        report_full_path = os.path.join(SH_TARGET_DIR, report_file_name)

        log_to_frontend("\n🛑 [人工覆核中斷點] 本機暫存稽核報告與附件已順利產出。")
        return {"status": "success", "report_path": report_full_path, "folder": state["generated_folder"]}
    except Exception as e:
        log_to_frontend(f"  ❌ 發生嚴重錯誤: {str(e)}")
        return {"status": "error", "message": str(e)}

@eel.expose
def run_stage_deploy_network():
    try:
        log_to_frontend("============================================================")
        log_to_frontend("🚀 第七階段：放行訊號確認，開始全量同步至網路共用磁碟...")
        log_to_frontend("============================================================")

        core_logic.deploy_local_folder_to_network_share(state["generated_folder"], BASE_DIRECTORY)

        log_to_frontend("\n🎉 🎉 【大功告成】每週定期程序修改查核作業與網碟發布圓滿結束！")
        return {"status": "success", "message": "網碟全量同步派送成功"}
    except Exception as e:
        log_to_frontend(f"  ❌ 網碟同步失敗: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    try:
        eel.start('index.html', mode='edge', size=(1280, 800))
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
