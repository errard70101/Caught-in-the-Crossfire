# 專案當前狀態

**最後更新**: 2025-11-14 by Claude (session: review-folder-structure-01WxdNHeSuY7JZVUCZZM6hdk)
**當前階段**: Phase 1 - 資料收集（0% 完成）
**專案總體進度**: 15%

---

## ⚡ 現在正在做什麼

**🔧 資料夾結構重整與任務管理系統建立**
- 建立project_management/任務追蹤系統
- 為Phase 1-5建立完整資料夾架構
- 設計人類與多AI協作的工作流程

---

## 🎯 下一步行動（優先順序）

### 今天必須完成
1. **[P0]** 完成資料夾重整與任務管理系統建立
2. **[P0]** 建立資料收集所需的data/資料夾結構
3. **[P0]** 創建.gitignore檔案（排除大型資料檔）

### 本週應開始
4. **[P1]** 下載台灣總體經濟變數（Milestone 1.1）
   - 從DGBAS下載IPI, CPI, 失業率等
5. **[P1]** 下載美國變數從FRED（Milestone 1.4）
   - FFR, IPI, BAA-AAA spread, EPU
6. **[P2]** 聯繫DHK (2025)作者索取程式碼（Milestone 2.1）

---

## 🚧 當前阻礙

**無阻礙** - 專案進展順利

---

## 📊 Phase進度摘要

| Phase | 狀態 | 完成率 | 預計完成日 | 備註 |
|-------|------|--------|-----------|------|
| Phase 0: 文獻與設計 | ✅ 完成 | 100% | 2025-11-14 | 已完成 |
| Phase 1: 資料收集 | 🔄 進行中 | 0% | 2026-02-28 | 今天啟動 |
| Phase 2: 模型實作 | ⏳ 計畫中 | 0% | 2026-05-31 | 需先完成Phase 1 |
| Phase 3: 分析 | ⏳ 計畫中 | 0% | 2026-09-30 | 三步驟研究設計 |
| Phase 4: 政策意涵 | ⏳ 計畫中 | 0% | 2027-01-31 | CBC政策簡報 |
| Phase 5: 寫作與發表 | ⏳ 計畫中 | 0% | 2027-05-31 | 期刊投稿 |

---

## 📝 最近完成的任務（最近10項）

1. ✅ 2025-11-14: 建立project_management/任務追蹤系統
2. ✅ 2025-11-14: 創建CURRENT_STATUS.md（本文件）
3. ✅ 2025-11-14: 完成資料夾重整規劃
4. ✅ 2025-11-14: 完成AI協作指引文件（INSTRUCTIONS_FOR_AI_literature_integration.md）
5. ✅ 2025-11-14: 整合文獻回顧到專案文件
6. ✅ 2025-11-14: 建立詳細研究方向與里程碑文件
7. ✅ 2025-11-14: 更新CLAUDE.md和README.md
8. ✅ 2025-11-08: 完成核心方法論決策（不延伸DHK模型）
9. ✅ 2025-11-08: 確認變數分類策略（外部變數放unclassified）
10. ✅ 2025-11-08: 完成全球不確定性衝擊文獻回顧（40+篇論文）

---

## 🔗 快速連結

### 任務管理
- [當前任務清單](todos/ACTIVE_TASKS.md)
- [Phase 1 詳細TODO](todos/phase1_data_collection.md)
- [進度追蹤儀表板](progress/PROGRESS_TRACKER.md)
- [里程碑達成紀錄](progress/milestones_achieved.md)

### 研究設計
- [研究方向與里程碑](../llm_logs/2025-11-14_research_direction_and_milestones.md)
- [核心方法論決策](decisions/2025-11-08_methodology_decisions.md)
- [專案總體說明](../docs/README.md)
- [AI協作指引](../docs/CLAUDE.md)

### 文獻回顧
- [全球不確定性衝擊文獻](../literature/uncertainty_shock_literature.md)
- [台灣特定文獻](../literature/taiwan_specific_uncertainty_literature.md)

### AI協作
- [工作階段紀錄索引](sessions/session_index.md)
- [決策紀錄索引](decisions/decision_log.md)

---

## 💡 給AI協作者的關鍵提醒

### 開始新任務前必讀
1. **本文件（CURRENT_STATUS.md）** - 了解當前狀態
2. **[ACTIVE_TASKS.md](todos/ACTIVE_TASKS.md)** - 查看可執行的任務
3. **[核心方法論決策](../llm_logs/2025-11-08_discussion.md)** - 理解研究方向

### 核心研究問題（勿搞錯）
❌ **錯誤**: "Which uncertainty (macro vs. financial) dominates Taiwan?"
✅ **正確**: "Which transmission channel (macro vs. financial) do external U.S.-China shocks use to impact Taiwan?"

### 關鍵決策（勿違反）
- ❌ 不延伸模型（不增加第三個不確定性因子）
- ❌ 不施加區塊外生性限制
- ✅ 維持DHK (2025)的2因子結構
- ✅ 外部變數全部放入"unclassified"類別

### 工作紀錄規範
- 完成任務後立即更新ACTIVE_TASKS.md
- 每次工作階段結束後建立session紀錄
- 重大決策必須記錄在decisions/資料夾

---

## 📞 聯絡資訊

### 人類研究者
- **負責人**: [待填寫]
- **聯絡方式**: [待填寫]

### 外部聯絡
- **DHK作者**: 需索取程式碼（Milestone 2.1）
- **DGBAS**: 台灣資料來源
- **CBC**: 央行資料來源

---

## 📅 重要日期

| 日期 | 事件 | 狀態 |
|------|------|------|
| 2025-11-08 | 專案啟動 | ✅ 完成 |
| 2025-11-14 | Phase 0完成 | ✅ 完成 |
| 2025-11-14 | **今天** - 任務管理系統建立 | 🔄 進行中 |
| 2025-12-31 | [目標] Milestone 1.1-1.3完成 | ⏳ 待開始 |
| 2026-02-28 | [目標] Phase 1完成 | ⏳ 待開始 |
| 2026-05-31 | [目標] Phase 2完成 | ⏳ 待開始 |
| 2027-05-31 | [目標] 論文投稿 | ⏳ 待開始 |

---

**📌 提醒**: 此文件應該是所有人類與AI協作者**第一個閱讀**的文件！
