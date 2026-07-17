# Project Context

## Purpose
TIPTOP GP 程式覆核自動化系統協助 MIS 同仁完成每週程式修改查核、附件整併、Excel 紅字紀錄比對，以及 DataCenter 成果同步。

## Stack
- Frontend: React, Vite, Ant Design, Lucide React
- Backend: Python 3.13, Eel, openpyxl
- Packaging: PyInstaller with `frontend/dist` bundled as Eel web assets

## Conventions
- UI keeps the current step-by-step audit workflow visible at all times.
- Manual checkpoints must remain explicit before TipTop shell execution, CR host batch execution, final report review, and DataCenter deployment.
- Backend file operations must preserve Chinese filenames and Windows network-share paths.
- New frontend quality checks should be repeatable from CLI scripts without adding noise to the operator workflow.
- High-risk production network-copy behavior should be tested around pure logic first, then manually verified on a controlled environment.

## Commands
- Frontend verify: `cd frontend && npm run verify`
- Backend tests: `cd backend && python -m unittest discover -s tests -v`
- Frontend build for Eel package: `cd frontend && npm run build`
- Development launch: `cd backend && python app.py`
