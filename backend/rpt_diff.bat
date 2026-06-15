@echo on

forfiles /P "D:\tiptop_cr\topprod\tiptop\" /M *.rpt /S /D +2026/06/08 /c "cmd /c echo @fdate @ftime @path" > 20260615_tiptop_rpt.csv
pause