下面是三段可以直接喂给本地 AI 的 prompt，每段都指定了使用的问题列、过滤逻辑、可视化规范和输出工具。先说一下三张图的优先级：

- **图 1（Q24 容忍度雷达）**：必做，论文 F5 的视觉锚点
- **图 2（Q26 动机雷达）**：推荐做，强化 F4 的角色差异
- **图 3（Q30 严重度三联雷达）**：可选，仅当你打算扩写 §4.1 时才做

CSV 文件名沿用项目里的 `Cornell_Carpool_System_Survey_April_21_2026_22_55.csv`。所有 prompt 都假设使用 **Python + pandas + matplotlib**，输出 PDF（vector format，LaTeX 友好）。

---

## Prompt 1 — Q24 Driver Tolerance 雷达图（最高优先级）

````
任务：生成一张雷达图（radar chart），可视化论文 §4.2 中报告的 Driver/Both subset (N=19) vs Rider-only control (N=11–12) 在四类乘客摩擦上的容忍度差异。这张图是 Table 2 的视觉化版本，用于揭示 unfair rating 维度的不对称收缩。

输入文件：
- /path/to/Cornell_Carpool_System_Survey_April_21_2026_22_55.csv
- 注意：Qualtrics 导出格式有三行 header（variable name / question text / JSON metadata），加载时使用 pandas.read_csv(..., header=0, skiprows=[1, 2]) 跳过非数据行
- 加载后排除 Status == "Survey Preview" 的预览行

使用的列：
- Q3：Travel Role（取值含 "Rider" / "Driver" / "Both" 等文字标签；如果是数字编码请先 print 头几行确认）
- Q24_1：容忍度——Passenger is 10 minutes late
- Q24_2：容忍度——Last-minute destination change
- Q24_3：容忍度——Unfair / misunderstanding ratings
- Q24_4：容忍度——Non-standard route requests
- 所有 Q24_x 是 0–100 数值滑动条，越高表示越容忍

数据处理：
1. 把 Q24_1 到 Q24_4 强制转 numeric（pd.to_numeric, errors="coerce"）
2. 构造两个 subset：
   - Driver/Both subset：Q3 ∈ {"Driver", "Both"}，并且四个 Q24 项都非空（dropna across Q24_1..Q24_4 with how="any"）。预期 N=19
   - Rider-only subset：Q3 == "Rider"，并且至少一个 Q24 项非空。预期 N=11–12（每项 N 单独报告）
3. 计算每个 subset 在四个轴上的 mean，per-axis N 单独记录
4. 验证数字：Driver/Both 的 Q24_3 应在 29 附近，Q24_4 在 52 附近；Rider-only 的 Q24_2 应在 19 附近。如果偏离超过 5 分，停下来 print 整个 subset 让我检查 Q3 的取值标签

雷达图规范（务必满足）：
- 4 个轴顺序（顺时针，从顶端开始）：
  顶端：Unfair rating (Q24_3)
  右：Late arrival (Q24_1)
  下：Non-standard route (Q24_4)
  左：Destination change (Q24_2)
  注：把 Unfair rating 放在顶端，让"内缩"成为视觉焦点
- 两层叠加：Driver/Both（实线 + 半透明填充 alpha=0.25）vs Rider-only（虚线 + 半透明填充 alpha=0.15）
- 颜色：Driver/Both 用 #C0392B（暖红），Rider-only 用 #2980B9（冷蓝）。两色在灰度打印下也可区分
- 半径范围 0–60，每 15 一格刻度（0, 15, 30, 45, 60）
- 轴标签使用两行换行，例：
  "Unfair rating\n(Q24_3)"
  避免长标签贴边
- 字体：sans-serif（Helvetica / Arial / DejaVu Sans 任一），轴标签 11pt，刻度 9pt
- 图例位置：图外右侧（bbox_to_anchor=(1.25, 1.0)），格式 "Driver/Both (N=19)" 和 "Rider-only (N=11–12)"
- 标题省略（论文 caption 会说明）；如果必须有，用 "Driver Tolerance for Passenger-Generated Friction"
- figsize=(8, 8)，DPI=300

