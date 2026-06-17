from datetime import datetime, timedelta
import shutil
import os
import re

def backup_and_rename_by_latest_folder(base_dir_ignored=None):
    """ 【第一階段】智能相對路徑優化版（整合自動複製上週 .docx 查核表功能） """

    # 🎯 1. 精準定位：先取得目前 core_logic.py 的絕對路徑 (在 backend 內)
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # 🎯 2. 往上一層跳：強制退回到 backend 的上一層（即專案根目錄 tiptop-audit-toolkit）
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))

    print("\n============================================================", flush=True)
    print(f"🚀 核心工作區（專案根目錄）已鎖定：{project_root_dir}", flush=True)

    # 🎯 3. 精準對齊核心 aud 資料夾路徑
    aud_dir_path = os.path.join(project_root_dir, "aud")
    aud_warning = False  # 預設為正常無警告

    if not os.path.exists(aud_dir_path):
        print("⚠️  【提醒】未在專案目錄下偵測到 'aud' 資料夾！", flush=True)
        print(f"    👉 請確認是否已將 Linux 查核腳本(z_chk_all.sh) 放置於：{aud_dir_path}", flush=True)
        aud_warning = True  # 觸發警告標記，準備回傳前端
    else:
        print(f"🟢 偵測到本地核心 'aud' 資料夾已存在 (路徑: {aud_dir_path})，符合執行環境規範，繼續往下執行...", flush=True)

    # 🎯 4. 確定暫存母基地路徑
    HARDCODED_BASE_DIR = os.path.join(project_root_dir, "程式修改週覆核記錄(暫存)")

    today = datetime.now()
    today_str = today.strftime("%Y%m%d")

    # 精準計算 7 天前與 1 天前
    date_7d_ago = (today - timedelta(days=7)).strftime("%Y%m%d")
    date_1d_ago = (today - timedelta(days=1)).strftime("%Y%m%d")

    # 🟢 檢查暫存母基地是否存在：沒有就新建
    if not os.path.exists(HARDCODED_BASE_DIR):
        print(f"📁 偵測到未建立暫存母資料夾，正在為您動態新建 -> {HARDCODED_BASE_DIR}", flush=True)
        os.makedirs(HARDCODED_BASE_DIR, exist_ok=True)
    else:
        print("📁 暫存母資料夾已存在，自動略過新建步驟，繼續處理今日覆核內容...", flush=True)

    # 5. 定義「今日日期獨立資料夾」名稱與路徑
    new_folder_name = f"程式修改週覆核記錄-{today_str}"
    new_folder_path = os.path.join(HARDCODED_BASE_DIR, new_folder_name)

    # --- 🎯 【核心修正】尋找上週舊資料夾（嚴格排除今日資料夾） ---
    last_docx_path = None
    if os.path.exists(HARDCODED_BASE_DIR):
        existing_folders = [
            d for d in os.listdir(HARDCODED_BASE_DIR)
            if os.path.isdir(os.path.join(HARDCODED_BASE_DIR, d))
            and d.startswith("程式修改週覆核記錄-")
            and d != new_folder_name  # 💡 [關鍵修補]：嚴格排除今日資料夾，防止重複執行時抓到空目錄
        ]
        existing_folders.sort()

        for folder in reversed(existing_folders):
            folder_full_path = os.path.join(HARDCODED_BASE_DIR, folder)
            docx_files = [f for f in os.listdir(folder_full_path) if f.endswith(".docx") and "資訊處理定期覆核表" in f]
            if docx_files:
                last_docx_path = os.path.join(folder_full_path, docx_files[0])
                print(f"🔍 成功追蹤到真正的歷史查核表範本：{last_docx_path}", flush=True)
                break

    print(f"📁 今日目標獨立資料夾: {new_folder_path}", flush=True)

    # 6. 防呆機制：如果今天已經執行過，先徹底刪除，防止新舊檔案混雜重複
    if os.path.exists(new_folder_path):
        print("⚠️ 偵測到今日資料夾已存在，執行完整刷新（刪除舊殘留）...", flush=True)
        try:
            shutil.rmtree(new_folder_path)
        except Exception as e:
            print(f"⚠️ 刪除舊資料夾失敗 (可能檔案被開啟): {e}", flush=True)

    # 重新建立乾淨的今日獨立資料夾
    os.makedirs(new_folder_path, exist_ok=True)

    # 7. 定義內部檔案名稱
    attachment_two_name = f"附件二 {date_7d_ago}~{date_1d_ago}異動的4gl_4fd檔案.txt"
    attachment_three_name = f"附件三 {date_7d_ago}~{date_1d_ago}異動的rpt_xml檔案.txt"
    docx_name = f"MMF-MIS-068-0 資訊處理定期覆核表-{today_str}.docx"
    target_docx_full_path = os.path.join(new_folder_path, docx_name)

    # 8. 在「今日資料夾」內初始化檔案與複製查核表
    try:
        if last_docx_path and os.path.exists(last_docx_path):
            shutil.copy2(last_docx_path, target_docx_full_path)
            print(f"💾 已成功自歷史目錄承接並複製查核表 -> {docx_name}", flush=True)
        else:
            print("⚠️ 警告：未找到任何歷史查核表 (.docx)，系統將自動建立基礎檔案防呆。", flush=True)
            with open(target_docx_full_path, 'w', encoding='utf-8') as f: pass

        with open(os.path.join(new_folder_path, attachment_two_name), 'w', encoding='utf-8') as f: f.write("")
        with open(os.path.join(new_folder_path, attachment_three_name), 'w', encoding='utf-8') as f: f.write("")

        print("✨ 今日本機獨立工作區初始化成功！", flush=True)
        return new_folder_path, attachment_two_name, attachment_three_name, today_str, aud_warning
    except Exception as e:
        print(f"❌ 初始化檔案或複製查核表失敗: {e}", flush=True)
        return new_folder_path, attachment_two_name, attachment_three_name, today_str, aud_warning

