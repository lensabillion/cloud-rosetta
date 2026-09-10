#!/usr/bin/env python3
"""Assemble the multi-page guide from the dataset and the Markdown chapters.

Built to docs/design-system.md. The structure is a journey first and a
reference second, never mixed in one view, with the whole shape visible in a
sidebar from every page. Pages are routed on the hash so the guide stays a
single publishable document.
"""

from __future__ import annotations

import datetime as dt
import html
import pathlib

import mdlite

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
CLOUDS = (("aws", "AWS"), ("azure", "Azure"), ("gcp", "Google Cloud"))
DIVERGENCE = {"exact": "Transfers cleanly", "partial": "Behaves differently", "none": "No equivalent"}
BITE = {"serious": "Serious", "regular": "Regular", "tip": "Tip"}
BITE_HELP = {
    "serious": "Significant risk or cost: a security exposure, real money, or an architectural choice that is hard to correct.",
    "regular": "Consequences are things not working, breaking, or not scaling gracefully.",
    "tip": "Important or often overlooked, but nothing breaks if you miss it.",
}


def esc(v) -> str:
    return html.escape(str(v if v is not None else ""), quote=True)


def flat(v) -> str:
    return esc(" ".join(str(v or "").split()))


# --------------------------------------------------------------------- pieces

def service_line(row: dict, key: str, label: str) -> str:
    block = row.get(key) or {}
    name, url = block.get("name"), block.get("url")
    if name:
        inner = f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(name)}</a>' if url else esc(name)
    else:
        inner = "<em>no equivalent</em>"
    extra = ""
    if block.get("maturity") == "superseded":
        extra += '<span class="meta">&#9873; superseded by the vendor</span>'
    if block.get("formerly"):
        extra += f'<span class="meta was">was {esc(", ".join(block["formerly"]))}</span>'
    if block.get("note"):
        extra += f'<span class="meta">{flat(block["note"])}</span>'
    return (f'<div class="svc {key}"><span class="who">{esc(label)}</span>'
            f'<span class="what">{inner}{extra}</span></div>')


def row_html(row: dict, domain: str) -> str:
    div, bite = row.get("divergence", "exact"), row.get("bite", "tip")
    services = "".join(service_line(row, k, lbl) for k, lbl in CLOUDS)

    note = ""
    if row.get("breaks_when"):
        note = ('<details class="note"><summary>Where it breaks</summary>'
                f'<p>{flat(row["breaks_when"])}</p></details>')
    elif row.get("shared_trap"):
        note = ('<details class="note"><summary>Same everywhere, still caught out</summary>'
                f'<p>{flat(row["shared_trap"])}</p></details>')

    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in row.get("exam_tags") or [])
    hay = " ".join([row.get("concept", ""), domain, div, bite, " ".join(row.get("exam_tags") or [])]
                   + [str((row.get(k) or {}).get("name") or "") for k, _ in CLOUDS]
                   + [row.get("breaks_when", ""), row.get("shared_trap", "")]).lower()

    return f"""<article class="row" data-bite="{esc(bite)}" data-div="{esc(div)}" data-find="{esc(hay)}">
<div class="rhead"><h3>{esc(row.get('concept'))}</h3><span class="marks">
<span class="mk b-{esc(bite)}" title="{esc(BITE_HELP[bite])}">{esc(BITE[bite])}</span>
<span class="mk d-{esc(div)}">{esc(DIVERGENCE[div])}</span></span></div>
<div class="svcs">{services}</div>
{note}
<div class="rfoot">{tags}<span class="stamp">Verified {esc(row.get('verified'))}</span></div>
</article>"""


