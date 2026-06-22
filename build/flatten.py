#!/usr/bin/env python3
"""
把 build/paper/{ptestyle.sty, cover.tex, sec_<SEC>_body.tex} 展平成一个
自包含 .tex（内联样式），写入 整理卷/。

用法:
    python3 build/flatten.py <SEC> <CN> <EXAM> <NNN> [IMGDIR]
例:
    python3 build/flatten.py writing  写作 1B 000           # 纯文字 → 整理卷/000_..._写作_整理卷.tex
    python3 build/flatten.py speaking 口语 1B 000 img       # 含图片 → 整理卷/000_..._口语_整理卷/（含 tex + img/）

说明:
- 纯文字版本: 生成单文件 .tex 直接放在 整理卷/ 下（写作即如此）。
- 含图片版本: 传入 IMGDIR（build/paper 下的图片目录名，如 img）。此时生成一个
  **子文件夹** 整理卷/<NNN>_PTE模考<EXAM>_<CN>_整理卷/，里面放 .tex 和 img/，
  这样「tex + 图片」是一个自包含的可移植单元（图片版本的版本规则，见 制作流程.md）。
- 之后到目标目录 `xelatex` 那个 .tex（跑两遍）得到同名 PDF。
- 版本规则: **每个 part 各自从 000 起编号**，旧版本只读永不改。
"""
import sys, pathlib, shutil

if len(sys.argv) not in (5, 6):
    print(__doc__); sys.exit(1)

SEC, CN, EXAM, VER = sys.argv[1:5]
IMGDIR = sys.argv[5] if len(sys.argv) == 6 else None

root = pathlib.Path(__file__).resolve().parent.parent
base = root / "build" / "paper"

sty   = (base / "ptestyle.sty").read_text(encoding="utf-8")
cover = (base / "cover.tex").read_text(encoding="utf-8")
body  = (base / f"sec_{SEC}_body.tex").read_text(encoding="utf-8")

keep = [l for l in sty.splitlines()
        if not l.strip().startswith(r"\ProvidesPackage") and l.strip() != r"\endinput"]
sty_inline = "\n".join(keep).rstrip()

out = (
    f"% PTE Core 模考 {EXAM} —— {CN} 错题与详解·整理卷  版本 {VER}（自包含）\n"
    f"% 编译: xelatex 本文件.tex   （需 Noto CJK + TeX Gyre Heros 字体）\n"
    + ("% 本版本含图片，依赖同目录的 img/ 子目录。\n" if IMGDIR else "% 本版本无外部图片，单文件即可复现。\n")
    + "\\documentclass[11pt]{article}\n\n"
    "% --------- 样式（原 ptestyle.sty，已内联）---------\n" + sty_inline + "\n\n"
    "\\begin{document}\n\n"
    "% --------- 封面（原 cover.tex）---------\n" + cover.rstrip() + "\n\n"
    f"% --------- {CN}正文（原 sec_{SEC}_body.tex）---------\n" + body.rstrip() + "\n\n"
    "\\end{document}\n"
)

folder = root / "整理卷"
folder.mkdir(exist_ok=True)
stem = f"{VER}_PTE模考{EXAM}_{CN}_整理卷"

if IMGDIR and (base / IMGDIR).is_dir():
    outdir = folder / stem
    outdir.mkdir(exist_ok=True)
    shutil.copytree(base / IMGDIR, outdir / IMGDIR, dirs_exist_ok=True)
    dest = outdir / f"{stem}.tex"
else:
    dest = folder / f"{stem}.tex"

dest.write_text(out, encoding="utf-8")
print(dest)
