#!/usr/bin/env python3
"""
把 build/paper/{ptestyle.sty, cover.tex, sec_<SEC>_body.tex} 展平成一个
单文件自包含 .tex（内联样式、无外部图片），写入 整理卷/<NNN>_PTE模考<EXAM>_<CN>_整理卷.tex

用法:
    python3 build/flatten.py <SEC> <CN> <EXAM> <NNN>
例:
    python3 build/flatten.py writing  写作 1B 001
    python3 build/flatten.py speaking 口语 1B 002

之后到 整理卷/ 里 `xelatex` 那个 .tex（跑两遍）得到同名 PDF。
版本规则: 序号 NNN 全局递增、从 000 起，旧版本只读永不改（见 制作流程.md / README.md）。
"""
import sys, pathlib

if len(sys.argv) != 5:
    print(__doc__); sys.exit(1)

SEC, CN, EXAM, VER = sys.argv[1:5]
root = pathlib.Path(__file__).resolve().parent.parent
base = root / "build" / "paper"

sty   = (base / "ptestyle.sty").read_text(encoding="utf-8")
cover = (base / "cover.tex").read_text(encoding="utf-8")
body  = (base / f"sec_{SEC}_body.tex").read_text(encoding="utf-8")

# .sty 去掉只能在宏包里用的两行，其余可放进文档导言区
keep = [l for l in sty.splitlines()
        if not l.strip().startswith(r"\ProvidesPackage") and l.strip() != r"\endinput"]
sty_inline = "\n".join(keep).rstrip()

out = (
    f"% PTE Core 模考 {EXAM} —— {CN} 错题与详解·整理卷  版本 {VER}（单文件自包含）\n"
    f"% 编译: xelatex 本文件.tex   （需 Noto CJK + TeX Gyre Heros 字体；无外部图片）\n"
    "\\documentclass[11pt]{article}\n\n"
    "% --------- 样式（原 ptestyle.sty，已内联）---------\n" + sty_inline + "\n\n"
    "\\begin{document}\n\n"
    "% --------- 封面（原 cover.tex）---------\n" + cover.rstrip() + "\n\n"
    f"% --------- {CN}正文（原 sec_{SEC}_body.tex）---------\n" + body.rstrip() + "\n\n"
    "\\end{document}\n"
)

folder = root / "整理卷"
folder.mkdir(exist_ok=True)
dest = folder / f"{VER}_PTE模考{EXAM}_{CN}_整理卷.tex"
dest.write_text(out, encoding="utf-8")
print(dest)