def term_html(term: dict) -> str:
    sev = term.get("severity", "low")
    senses = ""
    for key, label in CLOUDS:
        s = term.get(key)
        if not s:
            continue
        cat = esc(s.get("category"))
        cat = f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{cat}</a>' if s.get("url") else cat
        senses += (f'<div class="sense {key}"><span class="who">{esc(label)}</span>'
                   f'<span><span class="cat">{cat}</span><p>{flat(s.get("meaning"))}</p></span></div>')
    hay = (term.get("term", "") + " " + term.get("why_it_hurts", "") + " " +
           " ".join(str((term.get(k) or {}).get("meaning") or "") for k, _ in CLOUDS)).lower()
    label = {"high": "Different kind of thing", "medium": "Materially different", "low": "Naming difference"}[sev]
    return f"""<article class="term s-{esc(sev)}" data-find="{esc(hay)}">
<h3>{esc(term.get('term'))}</h3><span class="sev">{esc(label)}</span>
<div class="senses">{senses}</div>
<details class="note" open><summary>Why it costs marks</summary><p>{flat(term.get('why_it_hurts'))}</p></details>
</article>"""


def toolbar(scope: str, extra: str = "") -> str:
    return (f'<div class="toolbar"><input type="search" data-scope="{scope}" '
            f'placeholder="Search this page" aria-label="Search this page">{extra}'
            f'<span class="tcount" data-count="{scope}"></span></div>')


# --------------------------------------------------------------------- pages

def page_home(counts: dict, terms: int, exams: int) -> str:
    return f"""<section class="page hero" id="p-home">
<p class="eyebrow">AWS &middot; Azure &middot; Google Cloud</p>
<h1>The same idea, three different shapes.</h1>
<p class="lede">Most cross-cloud comparisons tell you what a service is called somewhere else.
This one tells you <b>what breaks when you assume it works the same way</b>, and it says so on
every row.</p>
<a class="cta" href="#00-landscape">Start reading &rarr;</a>
<p class="after">{counts['total']} graded mappings, {terms} colliding terms and {exams} exams.
Free, open source, and every claim links to the vendor's own page.</p>
</section>"""


def page_from_markdown(slug: str, path: pathlib.Path) -> str:
    body, _ = mdlite.render(path.read_text(encoding="utf-8"))
    return f'<section class="page hide" id="p-{slug}">{body}</section>'


def page_reference(domain: str, title: str, rows: list[dict]) -> str:
    serious = sum(1 for r in rows if r.get("bite") == "serious")
    body = "".join(row_html(r, domain) for r in rows)
    extra = '<button data-filter="serious" aria-pressed="false">Only what hurts</button>'
    return f"""<section class="page hide" id="p-ref-{domain}">
<p class="eyebrow">Service equivalents</p>
<h1>{esc(title)}</h1>
<p>{len(rows)} mappings, {serious} of them graded serious. Each row states how far the
equivalence can be trusted; open a note to see what actually differs.</p>
{toolbar('ref-' + domain, extra)}
<div class="list">{body}</div>
<p class="empty hide">Nothing on this page matches.</p>
</section>"""


def page_decoder(terms: list[dict]) -> str:
    order = {"high": 0, "medium": 1, "low": 2}
    terms = sorted(terms, key=lambda t: (order[t["severity"]], t["term"].lower()))
    high = sum(1 for t in terms if t["severity"] == "high")
    body = "".join(term_html(t) for t in terms)
    return f"""<section class="page hide" id="p-decoder">
<p class="eyebrow">Look it up</p>
<h1>The word means something else here</h1>
<p>{len(terms)} terms the three clouds use differently. {high} of them name a different
<em>kind of thing</em> rather than the same thing behaving differently, which is why a service
comparison table cannot hold them.</p>
{toolbar('decoder')}
<div class="list">{body}</div>
<p class="empty hide">No term matches.</p>
</section>"""


