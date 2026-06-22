# PTE 模考错题与详解 · 整理卷 —— 项目说明 & 新会话上手指南

> 这份文档是**给下一次会话(新的 Claude Code / 新接手的人)看的**。
> 拿到这个仓库后，先从头读一遍这一篇，就知道：这是在干什么、装什么、看哪里、怎么继续。
>
> 👉 **要动手做新一套(新考试、新截图、新成绩图)，看 [`制作流程.md`](制作流程.md)** —— 从读图到出版本的详细分步流程。本篇偏总览与规则。

---

## 0. 仓库地址

```
<在此粘贴 GitHub 仓库网址 —— 下次替换这里>
```

克隆：

```bash
git clone <在此粘贴 GitHub 仓库网址>
cd pte-001-0621
```

---

## 1. 这个项目在干什么

把 **APEUni / 猩际 PTE 模考**的"详解"截图（原始 PDF 不可复制、只能截图）**逐题人工誊写、重新排版**，做成干净、可读、可打印的 **错题整理卷 PDF**。

- 当前这套是 **PTE Core 模考 1B**（总分 40：听力 33 / 阅读 42 / 口语 29 / 写作 57）。
- 每个版面完整保留每题的：**题干 / 原文、范文、你的作答、逐项评分、彩色批改、AI 中文建议**。
- 错误按平台标注用颜色还原；平台**漏标**的错误用橙色"补"标记额外补上。
- 成品强调"忠于原图"：内容均为人工对照誊录，若与原图有出入以原图为准。

---

## 2. 怎么"看"成品（最快路径）

1. 成品都在 **`整理卷/`** 文件夹里，文件名形如 `001_PTE模考1B_写作_整理卷.pdf`。同一 part **序号最大的就是最新版**。
2. 想自己复现/改：对那一版的 `.tex` 跑一次 XeLaTeX 即可（见 §5）。每个 `.tex` 都是**单文件自包含**、不依赖任何图片。

---

## 3. 目录结构

```
pte-001-0621/
├─ README.md  制作流程.md          ← 先读这两份（总览 + 详细流程）
│
├─ 写作.pdf 写作详解1.pdf          ← 【原始素材】模考导出的原题/详解 PDF（只读，别改）
├─ 口语1.pdf 口语2.pdf 口语3.pdf 口语详解1.pdf
├─ 听力1.pdf 听力2.pdf 听力详解1.pdf
├─ 阅读1.pdf 阅读2.pdf
├─ 成绩.png                        ← 成绩总览截图（封面数字来源）
│
├─ 整理卷/                         ← 【成品】所有 part、所有版本都放这一个文件夹（见 §4）
│   ├─ 000_PTE模考1B_写作_整理卷.{pdf,tex}
│   ├─ 001_PTE模考1B_写作_整理卷.{pdf,tex}   ← 序号全局递增，只增不改
│   └─ …（口语 / 阅读 / 听力 依次接着编号）
│
└─ build/                          ← 【工作区/工具】誊写与排版的中间产物，可重新生成
    ├─ render.py / zoom.py / crop_tool.py   截图切分、放大（誊写时核对原图用）
    ├─ flatten.py                  把 paper/ 展平成单文件成品 → 整理卷/（见 §4、制作流程.md）
    ├─ extract/                    原始 PDF 抽出的文字（*.txt，多为空，仅参考）
    ├─ pages/ zoom/ crop/ preview/ 切好/放大的截图（.gitignore 内，可再生）
    └─ paper/                      ← LaTeX 真正的"活"源码（在这里编辑、预览）
        ├─ ptestyle.sty            共享样式：配色、批改宏(\fix \del \ins \add)、题块、评分表
        ├─ cover.tex               封面 / 成绩总览
        ├─ sec_<part>_body.tex     各部分正文（如 sec_writing_body.tex）
        └─ preview_<part>.tex      主文件：\input cover + sec_<part>_body
```

