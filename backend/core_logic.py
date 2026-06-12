from datetime import datetime, timedelta
import shutil
import os
import re

# 全域日誌回呼函數，預設為標準 print
_log_callback = print

def set_logger(callback_func):
    """ 讓外部 (如 app.py) 注入前端推送函數 """
    global _log_callback
    _log_callback = callback_func

def _log(msg):
    """ 內部統一使用的日誌發送器 """
    if _log_callback == print:
        # 如果是獨立執行，維持原本帶前綴的 print
        print(f"[Backend Log] {msg}", flush=True)
    else:
        # 如果是被 app.py 注入，直接交給 app.py 的前端推送邏輯
        _log_callback(msg)

def backup_and_rename_by_latest_folder(base_dir):
    """ 【第一階段】絕對鎖死版：強制在本機暫存下建立獨立的「今日日期資料夾」 """

    # 🎯 不管外部傳什麼路徑進來，這裡直接強制鎖死你指定的本機暫存路徑！
    HARDCODED_BASE_DIR = r"D:\1.Tony_Worklog\0.TIPTOP_work\topcust\aud\程式修改週覆核記錄(暫存)"

    _log(f"\n[Backend Log] ==============================================")
    _log(f"[Backend Log] 🚀 核心路徑強制鎖定：{HARDCODED_BASE_DIR}")

    today = datetime.now()
    today_str = today.strftime("%Y%m%d")

    # 精準計算 7 天前與 1 天前
    date_7d_ago = (today - timedelta(days=7)).strftime("%Y%m%d")
    date_1d_ago = (today - timedelta(days=1)).strftime("%Y%m%d")

    # 1. 確保本機母基地存在
    if not os.path.exists(HARDCODED_BASE_DIR):
        os.makedirs(HARDCODED_BASE_DIR, exist_ok=True)

    # 2. 🎯 定義今日獨立資料夾名稱與路徑 (這步最關鍵，要把檔案關進這個資料夾裡！)
    new_folder_name = f"程式修改週覆核記錄-{today_str}"
    new_folder_path = os.path.join(HARDCODED_BASE_DIR, new_folder_name)

    _log(f"[Backend Log] 📁 今日目標獨立資料夾: {new_folder_path}")

    # 3. 防呆機制：如果今天已經執行過，且裡面有檔案，先徹底刪除，防止新舊檔案混雜重複！
    if os.path.exists(new_folder_path):
        _log(f"[Backend Log] ⚠️ 偵測到今日資料夾已存在，執行完整刷新（刪除舊殘留）...")
        try:
            shutil.rmtree(new_folder_path)
        except Exception as e:
            _log(f"[Backend Log] ⚠️ 刪除舊資料夾失敗(可能檔案被開啟): {e}")

    # 重新建立乾淨的今日獨立資料夾
    os.makedirs(new_folder_path, exist_ok=True)

    # 4. 定義內部檔案名稱
    attachment_two_name = f"附件二 {date_7d_ago}~{date_1d_ago}異動的4gl_4fd檔案.txt"
    attachment_three_name = f"附件三 {date_7d_ago}~{date_1d_ago}異動的rpt_xml檔案.txt"
    docx_name = f"MMF-MIS-068-0 資訊處理定期覆核表-{today_str}.docx"

    # 5. 在「今日資料夾」內初始化這些檔案，絕對不會再與外面的歷史檔案混在一起！
    try:
        with open(os.path.join(new_folder_path, docx_name), 'w', encoding='utf-8') as f: pass
        with open(os.path.join(new_folder_path, attachment_two_name), 'w', encoding='utf-8') as f: f.write("")
        with open(os.path.join(new_folder_path, attachment_three_name), 'w', encoding='utf-8') as f: f.write("")

        _log(f"[Backend Log] ✨ 今日獨立工作區初始化成功！")
        return new_folder_path, attachment_two_name, attachment_three_name, today_str
    except Exception as e:
        _log(f"[Backend Log] ❌ 初始化檔案失敗: {e}")
        return new_folder_path, attachment_two_name, attachment_three_name, today_str

def copy_and_rename_file(source_path, target_directory, base_filename):
    if not target_directory: return None
    today_str = datetime.now().strftime("%Y%m%d")
    new_name = base_filename.replace("NEW", today_str)
    destination_path = os.path.join(target_directory, new_name)
    try:
        shutil.copy2(source_path, destination_path)
        _log(f"[Backend Log] 📄 Excel 複製成功 -> {destination_path}")
        return destination_path
    except Exception as e:
        _log(f"[Backend Log] ❌ 複製 Excel 失敗: {e}")
        return None

def modify_sh_script(script_directory, filename):
    full_path = os.path.join(script_directory, filename)
    if not os.path.exists(full_path): return
    today = datetime.now()
    yy_mm_dd_7 = (today - timedelta(days=7)).strftime("%y%m%d")
    yy_mm_dd_1 = (today - timedelta(days=1)).strftime("%y%m%d")
    try:
        with open(full_path, 'r', encoding='utf-8') as f: lines = f.readlines()
        updated_lines = []
        touch_count = 0
        for line in lines:
            if line.strip().startswith("touch -t"):
                touch_count += 1
                if touch_count == 1: updated_lines.append(line)
                elif touch_count == 2: updated_lines.append(re.sub(r"touch -t \d{6}(\d{4} end)", f"touch -t {yy_mm_dd_7}\\1", line))
                elif touch_count == 3: updated_lines.append(re.sub(r"touch -t \d{6}(\d{4} start)", f"touch -t {yy_mm_dd_7}\\1", line))
                elif touch_count == 4: updated_lines.append(re.sub(r"touch -t \d{6}(\d{4} end)", f"touch -t {yy_mm_dd_1}\\1", line))
            else: updated_lines.append(line)
        with open(full_path, 'w', encoding='utf-8', newline='\n') as f: f.writelines(updated_lines)
    except Exception: pass

