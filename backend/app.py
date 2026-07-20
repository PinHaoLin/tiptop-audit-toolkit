import os
import shutil
import sys

import eel

import core_logic


APP_NAME = "TIPTOP_Audit_Toolkit"
REVIEW_FOLDER_NAME = "程式修改週覆核記錄(暫存)"
AUD_FOLDER_NAME = "aud"

BASE_DIRECTORY = r"\\192.168.1.4\DataCenter\IT\IT部門內專用\ALL-系統及設備設定異動紀錄表\會計師查核用\1.每週程式修改記錄\2026\00.僅MIS內部參考(不對外提供)"
EXCEL_SOURCE = r"\\192.168.1.4\DataCenter\IT\IT部門內專用\系統-資訊系統及需求記錄\E.Tiptop GP\02.GP程式修改記錄vNEW.xlsx"
REMOTE_NETWORK_BASE_DIR = BASE_DIRECTORY


def is_frozen():
    return getattr(sys, "frozen", False)


def bundled_path(*parts):
    if is_frozen():
        return os.path.join(sys._MEIPASS, *parts)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *parts))


def runtime_root():
    if is_frozen():
        exe_dir = os.path.dirname(sys.executable)
        parent_dir = os.path.dirname(exe_dir)

        if os.path.basename(exe_dir).lower() == "dist":
            return parent_dir

        if os.path.isdir(os.path.join(parent_dir, AUD_FOLDER_NAME)) and os.path.isdir(
            os.path.join(parent_dir, REVIEW_FOLDER_NAME)
        ):
            return parent_dir

        return exe_dir
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


PROJECT_ROOT_DIR = runtime_root()
AUD_DIR_PATH = os.path.join(PROJECT_ROOT_DIR, AUD_FOLDER_NAME)
REVIEW_DIR_PATH = os.path.join(PROJECT_ROOT_DIR, REVIEW_FOLDER_NAME)
SH_TARGET_DIR = PROJECT_ROOT_DIR


def copytree_if_missing(source_path, target_path):
    if os.path.exists(target_path) or not os.path.exists(source_path):
        return False
    shutil.copytree(source_path, target_path)
    return True


def ensure_runtime_folders():
    if is_frozen():
        copytree_if_missing(bundled_path("aud_seed"), AUD_DIR_PATH)
        copytree_if_missing(bundled_path("review_seed"), REVIEW_DIR_PATH)
    else:
        os.makedirs(REVIEW_DIR_PATH, exist_ok=True)


ensure_runtime_folders()
eel.init(bundled_path("web") if is_frozen() else bundled_path("frontend", "dist"))


state = {
    "generated_folder": None,
    "target_att_two_name": None,
    "target_att_three_name": None,
    "current_today_str": None,
    "actual_excel_path": None,
}


def require_generated_folder():
    if not state["generated_folder"]:
        return {"status": "error", "message": "尚未建立本週覆核資料夾，請先執行步驟 1。"}
    return None


@eel.expose
def get_runtime_info():
    return {
        "project_root": PROJECT_ROOT_DIR,
        "aud_path": AUD_DIR_PATH,
        "review_path": REVIEW_DIR_PATH,
        "aud_exists": os.path.isdir(AUD_DIR_PATH),
        "review_exists": os.path.isdir(REVIEW_DIR_PATH),
    }


@eel.expose
def run_stage_initial():
    try:
        print("=" * 60, flush=True)
        print("Step 1 - environment check", flush=True)
        print(f"Runtime root: {PROJECT_ROOT_DIR}", flush=True)
        print(f"Aud path: {AUD_DIR_PATH}", flush=True)

        ensure_runtime_folders()
        if not os.path.isdir(AUD_DIR_PATH):
            return {
                "status": "error",
                "error_type": "AUD_MISSING",
                "message": f"找不到必要資料夾 aud。請建立或放置於：{AUD_DIR_PATH}",
                "aud_path": AUD_DIR_PATH,
            }

        res_folder, att_two, att_three, today_str, _aud_warn = core_logic.backup_and_rename_by_latest_folder(
            excel_source_path=EXCEL_SOURCE
        )

        state["current_today_str"] = today_str
        state["generated_folder"] = res_folder
        state["target_att_two_name"] = att_two
        state["target_att_three_name"] = att_three
        state["actual_excel_path"] = os.path.join(res_folder, f"02.GP程式修改記錄v{today_str}.xlsx")

        return {
            "status": "success",
            "message": "環境初始化完成。",
            "folder": state["generated_folder"],
            "today_str": today_str,
            "aud_path": AUD_DIR_PATH,
        }
    except Exception as exc:
        print(f"Step 1 failed: {exc}", flush=True)
        return {"status": "error", "message": str(exc), "aud_path": AUD_DIR_PATH}


@eel.expose
def run_stage_merge_diff():
    try:
        missing = require_generated_folder()
        if missing:
            return missing

        core_logic.merge_diff_files_to_attachment(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_two_name"],
        )
        core_logic.modify_bat_scripts(SH_TARGET_DIR)
        return {"status": "success", "message": "附件二已合併，CR 批次檔已更新。"}
    except Exception as exc:
        print(f"Step 3 failed: {exc}", flush=True)
        return {"status": "error", "message": str(exc)}


@eel.expose
def run_stage_process_attachment_three():
    try:
        missing = require_generated_folder()
        if missing:
            return missing

        core_logic.merge_csv_files_to_attachment_three(
            local_dir=SH_TARGET_DIR,
            target_dir=state["generated_folder"],
            target_filename=state["target_att_three_name"],
            today_str=state["current_today_str"],
        )
        return {"status": "success", "message": "附件三已合併。"}
    except Exception as exc:
        print(f"Step 5 failed: {exc}", flush=True)
        return {"status": "error", "message": str(exc)}


@eel.expose
def run_stage_final_audit():
    try:
        missing = require_generated_folder()
        if missing:
            return missing

        if not state["actual_excel_path"] or not os.path.exists(state["actual_excel_path"]):
            return {"status": "error", "message": "找不到本機備份 Excel，無法執行比對。"}

        core_logic.audit_and_compare_logs(
            excel_path=state["actual_excel_path"],
            att_two_path=os.path.join(state["generated_folder"], state["target_att_two_name"]),
            att_three_path=os.path.join(state["generated_folder"], state["target_att_three_name"]),
            output_log_dir=AUD_DIR_PATH,
            today_str=state["current_today_str"],
        )

        report_path = os.path.join(AUD_DIR_PATH, f"{state['current_today_str']}_稽核比對結果報告.txt")
        return {
            "status": "success",
            "message": "稽核比對完成。",
            "report_path": report_path,
            "folder": state["generated_folder"],
            "today_str": state["current_today_str"],
        }
    except Exception as exc:
        print(f"Step 6 failed: {exc}", flush=True)
        return {"status": "error", "message": str(exc)}


@eel.expose
def run_stage_deploy_network():
    try:
        missing = require_generated_folder()
        if missing:
            return missing

        core_logic.deploy_local_folder_to_network_share(state["generated_folder"], REMOTE_NETWORK_BASE_DIR)
        return {"status": "success", "message": "已同步至 DataCenter。"}
    except Exception as exc:
        print(f"Deploy failed: {exc}", flush=True)
        return {"status": "error", "message": str(exc)}


if __name__ == "__main__":
    try:
        eel.start("index.html", mode="edge", size=(1280, 800))
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
