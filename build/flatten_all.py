#!/usr/bin/env python3
"""把四部分合并成一本【总整理卷】（自包含 .tex + img/），输出到 整理卷/总整理卷/。

用法:
    python3 build/flatten_all.py <EXAM>
例:
    python3 build/flatten_all.py 1B

- 内联 ptestyle.sty，依次拼 cover + 目录/概览 + 听力 + 口语 + 阅读 + 写作（听·说·读·写）。
- 口语含 DI 配图 → 同时把 build/paper/img/ 拷到 整理卷/总整理卷/img/，整体自包含。
- 生成后到该目录 `xelatex` 跑两遍（目录页码要第二遍才对），再把 PDF 复制到 整理卷/ 根。
"""
import sys, pathlib, shutil

EXAM = sys.argv[1] if len(sys.argv) > 1 else "1B"
root = pathlib.Path(__file__).resolve().parent.parent
base = root / "build" / "paper"

sty = (base / "ptestyle.sty").read_text(encoding="utf-8")
keep = [l for l in sty.splitlines()
        if not l.strip().startswith(r"\ProvidesPackage") and l.strip() != r"\endinput"]
sty_inline = "\n".join(keep).rstrip()
cover = (base / "cover.tex").read_text(encoding="utf-8").rstrip()

# 顺序：听 → 说 → 读 → 写
order = ["listening", "speaking", "reading", "writing"]
bodies = []
for sec in order:
    bodies.append(f"% ===== sec_{sec}_body.tex =====\n"
                  + (base / f"sec_{sec}_body.tex").read_text(encoding="utf-8").rstrip())
bodies_tex = "\n\n\\clearpage\n".join(bodies)

toc_overview = r"""\clearpage
\tableofcontents
\bigskip

{\large\bfseries\color{cAccent}本卷概览}\par\smallskip
{\small
\begin{tabularx}{\linewidth}{@{}l c >{\RaggedRight\arraybackslash}X r@{}}
\rowcolor{cHead}\textcolor{white}{\bfseries 部分} & \textcolor{white}{\bfseries 题量} & \textcolor{white}{\bfseries 题型构成} & \textcolor{white}{\bfseries 本项得分}\\
听力 Listening & 15 & SST · MCM-L · FIB-L\,$\times$3 · MCS-L · SMW\,$\times$2 · HIW\,$\times$3 · WFD\,$\times$4 & 33 / 90\\
口语 Speaking & 30 & RA\,$\times$7 · RS\,$\times$11 · DI\,$\times$3 · RTS\,$\times$3 · ASQ\,$\times$6 & 29 / 90\\
阅读 Reading & 16 & FIB\,$\times$5 · MCM\,$\times$2 · RO\,$\times$2 · FIB(R)\,$\times$5 · MCS\,$\times$2 & 42 / 90\\
写作 Writing & \phantom{0}4 & SWT\,$\times$2 · WE\,$\times$2 & 57 / 90\\
\end{tabularx}}
\par\smallskip
{\footnotesize\color{gray}总分 40（听力 33 / 阅读 42 / 口语 29 / 写作 57）。颜色与标注沿用各部分；本合订本顺序为「听·说·读·写」。}"""

out = (
    f"% PTE Core 模考 {EXAM} —— 总整理卷（听·说·读·写 合订，自包含）\n"
    f"% 编译: xelatex 本文件.tex（跑两遍，目录页码才对）；依赖同目录 img/。\n"
    "\\documentclass[11pt]{article}\n\n"
    "% --------- 样式（原 ptestyle.sty，已内联）---------\n" + sty_inline + "\n"
    "\\renewcommand{\\contentsname}{目录\\quad Contents}\n\n"
    "\\begin{document}\n\n"
    "% --------- 封面（原 cover.tex）---------\n" + cover + "\n\n"
    "% --------- 目录 + 本卷概览 ---------\n" + toc_overview + "\n\n"
    "\\clearpage\n% --------- 四部分正文 ---------\n" + bodies_tex + "\n\n"
    "\\end{document}\n"
)

outdir = root / "整理卷" / "总整理卷"
outdir.mkdir(parents=True, exist_ok=True)
stem = f"PTE模考{EXAM}_总整理卷"
(outdir / f"{stem}.tex").write_text(out, encoding="utf-8")
if (base / "img").is_dir():
    shutil.copytree(base / "img", outdir / "img", dirs_exist_ok=True)
print(outdir / f"{stem}.tex")