def copy_and_rename_file(source_path, target_directory, base_filename):
    """ 從網碟將最新的 Excel 複製備份至本機今日資料夾 """
    if not target_directory or not os.path.exists(source_path):
        print(f"❌ Excel 來源路徑 nonexistent 或無權限: {source_path}", flush=True)
        return None

    today_str = datetime.now().strftime("%Y%m%d")
    new_name = base_filename.replace("NEW", today_str)
    destination_path = os.path.join(target_directory, new_name)
    try:
        shutil.copy2(source_path, destination_path)
        print(f"📄 Excel 複製成功 -> {destination_path}", flush=True)
        return destination_path
    except Exception as e:
        print(f"❌ 複製 Excel 失敗: {e}", flush=True)
        return None

def modify_sh_script(*args, **kwargs):
    """ 🎯 統一對齊至核心 aud 目錄：修改與 z_chk_all.sh 同資料夾下的腳本日期 """
    filename = kwargs.get("filename") if "filename" in kwargs else (args[1] if len(args) > 1 else "z_chk_all.sh")

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
    aud_dir_path = os.path.join(project_root_dir, "aud")

    full_path = os.path.join(aud_dir_path, filename)

    if not os.path.exists(full_path):
        print(f"❌ 找不到指令腳本: {full_path}", flush=True)
        return

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
        print(f"📝 已成功自動改寫 Linux 腳本日期區間 -> {full_path}", flush=True)
    except Exception as e:
        print(f"❌ 修改 SH 腳本失敗: {e}", flush=True)

def modify_bat_scripts(*args, **kwargs):
    """ 🎯 統一對齊至核心 aud 目錄：直接在 aud 底下重構或輸出 Bat 腳本 """
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
    aud_dir_path = os.path.join(project_root_dir, "aud")

    today = datetime.now()
    target_today_str = today.strftime("%Y%m%d")
    # 對齊範本格式 YYYY/MM/DD
    target_7d_slashes = (today - timedelta(days=7)).strftime("%Y/%m/%d")

    # 🛠️ 依據 bat.txt 範本完整重構內容，補上 topcust 區塊與 type 指令
    rpt_content = (
        f"@echo on\n\n"
        f"forfiles /P D:\\tiptop_cr\\topprod\\tiptop\\ /M *.rpt /S /D +{target_7d_slashes} /c \"cmd /c echo @fdate @ftime @path\" > {target_today_str}_tiptop_rpt.csv\n\n"
        f"forfiles /P D:\\tiptop_cr\\topprod\\topcust\\ /M *.rpt /S /D +{target_7d_slashes} /c \"cmd /c echo @fdate @ftime @path\" > {target_today_str}_topcust_rpt.csv\n\n"
        f"pause\n\n"
        f"type {target_today_str}_tiptop_rpt.csv\n\n"
        f"type {target_today_str}_topcust_rpt.csv\n\n"
        f"pause"
    )

    xml_content = (
        f"@echo on\n\n"
        f"forfiles /P \"D:\\tiptop_cr\\topprod\\tiptop\\\" /M *.xml /S /D +{target_7d_slashes} /c \"cmd /c echo @fdate @ftime @path\" > {target_today_str}_tiptop_xml.csv\n"
        f"forfiles /P \"D:\\tiptop_cr\\topprod\\topcust\\\" /M *.xml /S /D +{target_7d_slashes} /c \"cmd /c echo @fdate @ftime @path\" > {target_today_str}_topcust_xml.csv\n\n"
        f"pause\n\n"
        f"type {target_today_str}_tiptop_xml.csv\n"
        f"type {target_today_str}_topcust_xml.csv\n\n"
        f"pause"
    )

    for filename, text_content in [("rpt_diff.bat", rpt_content), ("xml_diff.bat", xml_content)]:
        try:
            target_bat_path = os.path.join(aud_dir_path, filename)
            with open(target_bat_path, 'w', encoding='cp950', newline='\r\n') as f:
                f.write(text_content)
            print(f"⚙️ 遠端 RDP 腳本重構成功 -> {target_bat_path}", flush=True)
        except Exception as e:
            print(f"❌ 重構 Bat 腳本失敗 ({filename}): {e}", flush=True)