输出：
- 矢量 PDF：q24_tolerance_radar.pdf
- 同时输出 PNG 预览版：q24_tolerance_radar.png（仅用于眼检）
- 在终端 print 一份数据表（subset × axis × N × mean），方便我交叉对比论文 Table 2

工具：Python 3，依赖 pandas、numpy、matplotlib。matplotlib 雷达图使用 polar projection（subplot_kw={"projection": "polar"}），第一个角度等于最后一个角度形成闭合多边形。
````

---

## Prompt 2 — Q26 Motivation 雷达图

````
任务：生成一张雷达图，可视化论文 §4.1 F4 中报告的四类拼车动机得分，并按 travel role 分组（Driver/Both subset vs Rider-only），用于展示司机在 Splitting fuel costs 和 Platform rewards 两项上的明显抬升。

输入文件：
- /path/to/Cornell_Carpool_System_Survey_April_21_2026_22_55.csv
- 加载时跳过 Qualtrics 的两行非数据 header：pandas.read_csv(..., header=0, skiprows=[1, 2])
- 排除 Status == "Survey Preview" 行

使用的列：
- Q3：Travel Role
- Q26_1：Social network expansion 动机
- Q26_2：Splitting fuel costs 动机
- Q26_3：Platform rewards / Earning points 动机
- Q26_4：Environmental impact 动机
- 注意：Q26_1 到 Q26_4 与轴标签的具体对应需要先 print 一下原始 question text（来自 CSV 第二行）确认。如果发现顺序与上述不一致，按 question text 的语义对应回正确的轴。所有 Q26_x 都是 0–100 滑动条

数据处理：
1. Q26_1 到 Q26_4 转 numeric
2. 两个 subset（与 Prompt 1 保持一致）：
   - Driver/Both：Q3 ∈ {"Driver", "Both"}，每个轴 dropna 后单独报 N
   - Rider-only：Q3 == "Rider"，同上
3. 每个 subset 计算 4 个轴上的 mean 和 per-axis N
4. 全样本（不分组）的 means 应该接近：fuel costs ≈ 63.6 (N=31)，platform rewards ≈ 48.3 (N=24)，social ≈ 45.6 (N=26)，environmental ≈ 44.5 (N=24)。如果偏离超过 3 分，停下来 print 整个数据让我检查

雷达图规范：
- 4 个轴顺序（顺时针，从顶端开始）：
  顶端：Splitting fuel costs
  右：Platform rewards (Points)
  下：Social expansion
  左：Environmental impact
  注：把得分最高的两项（fuel + rewards）放在视觉显眼位置
- 两层叠加：Driver/Both（实线 + alpha=0.25 填充）vs Rider-only（虚线 + alpha=0.15 填充）
- 颜色：Driver/Both 用 #C0392B，Rider-only 用 #2980B9（与 Prompt 1 保持一致以便论文风格统一）
- 半径范围 0–80，每 20 一格刻度
- 轴标签 11pt 两行换行，例：
  "Splitting\nfuel costs"
  "Platform rewards\n(Points)"
- 图例位置：图外右侧，标签格式 "Driver/Both (N=...)" 和 "Rider-only (N=...)"，N 用 per-subset 最小的 axis N（取保守值）
- 字体：sans-serif；figsize=(8, 8)；DPI=300

输出：
- q26_motivation_radar.pdf（矢量）
- q26_motivation_radar.png（预览）
- 终端 print：subset × axis × N × mean 表格

工具：Python 3，pandas + numpy + matplotlib polar projection。
````

---

## Prompt 3 — Q30 Severity 三联雷达图（可选）

````
任务：生成一组三面板雷达图（subplot 横排），展示三种距离场景（Within Ithaca / Short Trips 1–3 hrs / Long-Distance 3+ hrs）下八类交通痛点的严重度，按 travel role 分组（Driver/Both vs Rider-only）。这张图用于扩展论文 §4.1 F1，展示痛点结构的距离依赖。

输入文件：
- /path/to/Cornell_Carpool_System_Survey_April_21_2026_22_55.csv
- 加载时 skiprows=[1, 2]，排除 Status == "Survey Preview"

