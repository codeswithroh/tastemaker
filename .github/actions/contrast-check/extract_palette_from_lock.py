#!/usr/bin/env python3
import re, pathlib, sys
p = sys.argv[1] if len(sys.argv) > 1 else ".tastemaker/style-lock.md"
t = pathlib.Path(p).read_text(encoding="utf-8")
m = re.search(r"## Palette(.*?)(?:\n## |\Z)", t, re.S)
pt = m.group(1) if m else t
mp = {"background":"bg","surface":"surface","dark surface":"dark","primary":"primary","accent":"accent","text primary":"text","text":"text","text muted":"muted","muted":"muted","on-dark text":"on-dark","on-dark":"on-dark","button label color":"on-primary","on-primary":"on-primary","border":"border","bg":"bg","dark":"dark"}
roles={}
for line in pt.splitlines():
    hm = re.search(r"#([0-9a-fA-F]{6})", line)
    if not hm: continue
    hv = hm.group(1).lower()
    lm = re.search(r"-\s*([^:]+):", line)
    if not lm: continue
    lb = lm.group(1).strip().lower()
    lb = re.sub(r"^[^a-z]+", "", lb)
    ro = mp.get(lb)
    if not ro:
        for k,v in mp.items():
            if k in lb:
                ro=v
                break
    if ro and ro not in roles:
        roles[ro]=hv
print(" ".join(f"{k}={v}" for k,v in roles.items()), end="")