> 关系：`build/paper/` 是**可编辑的工作台**；`整理卷/` 里是**冻结的成品快照**（只增不改）。
> 成品 `.tex` = 把 `ptestyle.sty + cover.tex + sec_*_body.tex` 用 `build/flatten.py` **展平合并**成的一个单文件。

---

## 4. 成品版本规则（重要 —— 必须遵守）

用户定的规矩，新会话务必照做：

1. **一个版本 = 一对文件**：`<序号>_PTE模考<编号>_<部分>_整理卷.pdf` + 同名 `.tex`。
2. **只有一个成品文件夹 `整理卷/`**，所有 part、所有版本都放进去；靠**文件名里的部分名**区分写作 / 口语 / 阅读 / 听力。
3. **序号全局递增、从 `000` 起**，每产出或更新一份成品就用**下一个序号**（`000`→`001`→`002`…，三位数，不分 part 统一排）。某个 part 的最新版 = 带它名字的最大序号。
4. **绝不修改、绝不覆盖任何旧版本**——只**新增**下一个序号。旧的永远保持原样。
5. 成品 `.tex` 必须是**单文件自包含**（内联样式、无外部图片），保证多年后只靠这一个 `.tex` 就能复现同一 PDF。用 `build/flatten.py` 生成。

---

## 5. 环境与编译

**引擎：XeLaTeX**（中英混排，需 CJK 字体）。需要的字体：

- `Noto Sans CJK SC`、`Noto Serif CJK SC`（中文）
- `TeX Gyre Heros`（拉丁，Helvetica 风格）

安装（Debian/Ubuntu 示例）：

```bash
sudo apt-get install -y texlive-xetex texlive-latex-extra \
    fonts-noto-cjk fonts-texgyre
```

**编译某一版成品**（单文件，自包含）：

```bash
cd 整理卷
xelatex 001_PTE模考1B_写作_整理卷.tex      # 跑两遍，tcolorbox/fancyhdr 引用才稳定
xelatex 001_PTE模考1B_写作_整理卷.tex
```

**在工作区预览/继续排版**（编辑后快速看效果）：

```bash
cd build/paper
xelatex preview_writing.tex
xelatex preview_writing.tex
```

---

## 6. 新会话的标准流程（下次怎么继续）

1. **读 `README.md` + `制作流程.md`**，确认环境（`xelatex` + 上面三套字体都在）。
2. **看最新版 PDF**（`整理卷/` 里序号最大的）了解版式与配色风格，保持一致。
3. **在 `build/paper/` 工作**：
   - 新部分（如口语）→ 新建 `sec_speaking_body.tex` 和 `preview_speaking.tex`，复用 `ptestyle.sty`；
   - 改写作 → 编辑 `sec_writing_body.tex` / `cover.tex`；
   - 反复 `xelatex preview_*.tex` 预览，放大截图核对原图。
4. **产出新版本**：`python3 build/flatten.py <part英文> <中文> <考试号> <下一个序号>` 生成单文件 `.tex` 到 `整理卷/`，再 `xelatex` 编出 PDF——**不动任何旧版本**（见 §4）。
5. **提交并推送**：commit message 写清楚改了什么；推到指定的开发分支。

---

## 7. 批改标注图例（来自 `ptestyle.sty`）

| 宏 | 含义 | 颜色 |
|----|------|------|
| `\fix{原}{正}` | 修改 / 拼写 / 缺空格 | 红删除线 + 绿改正 |
| `\del{词}` | 应删除 | 蓝删除线 + "删" |
| `\ins{词}` | 应插入 | 紫色 + "∧插" |
| `\add{原}{正}` | **平台漏标**、本卷补标 | 橙色波浪线 + "补" |
| `\sfull/\spart/\szero` | 评分：满分 / 部分 / 零分 | 绿 / 橙 / 红 |

颜色主色为平台青绿 `cAccent = #16A085`；四项分数条形图配色见 `cover.tex`。