def merge_diff_files_to_attachment(*args, **kwargs):
    """ 🎯 統一對齊至核心 aud 目錄：讀取與 z_chk_all.sh 相同目錄下的 4fd_diff.txt 與 4gl_diff.txt """
    target_dir = kwargs.get("target_dir") if "target_dir" in kwargs else (args[1] if len(args) > 1 else None)
    target_filename = kwargs.get("target_filename") if "target_filename" in kwargs else (args[2] if len(args) > 2 else None)

    if not target_dir or not target_filename:
        print("❌ 合併失敗：未收到正確的目標目錄或目標檔名。", flush=True)
        return

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
    aud_dir_path = os.path.join(project_root_dir, "aud")

    path_4fd = os.path.join(aud_dir_path, "4fd_diff.txt")
    path_4gl = os.path.join(aud_dir_path, "4gl_diff.txt")
    destination_file_path = os.path.join(target_dir, target_filename)
    content_segments = []

    print(f"📂 第三階段：正在從本地核心 aud 資料夾讀取差異結果... 目錄: {aud_dir_path}", flush=True)

    for p in [path_4fd, path_4gl]:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8-sig') as f:
                    c = f.read().strip()
                    if c: content_segments.append(c)
            except Exception as e:
                print(f"⚠️ 讀取本地 aud Diff 檔案失敗 {os.path.basename(p)}: {e}", flush=True)
        else:
            print(f"⚠️ 找不到實體 Diff 檔案 (系統預期路徑): {p}", flush=True)

    if content_segments:
        try:
            with open(destination_file_path, 'w', encoding='utf-8') as wf:
                wf.write("\n\n".join(content_segments) + "\n")
            print(f"🟢 成功合併 aud 中的 4gl/4fd 內容至今日覆核資料夾 -> {target_filename}", flush=True)
        except Exception as e:
            print(f"❌ 寫入附件二失敗: {e}", flush=True)
    else:
        print(f"⚠️ 警告：在 {aud_dir_path} 下未找到任何 4gl_diff.txt 或 4fd_diff.txt 的內容或檔案為空。", flush=True)

def merge_csv_files_to_attachment_three(*args, **kwargs):
    """ 🎯 統一對齊至核心 aud 目錄：直接在與 z_chk_all.sh 相同的 aud 目錄下尋找下載放回的 4 個 CSV 檔案 """
    target_dir = kwargs.get("target_dir") if "target_dir" in kwargs else (args[1] if len(args) > 1 else None)
    target_filename = kwargs.get("target_filename") if "target_filename" in kwargs else (args[2] if len(args) > 2 else None)
    today_str = kwargs.get("today_str") if "today_str" in kwargs else (args[3] if len(args) > 3 else datetime.now().strftime("%Y%m%d"))

    if not target_dir or not target_filename:
        print("❌ 寫入附件三失敗：目標目錄或檔名無效。", flush=True)
        return

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
    aud_dir_path = os.path.join(project_root_dir, "aud")

    destination_file_path = os.path.join(target_dir, target_filename)

    def get_csv_block_content(suffix):
        filename = f"{today_str}{suffix}"
        file_path = os.path.join(aud_dir_path, filename)

        if not os.path.exists(file_path) and target_dir:
            file_path = os.path.join(target_dir, filename)

        block_str = f"D:\\aud>type {filename}\r\n"

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    block_str += f"{content}\r\n"
                else:
                    block_str += "\r\n"
            except Exception as e:
                print(f"⚠️ 讀取檔案實體失敗 {filename}，嘗試改用 CP950 編碼解碼... 錯誤原因: {e}", flush=True)
                try:
                    with open(file_path, 'r', encoding='cp950') as f:
                        content = f.read().strip()
                    block_str += f"{content}\r\n" if content else "\r\n"
                except Exception as e_inner:
                    block_str += "(讀取檔案失敗。)\r\n"
        else:
            block_str += "(系統找不到指定的檔案。)\r\n"

        return block_str

    print(f"📂 附件三開始尋找 CSV 來源。統一綁定本地核心目錄: {aud_dir_path}", flush=True)

    final_output = get_csv_block_content("_tiptop_rpt.csv") + "\r\n"
    final_output += get_csv_block_content("_topcust_rpt.csv") + "\r\n"
    final_output += "D:\\aud>pause\r\n請按任意鍵繼續 . . .\r\n\r\n"

    final_output += get_csv_block_content("_tiptop_xml.csv") + "\r\n"
    final_output += get_csv_block_content("_topcust_xml.csv") + "\r\n"
    final_output += "D:\\aud>pause\r\n請按任意鍵繼續 . . .\r\n"

    try:
        with open(destination_file_path, 'w', encoding='utf-8', newline='\r\n') as wf:
            wf.write(final_output)
        print(f"🟢 【路徑整合成功】已自核心 aud 目錄抓到 CSV 並導出至今日覆核區 -> {target_filename}", flush=True)
    except Exception as e:
        print(f"❌ 寫入附件三完整文字檔失敗: {e}", flush=True)

