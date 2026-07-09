#!/usr/bin/env python3
"""Render a learner persona's captured learning (transcript.md) as a self-contained,
illustrated HTML course for a claude.ai Artifact.

STANDARD (confirmed with the user — keep future topic renderings like this):
  - the FULL transcript dialogue for every concept (teach / reflect / answer / verdict),
  - a hand-drawn diagram or table per concept (drawn in-browser with rough.js),
  - handwriting scribbles (Caveat font, inlined), notebook aesthetic, role-coded beats,
  - fully self-contained: rough.js + font inlined (Artifact CSP blocks all external hosts;
    Mermaid cannot render there, so we use the rough.js engine).

Usage:
  python scripts/render_learning_artifact.py --learner alex --topic spark \\
      [--vault-dir <dir>] [--specs scripts/diagram_specs/<topic>.json] [--out out.html]

Then publish the produced HTML with the Artifact tool.

Per-topic diagram specs live in scripts/diagram_specs/<topic>.json:
  { "<concept-slug>": {
      "aha": "Alex's one-line takeaway (handwriting pull-quote)",
      "diagram": {"w":540,"h":200,"nodes":[{"id","x","y","w","h","t","c"}],"edges":[{"a","b","t"}]}
        # OR:  "table": [["header",...],["row",...], ...]
  }, ... }
Node colors ("c"): teal | amber | green | indigo | gray. Split node/edge labels with "|" or "\\n".
Concepts with no spec entry still render (full text, no figure).
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"


def esc(s: str) -> str:
    return html.escape(s)


def md_inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\[\[([a-z0-9-]+)\]\]", r'<span class="wl">\1</span>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def render_body(body: str) -> str:
    out = []
    for para in re.split(r"\n\s*\n", body.strip()):
        para = para.strip()
        if not para:
            continue
        lines = [l for l in para.splitlines() if l.strip()]
        if lines and all(l.lstrip().startswith(("- ", "* ")) for l in lines):
            out.append("<ul>" + "".join(f"<li>{md_inline(l.lstrip()[2:])}</li>" for l in lines) + "</ul>")
        else:
            out.append(f"<p>{md_inline(para)}</p>")
    return "\n".join(out)


BEATS = [("vutr teaches:", "teach", "vutr", "teaches"),
         ("Alex:", "alex", "Alex", "reflects &amp; asks"),
         ("vutr answers:", "answer", "vutr", "answers"),
         ("Verdict:", "verdict", "", "verdict")]


def split_beats(body: str):
    pat = re.compile(r"\*\*(" + "|".join(re.escape(b[0]) for b in BEATS) + r")\*\*")
    found = list(pat.finditer(body))
    return [(m.group(1), body[m.end():(found[k + 1].start() if k + 1 < len(found) else len(body))].strip())
            for k, m in enumerate(found)]


def table_html(rows):
    head = "".join(f"<th>{esc(c)}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def build(transcript: str, specs: dict, learner: str, topic: str) -> str:
    caveat = (ASSETS / "caveat.b64").read_text().strip()
    rough = (ASSETS / "roughjs.js").read_text()

    sec_re = re.compile(r"^## (\d+)\. ([a-z0-9-]+)\s+\(([^)]+)\)\s*$", re.MULTILINE)
    matches = list(sec_re.finditer(transcript))
    sections = [(m.group(1), m.group(2), m.group(3),
                 transcript[m.end():(matches[j + 1].start() if j + 1 < len(matches) else len(transcript))].strip())
                for j, m in enumerate(matches)]

    toc = "".join(f'<a class="tchip" href="#c{n}"><b>{n}</b> {slug}</a>' for n, slug, _, _ in sections)

    cards = []
    for num, slug, level, body in sections:
        d = specs.get(slug, {})
        if "diagram" in d:
            visual = f'<div class="diagram" data-spec=\'{json.dumps(d["diagram"])}\'></div>'
            cap = "a hand-drawn view"
        elif "table" in d:
            visual = table_html(d["table"])
            cap = "at a glance"
        else:
            visual = cap = ""
        fig = (f'<figure class="visual"><div class="figbody">{visual}</div>'
               f'<figcaption>{cap}</figcaption></figure>') if visual else ""
        aha = (f'<p class="aha"><span class="ahatag">the moment it clicks</span>{esc(d["aha"])}</p>'
               if d.get("aha") else "")
        blocks = []
        for marker, content in split_beats(body):
            _, cls, who, verb = next(b for b in BEATS if b[0] == marker)
            who_html = f'<span class="who {cls}">{who}</span> ' if who else ""
            blocks.append(f'<div class="beat {cls}"><div class="beatlabel">{who_html}'
                          f'<span class="verb">{verb}</span></div>'
                          f'<div class="beattext">{render_body(content)}</div></div>')
        cards.append(f'<section class="card" id="c{num}">'
                     f'<header class="cardhead"><span class="cnum" data-n="{num}"></span>'
                     f'<h2>{esc(slug)}</h2><span class="badge">{esc(level)}</span></header>'
                     f'{fig}{aha}<div class="dialogue">{"".join(blocks)}</div></section>')

    css = _CSS.replace("__CAVEAT__", caveat)
    head = _HEAD.replace("__TOC__", toc).replace("__LEARNER__", esc(learner)).replace("__TOPIC__", esc(topic))
    js = _JS.replace("%ROUGH%", rough)
    return css + head + "\n".join(cards) + _FOOT + js


_CSS = r"""
<style>
@font-face{font-family:'Caveat';src:url(data:font/woff2;base64,__CAVEAT__) format('woff2');font-weight:600;font-display:swap;}
:root{--paper:#FBFAF6;--ink:#20222A;--muted:#63697A;--line:#E6E2D8;
 --teal:#0E6E63;--amber:#B26A15;--green:#2F6B3D;--indigo:#3B3E86;--gray:#7B8091;
 --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
 --serif:Charter,"Iowan Old Style",Georgia,serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace;--hand:'Caveat',cursive;}