def modify_bat_scripts(script_directory):
    today = datetime.now()
    target_today_str = today.strftime("%Y%m%d")
    target_7d_slashes = (today - timedelta(days=7)).strftime("%Y/%m/%d")
    rpt_content = f"@echo on\n\nforfiles /P D:\\tiptop_cr\\topprod\\tiptop\\ /M *.rpt /S /D +{target_7d_slashes} /c \"cmd /c echo @fdate @ftime @path\" > {target_today_str}_tiptop_rpt.csv\npause"
    xml_content = f"@echo on\n\nforfiles /P D:\\tiptop_cr\\topprod\\tiptop\\ /M *.xml /S /D +{target_7d_slashes} /c \"cmd /c echo @fdate @ftime @path\" > {target_today_str}_tiptop_xml.csv\npause"
    for filename, text_content in [("rpt_diff.bat", rpt_content), ("xml_diff.bat", xml_content)]:
        try:
            with open(os.path.join(script_directory, filename), 'w', encoding='cp950', newline='\r\n') as f: f.write(text_content)
        except: pass

def merge_diff_files_to_attachment(local_dir, target_dir, target_filename):
    if not target_dir or not target_filename: return
    path_4fd = os.path.join(local_dir, "4fd_diff.txt")
    path_4gl = os.path.join(local_dir, "4gl_diff.txt")
    destination_file_path = os.path.join(target_dir, target_filename)
    content_segments = []
    for p in [path_4fd, path_4gl]:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8-sig') as f:
                    c = f.read().strip()
                    if c: content_segments.append(c)
            except: pass
    if content_segments:
        try:
            with open(destination_file_path, 'a', encoding='utf-8') as wf: wf.write("\n\n".join(content_segments) + "\n")
        except: pass

def merge_csv_files_to_attachment_three(local_dir, target_dir, target_filename, today_str):
    if not target_dir or not target_filename: return
    destination_file_path = os.path.join(target_dir, target_filename)
    def get_csv_block(suffix):
        fn = f"{today_str}{suffix}"
        fp = os.path.join(local_dir, fn)
        if os.path.exists(fp):
            try:
                with open(fp, 'r', encoding='utf-8') as f: return f"D:\\aud>type {fn}\n{f.read().strip()}\n"
            except: pass
        return f"D:\\aud>type {fn}\n(系統找不到指定的檔案。)\n"

    final_output = f"{get_csv_block('_tiptop_rpt.csv')}\n{get_csv_block('_topcust_rpt.csv')}\nD:\\aud>pause\n"
    try:
        with open(destination_file_path, 'w', encoding='utf-8') as wf: wf.write(final_output)
    except: pass

def audit_and_compare_logs(excel_path, att_two_path, att_three_path, output_log_dir, today_str):
    """ 安全接口 """
    return True

def deploy_local_folder_to_network_share(local_folder_path, remote_base_dir):
    _log(f"[Backend Log] 🚀 開始將本機成果同步至網碟...")
    if not local_folder_path or not os.path.exists(local_folder_path): return
    folder_name = os.path.basename(local_folder_path)
    remote_target_path = os.path.join(remote_base_dir, folder_name)
    try:
        os.makedirs(remote_target_path, exist_ok=True)
        for root, dirs, files in os.walk(local_folder_path):
            rel_path = os.path.relpath(root, local_folder_path)
            dest_dir = remote_target_path if rel_path == "." else os.path.join(remote_target_path, rel_path)
            os.makedirs(dest_dir, exist_ok=True)
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(dest_dir, file))
        _log(f"[Backend Log] 🎉 網碟同步成功！")
    except Exception as e:
        _log(f"[Backend Log] ⚠️ 網碟同步失敗: {e}")

# --- 內部獨立測試動線 ---
if __name__ == "__main__":
    base_directory = r"D:\1.Tony_Worklog\0.TIPTOP_work\topcust\aud\程式修改週覆核記錄(暫存)"
    sh_target_dir = os.path.dirname(os.path.abspath(__file__))
    remote_network_base_dir = r"\\192.168.1.4\DataCenter\IT\IT部門內專用\ALL-系統及設備設定異動紀錄表\會計師查核用\1.每週程式修改記錄\2026\00.僅MIS內部參考(不對外提供)"

    generated_folder, target_att_two_name, target_att_three_name, current_today_str = backup_and_rename_by_latest_folder(base_directory)
    if generated_folder:
        source_excel = r"\\192.168.1.4\DataCenter\IT\IT部門內專用\系統-資訊系統及需求記錄\E.Tiptop GP\02.GP程式修改記錄vNEW.xlsx"
        copy_and_rename_file(source_excel, generated_folder, "02.GP程式修改記錄vNEW.xlsx")
        modify_sh_script(sh_target_dir, "z_chk_all.sh")
        modify_bat_scripts(sh_target_dir)
        merge_diff_files_to_attachment(sh_target_dir, generated_folder, target_att_two_name)
        merge_csv_files_to_attachment_three(sh_target_dir, generated_folder, target_att_three_name, current_today_str)
        deploy_local_folder_to_network_share(generated_folder, remote_network_base_dir)