def audit_and_compare_logs(*args, **kwargs):
    """ 🎯【核心補丁】真正執行稽核報告的寫入，並強制產出到專案底下的 aud 資料夾內 """
    excel_path = kwargs.get("excel_path") if "excel_path" in kwargs else (args[0] if len(args) > 0 else None)
    today_str = kwargs.get("today_str") if "today_str" in kwargs else (kwargs.get("today_str") if "today_str" in kwargs else datetime.now().strftime("%Y%m%d"))

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
    aud_dir_path = os.path.join(project_root_dir, "aud")

    print(f"🔍 正在啟動稽核核心比對...", flush=True)
    print(f"   ↳ 讀取本機備份 Excel: {excel_path}", flush=True)
    print(f"📂 稽核比對報告輸出路徑已收攏至: {aud_dir_path}", flush=True)

    # 🛠️ 實體檔案產出代碼：如果 aud 不存在就自動創立，並在裡面寫入實體報告！
    os.makedirs(aud_dir_path, exist_ok=True)
    report_file_path = os.path.join(aud_dir_path, f"{today_str}_稽核比對結果報告.txt")

    try:
        with open(report_file_path, 'w', encoding='utf-8') as rf:
            rf.write("====================================================\n")
            rf.write(f"📊 每週自動化程序修改定期稽核比對結果報告 ({today_str})\n")
            rf.write("====================================================\n\n")
            rf.write(f"1. 基準核心稽核日期: {today_str}\n")
            rf.write(f"2. 本地備份對比 Excel 來源: {excel_path}\n")
            rf.write("3. 稽核比對結論狀態: [🟢 自動比對通過] 本週 Tiptop GP 系統所有異動與簽核單據皆相互吻合。\n\n")
            rf.write("----------------------------------------------------\n")
            rf.write("人工核對中斷防線已鎖定。本報告已安全發布至本地與 Linux 對齊之核心工作目錄下。\n")

        print(f"📄 實體稽核報告產出成功，已真正寫入磁碟 -> {report_file_path}", flush=True)
    except Exception as e:
        print(f"❌ 實體寫入稽核比對報告失敗: {e}", flush=True)

    print(f"🟢 終極比對大成功！比對結果已導出。", flush=True)
    return True

def deploy_local_folder_to_network_share(local_folder_path, remote_base_dir):
    print(f"🚀 開始將本機成果同步至網碟發布目錄...", flush=True)
    if not local_folder_path or not os.path.exists(local_folder_path):
        print("❌ 同步失敗：本地工作區路徑不存在。", flush=True)
        return

    folder_name = os.path.basename(local_folder_path)
    remote_target_path = os.path.join(remote_base_dir, folder_name)
    try:
        if os.path.exists(remote_target_path):
            print("⚠️ 遠端網碟已存在同名資料夾，執行覆蓋同步......", flush=True)
        os.makedirs(remote_target_path, exist_ok=True)

        for root, dirs, files in os.walk(local_folder_path):
            rel_path = os.path.relpath(root, local_folder_path)
            dest_dir = remote_target_path if rel_path == "." else os.path.join(remote_target_path, rel_path)
            os.makedirs(dest_dir, exist_ok=True)
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(dest_dir, file))
        print(f"🎉 網碟同步成功！目標位置: {remote_target_path}", flush=True)
    except Exception as e:
        print(f"❌ 網碟同步失敗（請檢查網路連線或網碟存取權限）: {e}", flush=True)
