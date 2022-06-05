import fontforge
import shutil
import os

d2coding_name = "D2Coding-Ver1.3.2-20180524.ttf"
d2coding_width = 1000
jbmono_directory = "jbmono"
jbmono_width = 1200
out_directory = "out"

if not os.path.exists(out_directory):
    os.makedirs(out_directory)

addition = jbmono_width-d2coding_width

def add_bearing(glyph, addition):
    glyph.left_side_bearing = addition//2+int(glyph.left_side_bearing)
    glyph.right_side_bearing = addition//2+int(glyph.right_side_bearing)
    return glyph

def replace_name(string):
    return string.replace("JetBrainsMono", "JetBrainsMonoHangul") \
            .replace("JetBrains Mono", "JetBrainsMonoHangul")

d2 = fontforge.open(d2coding_name)

hangul = d2.selection.select(("unicode", "ranges"), 0x3131, 0x318E) \
        .select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3) 
for i in hangul:
    glyph = d2[i]
    if not glyph.references:
        add_bearing(glyph, 200)
    else:
        for j in glyph.references:
            refglyph = d2[j[0]]
            if int(refglyph.width) == jbmono_width:
                continue
            else:
                add_bearing(refglyph, 200)
d2.copy()

for name in os.listdir(jbmono_directory):
    jb = fontforge.open(f"{jbmono_directory}/{name}")
    jb.selection.select(("unicode", "ranges"), 0x3131, 0x318E) \
        .select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)
    jb.paste()

    namel = name.split(".")
    namel[len(namel)-2]+="-Hangul"

    jb.familyname = replace_name(jb.familyname)
    jb.fontname = replace_name(jb.fontname)
    jb.fullname = replace_name(jb.fullname)

    subFamilyIdx = [x[1] for x in jb.sfnt_names].index("SubFamily")
    sfntNamesStringIdIdx = 2
    subFamily = jb.sfnt_names[subFamilyIdx][sfntNamesStringIdIdx]

    jb.appendSFNTName("English (US)", "Preferred Family", jb.familyname)
    jb.appendSFNTName("English (US)", "Family", jb.familyname)
    jb.appendSFNTName("English (US)", "Compatible Full", jb.fullname)
    jb.appendSFNTName("English (US)", "SubFamily", subFamily)
    jb.generate(".".join(namel))
    shutil.move(".".join(namel), out_directory+"/"+".".join(namel))
    print("Exported "+ ".".join(namel))