*{box-sizing:border-box;}
.wrap{background:linear-gradient(var(--paper),var(--paper)),repeating-linear-gradient(0deg,transparent 0 27px,rgba(80,90,120,.045) 27px 28px);
 color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.72;padding:0 18px 90px;}
.col{max-width:820px;margin:0 auto;}
.masthead{padding:52px 0 20px;}
.eyebrow{font-family:var(--sans);text-transform:uppercase;letter-spacing:.14em;font-size:11.5px;color:var(--indigo);font-weight:600;margin:0 0 12px;}
h1{font-family:var(--sans);font-weight:600;font-size:2.3rem;letter-spacing:-.015em;margin:0 0 6px;}
h1 .hand{font-family:var(--hand);color:var(--teal);font-size:2.6rem;}
.lede{color:var(--muted);max-width:60ch;margin:6px 0 20px;}
.stats{display:flex;flex-wrap:wrap;gap:9px;font-family:var(--sans);font-size:12.5px;}
.stat{background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 13px;}
.toc{display:flex;flex-wrap:wrap;gap:7px;margin:24px 0 8px;}
.tchip{font-family:var(--sans);font-size:12.5px;text-decoration:none;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:8px;padding:5px 10px;}
.tchip b{color:var(--indigo);font-variant-numeric:tabular-nums;}.tchip:hover{border-color:var(--teal);}
.card{padding:34px 0 6px;border-top:2px dashed var(--line);margin-top:16px;scroll-margin-top:12px;}
.cardhead{display:flex;align-items:center;gap:13px;margin:0 0 16px;}
.cnum{width:40px;height:40px;flex:none;}
.cardhead h2{font-family:var(--mono);font-weight:500;font-size:1.35rem;margin:0;flex:1;}
.badge{font-family:var(--sans);font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;font-weight:600;color:var(--green);background:#EBF3EC;border:1px solid #CDE3D2;padding:4px 10px;border-radius:999px;}
.visual{margin:0 0 18px;}
.figbody{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;overflow-x:auto;}
.figbody svg{display:block;width:100%;height:auto;}
.visual figcaption{font-family:var(--hand);font-size:1.15rem;color:var(--muted);text-align:center;margin-top:6px;}
table{border-collapse:collapse;width:100%;font-size:14px;font-family:var(--sans);}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);border-bottom:2px solid var(--line);padding:8px 10px;}
td{border-bottom:1px solid var(--line);padding:9px 10px;vertical-align:top;}tr td:first-child{font-weight:600;color:var(--indigo);}
.aha{font-family:var(--hand);font-size:1.55rem;line-height:1.3;color:var(--teal);margin:0 0 20px;background:linear-gradient(transparent 60%,#FBE9C9 60%);display:inline;padding:0 3px;}
.ahatag{display:block;font-family:var(--sans);font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;color:var(--amber);margin-bottom:1px;font-weight:600;-webkit-text-fill-color:var(--amber);}
.beat{border-left:3px solid var(--line);padding:2px 0 2px 18px;margin:0 0 20px;}
.beat.teach{border-color:var(--teal);}.beat.answer{border-color:var(--teal);border-left-style:dashed;}
.beat.alex{border-color:var(--amber);}
.beat.verdict{border-color:var(--green);background:#EBF3EC;border-left-style:solid;padding:12px 16px;border-radius:0 8px 8px 0;}
.beatlabel{font-family:var(--sans);font-size:12px;text-transform:uppercase;letter-spacing:.1em;margin:0 0 5px;color:var(--muted);}
.who{font-weight:600;}.who.teach,.who.answer{color:var(--teal);}.who.alex{color:var(--amber);}.verb{color:var(--muted);}
.beattext p{margin:0 0 12px;}.beattext p:last-child{margin-bottom:0;}.beat.verdict .beattext{font-size:.95rem;}
.wl{font-family:var(--mono);font-size:.8em;background:#EEF0F5;color:var(--indigo);padding:1px 6px;border-radius:5px;white-space:nowrap;}
code{font-family:var(--mono);font-size:.85em;background:#F0EEE8;padding:1px 5px;border-radius:4px;}
ul{margin:0 0 12px;padding-left:22px;}li{margin:0 0 4px;}
.footer{padding:34px 0 0;color:var(--muted);font-family:var(--sans);font-size:12.5px;border-top:2px dashed var(--line);margin-top:16px;}
@media(max-width:640px){h1{font-size:1.9rem;}.wrap{font-size:16.5px;}}
</style>
"""

_HEAD = """
<div class="wrap"><div class="col">
 <header class="masthead">
  <p class="eyebrow">An illustrated course · full dialogue · closed-book from the vutr wiki</p>
  <h1>__LEARNER__ learns <span class="hand">__TOPIC__</span></h1>
  <p class="lede">Each concept opens with a hand-drawn diagram or table, then the complete exchange:
   vutr teaches it at a 15-year-old level, __LEARNER__ says it back and asks the deeper question,
   vutr answers, and the verdict lands. Read in order — it builds.</p>
  <div class="stats"><span class="stat">every claim grounded in vutr&rsquo;s material</span></div>
  <nav class="toc">__TOC__</nav>
 </header>
"""

_FOOT = """
 <p class="footer">Diagrams drawn in-browser with a hand-drawn engine (rough.js); handwriting is Caveat.
  Where even vutr&rsquo;s deep material stops short, it&rsquo;s logged as a wiki gap — the roadmap for what to teach next.</p>
</div></div>
"""

_JS = r"""
<script>%ROUGH%</script>
<script>
(function(){
  var NS="http://www.w3.org/2000/svg";
  var FILL={teal:"#DDEFEC",amber:"#FBE5C9",green:"#E1EFE4",indigo:"#E2E3F4",gray:"#ECEDF1"};
  var STROKE={teal:"#0E6E63",amber:"#B26A15",green:"#2F6B3D",indigo:"#3B3E86",gray:"#7B8091"};
  function txt(svg,x,y,s,opt){opt=opt||{};var t=document.createElementNS(NS,"text");
    t.setAttribute("x",x);t.setAttribute("y",y);t.setAttribute("text-anchor",opt.anchor||"middle");
    t.setAttribute("font-family",opt.font||"-apple-system,Segoe UI,Roboto,sans-serif");
    t.setAttribute("font-size",opt.size||11.5);t.setAttribute("fill",opt.fill||"#20222A");
    if(opt.weight)t.setAttribute("font-weight",opt.weight);t.textContent=s;svg.appendChild(t);}
  function wrap(t){return String(t).split("|").reduce(function(a,seg){return a.concat(seg.split("\n"));},[]);}
  function node(rc,svg,n){var col=n.c||"gray";
    svg.appendChild(rc.rectangle(n.x,n.y,n.w,n.h,{fill:FILL[col],fillStyle:"solid",stroke:STROKE[col],roughness:1.5,bowing:1.4,strokeWidth:1.7}));
    var lines=wrap(n.t),cx=n.x+n.w/2,lh=15,y0=n.y+n.h/2-(lines.length-1)*lh/2+4;
    lines.forEach(function(ln,i){txt(svg,cx,y0+i*lh,ln,{size:11.5,weight:600});});}
  function C(n){return[n.x+n.w/2,n.y+n.h/2];}
  function edge(rc,svg,map,e){var A=map[e.a],B=map[e.b],ca=C(A),cb=C(B),dx=cb[0]-ca[0],dy=cb[1]-ca[1],sx,sy,ex,ey;
    if(Math.abs(dx)>=Math.abs(dy)){if(dx>=0){sx=A.x+A.w;sy=ca[1];ex=B.x;ey=cb[1];}else{sx=A.x;sy=ca[1];ex=B.x+B.w;ey=cb[1];}}
    else{if(dy>=0){sx=ca[0];sy=A.y+A.h;ex=cb[0];ey=B.y;}else{sx=ca[0];sy=A.y;ex=cb[0];ey=B.y+B.h;}}
    svg.appendChild(rc.line(sx,sy,ex,ey,{stroke:"#4A4F60",roughness:1.2,strokeWidth:1.6}));
    var a=Math.atan2(ey-sy,ex-sx),h=8;
    svg.appendChild(rc.line(ex,ey,ex-h*Math.cos(a-0.42),ey-h*Math.sin(a-0.42),{stroke:"#4A4F60",roughness:.8,strokeWidth:1.6}));
    svg.appendChild(rc.line(ex,ey,ex-h*Math.cos(a+0.42),ey-h*Math.sin(a+0.42),{stroke:"#4A4F60",roughness:.8,strokeWidth:1.6}));
    if(e.t)txt(svg,(sx+ex)/2,(sy+ey)/2-6,e.t,{font:"Caveat,cursive",size:15,fill:"#B26A15"});}
  function render(div){var spec=JSON.parse(div.getAttribute("data-spec"));
    var svg=document.createElementNS(NS,"svg");svg.setAttribute("viewBox","0 0 "+spec.w+" "+spec.h);svg.setAttribute("width","100%");div.appendChild(svg);
    var rc=rough.svg(svg),map={};spec.nodes.forEach(function(n){map[n.id]=n;});
    spec.nodes.forEach(function(n){node(rc,svg,n);});(spec.edges||[]).forEach(function(e){edge(rc,svg,map,e);});}
  function circles(){document.querySelectorAll(".cnum").forEach(function(el){
    var n=el.getAttribute("data-n");var svg=document.createElementNS(NS,"svg");
    svg.setAttribute("viewBox","0 0 40 40");svg.setAttribute("width","40");svg.setAttribute("height","40");el.appendChild(svg);
    var rc=rough.svg(svg);svg.appendChild(rc.circle(20,20,32,{stroke:"#3B3E86",roughness:1.9,strokeWidth:2,fill:"#E2E3F4",fillStyle:"solid"}));
    txt(svg,20,27,n,{font:"Caveat,cursive",size:22,fill:"#3B3E86"});});}
  function underlines(){document.querySelectorAll(".mark").forEach(function(el){
    var w=el.offsetWidth||60;var svg=document.createElementNS(NS,"svg");svg.setAttribute("width",w);svg.setAttribute("height","8");
    svg.setAttribute("viewBox","0 0 "+w+" 8");svg.style.position="absolute";svg.style.left="0";svg.style.bottom="-5px";el.appendChild(svg);
    var rc=rough.svg(svg);svg.appendChild(rc.line(2,4,w-2,5,{stroke:"#B26A15",roughness:2.3,strokeWidth:2,bowing:3}));});}
  function go(){document.querySelectorAll(".diagram").forEach(render);circles();underlines();}
  if(document.readyState!=="loading")go();else document.addEventListener("DOMContentLoaded",go);
})();
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--learner", default="alex")
    ap.add_argument("--topic", default="spark")
    ap.add_argument("--vault-dir", default=None, help="repo root; defaults to two levels up")
    ap.add_argument("--specs", default=None, help="diagram specs JSON; defaults to scripts/diagram_specs/<topic>.json")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    root = Path(a.vault_dir).expanduser().resolve() if a.vault_dir else HERE.parent
    transcript = (root / "wiki/personas" / a.learner / a.topic / "transcript.md").read_text(encoding="utf-8")
    specs_path = Path(a.specs) if a.specs else HERE / "diagram_specs" / f"{a.topic}.json"
    specs = json.loads(specs_path.read_text(encoding="utf-8")) if specs_path.exists() else {}
    out = Path(a.out) if a.out else HERE / f"{a.learner}-{a.topic}-illustrated.html"
    out.write_text(build(transcript, specs, a.learner.capitalize(), a.topic.replace("-", " ").title()),
                   encoding="utf-8")
    print(f"wrote {out} — {len(specs)} concept specs; publish it with the Artifact tool.")


if __name__ == "__main__":
    main()