def page_exams(exams: list[dict]) -> str:
    levels = ["foundational", "associate", "professional", "expert", "specialty"]
    names = {"aws": "AWS", "azure": "Azure", "gcp": "Google Cloud"}
    current = [e for e in exams if e["status"] == "current"]
    retired = [e for e in exams if e["status"] != "current"]

    out = []
    for prov in ("aws", "azure", "gcp"):
        rows = sorted([e for e in current if e["provider"] == prov],
                      key=lambda e: (levels.index(e["level"]), e["code"]))
        if not rows:
            continue
        trs = "".join(
            f'<tr><td><code>{esc(e["code"])}</code></td>'
            f'<td><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["name"])}</a></td>'
            f'<td>{esc(e["level"])}</td><td>{esc(e["verified"])}</td></tr>' for e in rows)
        out.append(f'<h2>{names[prov]}</h2><div class="tw"><table><thead><tr>'
                   f'<th>Code</th><th>Certification</th><th>Level</th><th>Verified</th>'
                   f'</tr></thead><tbody>{trs}</tbody></table></div>')

    trs = "".join(
        f'<tr><td><code>{esc(e["code"])}</code></td>'
        f'<td><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["name"])}</a></td>'
        f'<td>{names[e["provider"]]}</td><td>{flat(e.get("note", "Retired."))}</td></tr>'
        for e in sorted(retired, key=lambda e: e["code"]))
    out.append(f'<h2>Retired</h2><p>Listed rather than deleted, because course material for them '
               f'is still on sale.</p><div class="tw"><table><thead><tr><th>Code</th>'
               f'<th>Certification</th><th>Cloud</th><th>Note</th></tr></thead>'
               f'<tbody>{trs}</tbody></table></div>')

    return f"""<section class="page wide hide" id="p-exams">
<p class="eyebrow">Look it up</p>
<h1>Which exam, and what it costs</h1>
<p>{len(current)} current exams and {len(retired)} retired ones, each linked to the vendor's own
page. An exam retiring and a product retiring are separate events; only the exam is tracked here.</p>
{"".join(out)}
</section>"""


# --------------------------------------------------------------------- assembly

def nav(groups: list) -> str:
    out = []
    for title, items in groups:
        links = ""
        for item in items:
            if isinstance(item, tuple) and item[0] == "sub":
                kids = "".join(f'<a class="nl" href="#{esc(s)}">{esc(l)}</a>' for s, l in item[2])
                links += f'<div class="sub">{kids}</div>'
            else:
                slug, label = item
                links += f'<a class="nl" href="#{esc(slug)}">{esc(label)}</a>'
        out.append(f'<div class="grp"><h2>{esc(title)}</h2>{links}</div>')
    return "<nav id=\"nav\">" + "".join(out) + "</nav>"


ROUTER = """
<script>
(function(){
  var pages=[].slice.call(document.querySelectorAll('.page'));
  var links=[].slice.call(document.querySelectorAll('.side a.nl'));
  function has(id){return !!document.getElementById('p-'+id);}

  function show(id){
    if(!has(id)) id='home';
    var target=document.getElementById('p-'+id);
    pages.forEach(function(p){p.classList.toggle('hide',p!==target);});
    links.forEach(function(a){
      if(a.getAttribute('href')==='#'+id){a.setAttribute('aria-current','page');}
      else{a.removeAttribute('aria-current');}
    });
    var h1=target.querySelector('h1');
    document.title=(h1?h1.textContent+' \u2014 ':'')+'Cloud Rosetta';
    window.scrollTo(0,0);
    var n=document.getElementById('nav'); if(n) n.classList.remove('open');
  }

  // Route on the click itself. Some sandboxes refuse hash navigation, and the
  // guide must not depend on it; the hash is a nicety for deep links, not the
  // mechanism.
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href^="#"]');
    if(a){
      var id=a.getAttribute('href').slice(1);
      if(has(id)){
        e.preventDefault(); show(id);
        try{history.replaceState(null,'','#'+id);}catch(_){}
      }
      return;                      // in-page heading anchors fall through
    }
    var b=e.target.closest('.toolbar button');
    if(b){
      var on=b.getAttribute('aria-pressed')==='true';
      b.setAttribute('aria-pressed',String(!on));
      var box=b.closest('.page').querySelector('input[type=search]');
      box.dispatchEvent(new Event('input',{bubbles:true}));
      return;
    }
    if(e.target.closest('.menutog')){document.getElementById('nav').classList.toggle('open');return;}
    if(e.target.closest('.themetog')){
      var cur=document.documentElement.getAttribute('data-theme');
      var next=cur==='dark'?'light':(cur==='light'?'dark':(matchMedia('(prefers-color-scheme: dark)').matches?'light':'dark'));
      document.documentElement.setAttribute('data-theme',next);
      try{localStorage.setItem('cr-theme',next);}catch(_){}
    }
  });

  window.addEventListener('hashchange',function(){show((location.hash||'#home').slice(1));});

  document.addEventListener('input',function(e){
    var box=e.target.closest('input[type=search]'); if(!box) return;
    var page=box.closest('.page'), q=box.value.trim().toLowerCase();
    var items=[].slice.call(page.querySelectorAll('[data-find]')), shown=0;
    var only=page.querySelector('.toolbar button[aria-pressed="true"]');
    items.forEach(function(it){
      var ok=(!q||it.dataset.find.indexOf(q)!==-1)&&(!only||it.dataset.bite==='serious');
      it.classList.toggle('hide',!ok); if(ok)shown++;
    });
    page.querySelector('.tcount').textContent=shown+' / '+items.length;
    page.querySelector('.empty').classList.toggle('hide',shown>0);
  });

  try{var th=localStorage.getItem('cr-theme'); if(th)document.documentElement.setAttribute('data-theme',th);}catch(_){}
  document.querySelectorAll('.tcount').forEach(function(c){
    var p=c.closest('.page'); c.textContent=p.querySelectorAll('[data-find]').length+' items';
  });
  show(((location.hash||'#home').slice(1))||'home');
})();
</script>
"""


