# 當前進行中的任務

**更新時間**: 2025-11-14 (by Claude)
**當前Phase**: Phase 1 - 資料收集

---

## 🔴 進行中 (In Progress)

### Task-000: 建立專案管理系統與資料夾重整
- **任務ID**: SETUP-001
- **優先級**: P0 (緊急)
- **負責**: Claude (session: review-folder-structure-01WxdNHeSuY7JZVUCZZM6hdk)
- **開始時間**: 2025-11-14
- **預計完成**: 2025-11-14 (今天)
- **預計時間**: 3小時
- **已用時間**: 1.5小時

**說明**:
建立project_management/任務追蹤系統，為Phase 1-5建立完整資料夾架構，設計人類與多AI協作的工作流程。

**前置任務**: 無

**檢查清單**:
- [x] 建立project_management/資料夾結構
- [x] 創建CURRENT_STATUS.md（當前狀態摘要）
- [x] 創建ACTIVE_TASKS.md（本文件）
- [ ] 創建PROGRESS_TRACKER.md（進度儀表板）
- [ ] 建立data/, code/, results/, figures/, tables/等Phase 1-5資料夾
- [ ] 創建.gitignore檔案
- [ ] 建立project_management/README.md（系統說明）
- [ ] 創建工作階段紀錄並更新索引
- [ ] Git commit所有變更

---

## 🟡 待開始 (Ready to Start)

### Task-001: 下載台灣工業生產指數（IPI）
- **任務ID**: DATA-1.1.1
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 2小時
- **階段**: Milestone 1.1.1

**說明**:
從DGBAS（主計總處）下載台灣工業生產指數、製造業生產指數、出口訂單月度資料（1990-2025）。

**前置任務**: Task-000 (需要data/資料夾)

**資料來源**:
- 網站: https://statdb.dgbas.gov.tw
- 資料庫: 國民所得及經濟成長 → 工業生產指數

**檢查清單**:
- [ ] 訪問DGBAS統計資料庫
- [ ] 下載工業生產指數（月度，2020=100）
- [ ] 下載製造業生產指數
- [ ] 下載出口訂單指數
- [ ] 儲存原始資料至data/raw/taiwan_macro/
- [ ] 記錄資料來源URL和下載日期
- [ ] 初步檢查資料完整性（缺失值、時間範圍）
- [ ] 更新data/README.md

**輸出檔案**:
- `data/raw/taiwan_macro/ipi_raw.csv`
- `data/raw/taiwan_macro/manufacturing_production_raw.csv`
- `data/raw/taiwan_macro/export_orders_raw.csv`

---

### Task-002: 下載台灣CPI、WPI物價資料
- **任務ID**: DATA-1.1.6
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 1.5小時
- **階段**: Milestone 1.1.6

**說明**:
從DGBAS下載CPI（消費者物價指數）、Core CPI（核心CPI）、WPI（躉售物價指數）月度資料。

**前置任務**: Task-000

**檢查清單**:
- [ ] 下載CPI總指數（2021=100）
- [ ] 下載核心CPI（不含蔬果、能源）
- [ ] 下載WPI（2021=100）
- [ ] 儲存至data/raw/taiwan_macro/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/taiwan_macro/cpi_raw.csv`
- `data/raw/taiwan_macro/core_cpi_raw.csv`
- `data/raw/taiwan_macro/wpi_raw.csv`

---

### Task-003: 下載台灣失業率與就業資料
- **任務ID**: DATA-1.1.8
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 1小時
- **階段**: Milestone 1.1.8

**說明**:
從DGBAS下載失業率（經季節調整）、就業人數月度資料。

**前置任務**: Task-000

**檢查清單**:
- [ ] 下載失業率（經季節調整）
- [ ] 下載就業人數（千人）
- [ ] 儲存至data/raw/taiwan_macro/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/taiwan_macro/unemployment_rate_raw.csv`
- `data/raw/taiwan_macro/employment_raw.csv`

---

### Task-004: 下載美國聯邦基金利率（FFR）
- **任務ID**: DATA-1.4.1
- **優先級**: P1 (高) - **建議最先執行（最簡單）**
- **負責**: 待分配
- **預計時間**: 30分鐘
- **階段**: Milestone 1.4.1

**說明**:
從FRED下載美國聯邦基金利率（Federal Funds Rate）月度資料。這是最簡單的資料下載任務，建議作為練習。

**前置任務**: Task-000

**資料來源**:
- 網站: https://fred.stlouisfed.org
- Series ID: FEDFUNDS
- 頻率: Monthly
- 時間範圍: 1990-01 to 2025-10

**檢查清單**:
- [ ] 訪問FRED網站
- [ ] 搜尋FEDFUNDS系列
- [ ] 下載CSV格式（1990-2025）
- [ ] 儲存至data/raw/us/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/us/fedfunds_raw.csv`

**備註**: 此任務最簡單，可作為熟悉FRED資料下載流程的練習。

---

### Task-005: 下載美國工業生產指數（US IPI）
- **任務ID**: DATA-1.4.2
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 30分鐘
- **階段**: Milestone 1.4.2

**說明**:
從FRED下載美國工業生產指數月度資料。

**前置任務**: Task-000

**資料來源**:
- Series ID: INDPRO
- 頻率: Monthly

**檢查清單**:
- [ ] 下載FRED INDPRO系列
- [ ] 儲存至data/raw/us/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/us/indpro_raw.csv`