使用的列：
- Q3：Travel Role
- Q30_X_Y 共 24 列，X ∈ {1..8} 是痛点维度，Y ∈ {1..3} 是距离场景
- 八类痛点（按 X 编号）：
  Q30_1_*：Inflexible schedule
  Q30_2_*：Bus delays
  Q30_3_*：Expensive parking fee
  Q30_4_*：Weather disruptions
  Q30_5_*：Limited coverage
  Q30_6_*：Luggage restrictions
  Q30_7_*：Safety hazards
  Q30_8_*：Inconsistent operating hours
- 三种距离（按 Y 编号）：
  *_*_1：Within Ithaca
  *_*_2：Short Trips (1–3 hrs)
  *_*_3：Long-Distance (3+ hrs)
- 注意：上述 X 和 Y 的语义对应需要先 print 第二行的 question text 确认。如果与上述不一致，按 question text 重新映射
- Q30 是 likert 整数评分（约 1–7 量级，请先 print min/max 确认）

数据处理：
1. 全部 Q30_X_Y 列转 numeric
2. 两个 subset（与前两张图保持一致）：Driver/Both，Rider-only
3. 对每个 (subset, distance scenario) 组合，计算 8 个痛点维度的 mean，per-axis N 单独记录
4. 共得到 6 个数据系列（2 subsets × 3 distance scenarios），分别绘制在三个面板里

雷达图规范：
- 三个面板横排，每个面板 8 个轴（八类痛点），共享同一个半径范围（用三个面板里全局 max + 一格 buffer 决定）
- 每个面板内：Driver/Both 实线（#C0392B）+ alpha=0.25 填充；Rider-only 虚线（#2980B9）+ alpha=0.15 填充
- 8 个轴的标签务必横向能容下，建议两行换行：
  "Inflexible\nschedule"、"Bus\ndelays"、"Expensive\nparking fee"、"Weather\ndisruptions"、"Limited\ncoverage"、"Luggage\nrestrictions"、"Safety\nhazards"、"Inconsistent\noperating hours"
- 三个面板各自设标题："Within Ithaca"、"Short Trips (1–3 hrs)"、"Long-Distance (3+ hrs)"，标题字号 12pt
- 共享一个图例放在整图最右侧（fig.legend, bbox_to_anchor=(0.98, 0.5)），不要每个面板各自重复图例
- 字体 sans-serif；图例标签 "Driver/Both (N=...)" 和 "Rider-only (N=...)"
- figsize=(18, 7)，DPI=300
- subplots_adjust 留出足够 padding 让所有轴标签不被裁切（建议 left=0.04, right=0.86, top=0.88, bottom=0.05, wspace=0.45）

输出：
- q30_severity_by_distance.pdf（矢量）
- q30_severity_by_distance.png（预览）
- 终端 print：subset × distance × axis × N × mean 表格（24 行）

工具：Python 3，pandas + numpy + matplotlib，使用 plt.subplots(1, 3, subplot_kw={"projection": "polar"}, figsize=(18, 7))。
````

---

## 使用建议

跑完之后请眼检三个事情：
- **数字校对**：Prompt 1 出来的 Driver/Both Q24_3 mean 必须等于 29.1（论文 Table 2 的数）；Q26 全样本 fuel costs mean 必须接近 63.6。如果对不上，说明 Q3 的取值标签可能不是字符串而是数字编码，需要让本地 AI 先 print Q3.unique() 检查
- **轴标签不重叠**：Q30 那张八轴图最容易出 occlusion，如果发现挤压，在 prompt 里加一句"将每个轴标签的 labelpad 增加到 18，必要时使用 ax.set_xticks 和 ax.set_xticklabels 手动控制"
- **subset 合并的合法性**：Driver/Both 合并是论文 §4.2 已经做的方法学决定，但放进 §4.1 的 Q26 motivation 图前最好回头看一眼 §4.1 的写作——目前 §4.1 在 F4 段落里没显式引入 Driver/Both subset 概念，可能需要在那里加半句话承接

跑出来 PDF 后直接 `\includegraphics` 进 LaTeX，建议宽度设 `\linewidth`（单图）和 `\textwidth`（三联图）。