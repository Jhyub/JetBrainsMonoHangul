import fontforge
import shutil
import os

from config import *

def add_bearing(glyph, addition):
    glyph.left_side_bearing = addition//2+int(glyph.left_side_bearing)
    glyph.right_side_bearing = addition//2+int(glyph.right_side_bearing)
    return glyph

def replace_name(string):
    return string.replace("JetBrainsMono", "JetBrainsMonoHangul") \
            .replace("JetBrains Mono", "JetBrainsMonoHangul")

def build_font():
    if not os.path.exists(out_path):
        print(f'[INFO] Make \'{out_path}\' directory')
        os.makedirs(out_path)

    d2 = fontforge.open(f'{download_path}/D2Coding/D2Coding-Ver{d2_coding_version}-{d2_coding_date}.ttf')

    hangul = d2.selection.select(("unicode", "ranges"), 0x3131, 0x318E) \
            .select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3) 
    for i in hangul:
        glyph = d2[i]
        if not glyph.references:
            add_bearing(glyph, jetbrains_mono_width - d2_coding_width)
        else:
            for j in glyph.references:
                refglyph = d2[j[0]]
                if int(refglyph.width) == jetbrains_mono_width:
                    continue
                else:
                    add_bearing(refglyph, jetbrains_mono_width - d2_coding_width)
    d2.copy()

    print("[INFO] Merge fonts and output")
    for name in os.listdir(f'{download_path}/fonts/ttf'):
        jb = fontforge.open(f"{download_path}/fonts/ttf/{name}")
        jb.selection.select(("unicode", "ranges"), 0x3131, 0x318E) \
            .select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)
        jb.paste()

        namel = name.split(".")
        namel[-2] = replace_name(namel[-2])

        jb.familyname = replace_name(jb.familyname)
        jb.fontname = replace_name(jb.fontname)
        jb.fullname = replace_name(jb.fullname)

        subFamilyIdx = [x[1] for x in jb.sfnt_names].index("SubFamily")
        sfntNamesStringIdIdx = 2
        subFamily = jb.sfnt_names[subFamilyIdx][sfntNamesStringIdIdx]

        for (language, strid, string) in jb.sfnt_names:
            if strid == "UniqueID":
                jb.appendSFNTName(language, strid, f"{jb.fullname} {version_name}")
            
            if strid == "Version":
                jb.appendSFNTName(language, strid, f"{string};Hangulify {version_name}")

            if strid == "Preferred Family":
                jb.appendSFNTName(language, strid, replace_name(string))

        for (language, strid, string) in jb.sfnt_names:
            print(language, strid, string)

        jb.generate(".".join(namel))
        shutil.move(".".join(namel), out_path+"/"+".".join(namel))
        print("[INFO] Exported "+ ".".join(namel))