---

### Task-006: 聯繫DHK (2025)作者索取程式碼
- **任務ID**: CODE-2.1.1
- **優先級**: P2 (中) - **可提前開始**
- **負責**: 待分配（需人類執行）
- **預計時間**: 1小時（撰寫email + 等待回覆）
- **階段**: Milestone 2.1.1

**說明**:
聯繫Davidson, Hou, Koop (2025)作者，請求提供OI-SVMVAR的MATLAB/R/Python程式碼。這個任務可以提前開始，因為等待回覆可能需要數週。

**前置任務**: 無（可立即開始）

**作者聯絡資訊**:
- James B. Davidson (Cardiff University)
- Chen Hou (University of Edinburgh)
- Gary Koop (University of Strathclyde)
- 期刊: Journal of Business & Economic Statistics
- 年份: 2025

**檢查清單**:
- [ ] 在Journal of Business & Economic Statistics網站查找補充材料
- [ ] 如無程式碼，撰寫禮貌的email請求
- [ ] Email應包含:
  - [ ] 簡短自我介紹
  - [ ] 研究目的（Taiwan應用）
  - [ ] 請求程式碼
  - [ ] 願意引用致謝
- [ ] 記錄email發送日期
- [ ] 追蹤回覆狀態

**備註**: 此任務需要人類執行，但可以請AI協助撰寫email草稿。

---

## 🟢 已完成 (Completed) - 最近10項

1. ✅ **DOC-015**: 修訂research_proposal.tex動機段落 (2025-11-14)
   - **重要性**: Phase 0關鍵產出，確保提案與正確研究方向對齊
   - **執行**: 依據INSTRUCTIONS_FOR_AI_literature_integration.md完整執行
   - **成果**:
     - 4段落完全重寫（~1,600字）
     - 研究問題重新定位："Which transmission channel?" vs. "Which uncertainty?"
     - 整合40+篇文獻證據（global + Taiwan）
     - 明確區隔DHK (2025)差異（novel application）
     - 新增2篇關鍵引用：Brianti (2025), Banbura et al. (2010)
   - **自檢**: 通過所有9項質量檢查標準
   - **Git**: Committed & pushed to claude/review-literature-integration-instructions-01LRNFzNDc4P9pDgmAUQ3eri

2. ✅ **PHASE0-FINAL**: Phase 0所有任務 (2025-11-14)
   - 全球文獻回顧（40+篇論文）
   - 台灣文獻回顧（10+篇論文）
   - 研究方向確定與方法論決策
   - 里程碑規劃文件建立

3. ✅ **DOC-014**: 創建AI協作指引（INSTRUCTIONS_FOR_AI_literature_integration.md）(2025-11-14)

4. ✅ **DOC-013**: 完成研究方向與里程碑文件（2025-11-14_research_direction_and_milestones.md）(2025-11-14)

5. ✅ **DOC-012**: 更新CLAUDE.md（Phase 0完成）(2025-11-14)

6. ✅ **DOC-011**: 更新README.md（Phase 0完成）(2025-11-14)

7. ✅ **LIT-002**: 完成台灣特定文獻回顧（taiwan_specific_uncertainty_literature.md）(2025-11-14)

8. ✅ **LIT-001**: 完成全球不確定性衝擊文獻回顧（uncertainty_shock_literature.md）(2025-11-14)

9. ✅ **DEC-001**: 核心方法論決策（不延伸DHK模型）(2025-11-08)

10. ✅ **DEC-002**: 變數分類策略確認（外部變數→unclassified）(2025-11-08)

---

## ⏸️ 暫停 (On Hold)

### 無

---

## ❌ 已取消 (Cancelled)

### 無

---

## 📊 任務統計

- **進行中**: 1 task
- **待開始**: 6 tasks
- **已完成**: 11 tasks (Phase 0)
- **暫停**: 0 tasks
- **已取消**: 0 tasks

**Phase 0完成度**: 100% ✅ (包含research_proposal.tex動機段落修訂)

---

## 🔔 提醒事項

### 給AI協作者
1. **開始新任務前**: 先閱讀[CURRENT_STATUS.md](../CURRENT_STATUS.md)
2. **完成任務後**: 立即更新本文件，將任務狀態改為"已完成"
3. **遇到問題**: 將任務狀態改為"暫停"，並在CURRENT_STATUS.md記錄阻礙
4. **每次工作**: 結束後建立工作階段紀錄（sessions/資料夾）

### 給人類協作者
1. **Task-006（聯繫DHK作者）**: 需要人類執行，可請AI協助撰寫email
2. **資料下載**: 大部分任務AI可執行，但需要檢查資料品質
3. **任務分配**: 可在"負責"欄位填寫負責人名稱

---

## 📋 任務ID命名規則

- **SETUP-XXX**: 專案設定與系統建立
- **DOC-XXX**: 文件撰寫與更新
- **DATA-X.X.X**: 資料收集（對應Milestone編號）
- **CODE-X.X.X**: 程式碼開發
- **ANAL-X.X.X**: 分析任務
- **LIT-XXX**: 文獻回顧
- **DEC-XXX**: 決策紀錄
- **PHASEXX-XXX**: 階段性總結任務

---

**更新紀錄**:
- 2025-11-14: 初始建立，加入Phase 0完成任務與Phase 1初始任務