REPO = "https://github.com/lensabillion/cloud-rosetta/blob/main/docs"

# Chapter stem -> in-page route. Anything not here links back to the repository,
# so a reference to a research document does not become a dead in-page link.
ROUTES = {
    "00-landscape": "00-landscape",
    "01-mental-models": "01-mental-models",
    "02-identity": "02-identity",
    "03-networking": "03-networking",
    "05-databases": "05-databases",
    "09-confusing-terms": "decoder",
    "10-exam-map": "exams",
    "practice": "practice",
    "README": "home",
}


def resolve(stem: str) -> str:
    return f"#{ROUTES[stem]}" if stem in ROUTES else f"{REPO}/{stem}.md"


def build(domains: list[dict], terms: list[dict], exams: list[dict], out: pathlib.Path) -> dict:
    mdlite.RESOLVE = resolve

    rows = [r for d in domains for r in d["rows"]]
    counts = {"total": len(rows),
              "serious": sum(1 for r in rows if r.get("bite") == "serious")}

    pages = [page_home(counts, len(terms), len(exams))]

    journey = [("00-landscape", "What these three clouds are"),
               ("01-mental-models", "How they are shaped differently")]
    learn = [("02-identity", "Who can do what"),
             ("03-networking", "How the network is put together"),
             ("05-databases", "Where data lives")]

    for slug, _ in journey + learn:
        path = DOCS / f"{slug}.md"
        if path.exists():
            pages.append(page_from_markdown(slug, path))

    pages.append(page_decoder(terms))

    refs = []
    for doc in domains:
        slug, title = doc["domain"], doc.get("title", doc["domain"].title())
        pages.append(page_reference(slug, title, doc["rows"]))
        refs.append((f"ref-{slug}", title))

    if exams:
        pages.append(page_exams(exams))
    if (DOCS / "practice.md").exists():
        pages.append(page_from_markdown("practice", DOCS / "practice.md"))

    groups = [
        ("Start here", journey),
        ("Learn the parts that differ", learn),
        ("Look it up", [("decoder", "The word means something else here"),
                        ("sub", "Service equivalents", refs),
                        ("exams", "Which exam, and what it costs")]),
        ("Practise", [("practice", "Drills and self-check")]),
    ]

    shell = (ROOT / "scripts" / "shell.html").read_text(encoding="utf-8")
    body = f"""
<button class="themetog" title="Switch light and dark" aria-label="Switch light and dark">&#9681;</button>
<div class="app">
  <aside class="side">
    <div class="brand"><a href="#home"><b>Cloud Rosetta</b></a>
      <span>AWS, Azure and Google Cloud, side by side</span></div>
    <button class="menutog">Contents</button>
    {nav(groups)}
  </aside>
  <main class="doc">
{"".join(pages)}
  </main>
</div>
{ROUTER}"""

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(shell + body, encoding="utf-8")
    return {"pages": len(pages), "rows": len(rows), "terms": len(terms), "exams": len(exams),
            "nav": sum(len(i) if t != "Look it up" else len(refs) + 2 for t, i in groups)}
