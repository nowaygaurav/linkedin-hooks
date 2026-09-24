#!/usr/bin/env python3
"""Builds index.html for the '10 hooks i actually posted' guide.
Edit the HOOKS list below, then run:  python3 build.py && ./make-pdf.sh
"""
import os
import re
from pathlib import Path

HERE = Path(__file__).parent

# Each hook: name (last words get the marker underline), type chip, lede,
# the two real lines, stats, why bullets, watch-out, template (use [..] for blanks), your-turn task.
HOOKS = [
    dict(
        name=("the flex", "with a twist"), chip="celebration + contrast",
        lede="say the impressive thing, then undercut it straight away. the gap between the two lines is the hook.",
        l1="i was the president of Finance & Investment Cell, Aryabhatta College",
        l2="and now my career is complete opposite of it",
        reactions=175, comments=14,
        why=["line 1 is proof, so nobody scrolls past thinking you're a nobody",
             "line 2 opens a question: wait, why did he leave?",
             "the flex feels earned because the post is about walking away from it"],
        watch="if the twist never comes, it's just a brag with extra steps.",
        tpl="i was [the impressive thing you used to be] / and now i [do the complete opposite]",
        turn="write down 3 titles, roles or wins you had that have nothing to do with your work today. pick the one people would least expect from you. that's line 1.",
    ),
    dict(
        name=("the", "confession"), chip="face + story",
        lede="open on the feeling you'd normally hide. people stop for the emotion and stay for the story.",
        l1="seeing my mother crying was not on the bucket list gang",
        l2="but your boy has finally moved out..",
        reactions=171, comments=33,
        why=["line 1 is a scene, not a claim. you can literally see it",
             "“gang” and “your boy” stop it from getting too heavy",
             "line 2 says what actually happened, so nobody feels tricked"],
        watch="don't fake the feeling. people can smell a manufactured tear from the feed.",
        tpl="[the emotional moment you didn't plan for] / but [the big thing you actually did]",
        turn="think of the last big decision you made. what was the hardest moment around it, the one you'd skip if you told the story at a party? start there.",
    ),
    dict(
        name=("the", "receipt"), chip="credibility",
        lede="one exact number does more than a paragraph of adjectives. the more precise, the more people believe it.",
        l1="in the month of july i spent 1,15,643",
        l2="to be precise",
        reactions=155, comments=28,
        why=["1,15,643 is not a round number, so it reads as true",
             "money is the one topic everyone reads twice",
             "“to be precise” is a tiny joke. it sounds like a person, not a report"],
        watch="the number needs a story behind it. mine was moving out and buying my brother a phone.",
        tpl="in [a time period] i [spent / sent / lost / made] [an exact, unrounded number] / [a 3 word aside]",
        turn="open your bank app, screen time, calendar or sent folder. find one number from last month that surprised you. don't round it.",
    ),
    dict(
        name=("the", "“how did i”"), chip="value",
        lede="ask the question people would DM you anyway, then answer it in the post. it's a promise dressed up as a question.",
        l1="how as a 21 year old i managed",
        l2="to move out from my house?",
        reactions=141, comments=30,
        why=["it's specific: an age, an action, a result",
             "it promises a how, so people expect steps and stay for them",
             "30 comments, because everyone had their own version to share"],
        watch="you have to actually give the how. a question hook with a vague answer burns trust fast.",
        tpl="how as a [who you were back then] i managed / to [the thing people think is hard]?",
        turn="what's one thing people keep asking you “how did you do that?” about? write the question exactly the way they ask it.",
    ),
    dict(
        name=("the", "fake-out"), chip="surprise",
        lede="say something that sounds like one thing, then flip it in the very next line.",
        l1="i hate posting on linkedin nowadays!!",
        l2="and it's not what you think",
        reactions=118, comments=11,
        also=("i am hiring, actually not for my company!", "105 reactions · 27 comments"),
        why=["line 1 gives a tiny “wait, what?”",
             "line 2 admits there's a twist, so people tap to get it",
             "it only works when the flip is honest"],
        watch="the real reason has to be good. if the twist is boring, the fake-out feels like a lie.",
        tpl="i [a strong statement nobody expects from you] / and it's not what you think",
        turn="finish “i hate ___” three different ways. keep the one where the real reason is the opposite of what people will assume.",
    ),
    dict(
        name=("the withheld", "answer"), chip="curiosity",
        lede="tell them there IS an answer. just don't give it in line 1.",
        l1="i inherited the one thing",
        l2="i used to hate about my dad",
        reactions=107, comments=27,
        why=["“the one thing” opens a loop the brain wants to close",
             "everyone has a thing they swore they'd never become",
             "the answer lands right after “see more”, so they have to tap"],
        watch="pay it off fast. if the answer is buried at the bottom, people leave.",
        tpl="i [inherited / copied / became] the one thing / i used to [hate / judge / laugh at] about [a person]",
        turn="who's the person you swore you'd never become? what's one habit of theirs you have now? that's your post.",
    ),
    dict(
        name=("the", "backfire"), chip="honest failure",
        lede="tell them the plan went wrong. people trust the person who admits it way more than the one who only posts wins.",
        l1="moving out actually backfired on me",
        l2="because i didn't see coming these things",
        reactions=80, comments=11,
        why=["it's the sequel to a win they already saw, so they're invested",
             "“backfired” is one strong, simple word",
             "an honest update beats a polished highlight reel"],
        watch="don't end in self pity. end with what you're changing. mine was timeblocking.",
        tpl="[a decision you were proud of] actually backfired on me / because [what you didn't see coming]",
        turn="pick something you posted about proudly 1 to 3 months ago. what went wrong after? write the update nobody asked for.",
    ),
    dict(
        name=("the", "one-liner"), chip="photo + one line",
        lede="one line, one photo. no lesson, no list. it's a vibe, and vibes get comments.",
        l1="i was staring the ceiling to get some idea",
        l2="i think need to stare more.",
        reactions=73, comments=14,
        also=("Hardest question to answer ‘Aap kartey kya ho?’", "45 reactions · 5 comments"),
        why=["it takes 2 seconds, so almost everyone finishes it",
             "the photo does half the work",
             "it reminds people you're a person, not a content machine"],
        watch="it's a breather, not a strategy. use it between your big posts, not instead of them.",
        tpl="[a real, slightly silly thing you're doing right now] / [one line joke about it]",
        turn="take one honest photo of where you're working today. write one line about it. post it before you overthink it.",
    ),
    dict(
        name=("the hot", "take"), chip="counter-narrative",
        lede="say the opposite of what everyone in your space keeps repeating. only if you actually believe it.",
        l1="ai will not make you rich",
        l2="at least in 2026",
        reactions=52, comments=1,
        why=["it argues with the feed, and that stops the scroll",
             "“at least in 2026” makes it a sharp claim, not a rant",
             "it tells people what you stand for"],
        watch="honest data: my hot takes got way fewer comments than my stories. people nod and scroll. use them to take a stand, not for reach.",
        tpl="[the popular belief in your space] will not [the promise everyone makes] / at least [the condition that makes you right]",
        turn="write down the advice in your industry you're most tired of hearing. now write, in one line, what you'd say instead.",
    ),
    dict(
        name=("the", "mirror"), chip="say what they're thinking",
        lede="describe their problem better than they could. they feel seen before they know what you're offering.",
        l1="you're posting daily, building daily, grinding daily",
        l2="and still can't tell if you're actually moving forward",
        reactions=45, comments=1,
        why=["daily, daily, daily is rhythm. you feel the tiredness",
             "it names the reader without saying “if you're a creator”",
             "the next line is “that was me”, so it turns into a story"],
        watch="my lowest one here, and i think i know why: the rest of the post read like advice. the mirror only works if you step into it too.",
        tpl="you're [doing X] daily, [doing Y] daily / and still [the frustration they won't say out loud]",
        turn="collect the exact words your people use when they complain. DMs, comments, calls. use their words in line 1, not yours.",
    ),
]

# real post screenshots (shots/) + LinkedIn activity ids, in HOOKS order
POSTS = [("flex", "7492671912431480832"), ("confession", "7489733638901612544"),
         ("receipt", "7492968750564995072"), ("howdidi", "7492304063196221440"),
         ("fakeout", "7490426197579988992"), ("withheld", "7484345582925402113"),
         ("backfire", "7507180059527593984"), ("oneliner", "7491211649865920512"),
         ("hottake", "7484851320336842752"), ("mirror", "7507837862533586944")]
ALSO_IDS = {5: "7500629649450823680", 8: "7499103732236935168"}  # hiring, aap kartey kya ho


def post_url(pid: str) -> str:
    return f"https://www.linkedin.com/feed/update/urn:li:activity:{pid}/"


STAR = """<svg class="{cls}" viewBox="0 0 200 200" aria-hidden="true">
<path d="M101 6 L126 70 L193 74 L139 119 L157 187 L99 147 L41 189 L61 117 L7 72 L75 69 Z" fill="#1B3CCB" stroke="#17150F" stroke-width="5" stroke-linejoin="round"/>
<circle cx="82" cy="97" r="14" fill="#FFFAF0" stroke="#17150F" stroke-width="4"/>
<circle cx="119" cy="94" r="14" fill="#FFFAF0" stroke="#17150F" stroke-width="4"/>
<circle cx="85" cy="100" r="6" fill="#17150F"/><circle cx="122" cy="97" r="6" fill="#17150F"/>
<ellipse cx="101" cy="126" rx="9" ry="7" fill="#17150F"/></svg>"""

FOOT = '<footer class="foot"><span>gaurav sharma · 10 hooks i actually posted</span><span>{n}</span></footer>'


SCREEN_TOP = """<div class="intro"><span class="fact hi">this guide is interactive</span>
<p>fill the <b>your turn</b> boxes, the worksheet and the checklist right here. it saves on this device only, nothing gets sent anywhere. then hit <b>download my pdf</b> to keep your own filled-in copy.</p></div>"""

SCREEN_UI = """<div class="bar"><button class="mine" type="button">download my pdf</button><a class="blankpdf" href="10-hooks-i-actually-posted.pdf" download>blank pdf</a></div>
<script src="app.js"></script>"""

DEBUG_JS = """<script>
document.fonts.ready.then(() => {
  const bad = [];
  document.querySelectorAll('.page').forEach((pg, i) => {
    const P = pg.getBoundingClientRect();
    const kids = [...pg.querySelectorAll('h1,h2,.lede,.post,.also,.cols,.why,.tpl,.turn,.rule,.data,.rows,.checklist,.leftout,.cta,.send,.say,.fine,.inside,.chips,.foot')];
    kids.forEach(k => { const r = k.getBoundingClientRect(); if (r.bottom > P.bottom - 30 || r.right > P.right - 40) bad.push(`p${i+1} ${k.className||k.tagName} overflows`); });
    for (let a = 0; a < kids.length; a++) for (let b = a+1; b < kids.length; b++) {
      const A = kids[a], B = kids[b]; if (A.contains(B) || B.contains(A)) continue;
      const r1 = A.getBoundingClientRect(), r2 = B.getBoundingClientRect();
      if (r1.left < r2.right && r2.left < r1.right && r1.top < r2.bottom - 4 && r2.top < r1.bottom - 4) bad.push(`p${i+1} ${A.className||A.tagName} x ${B.className||B.tagName}`);
    }
  });
  document.body.setAttribute('data-report', bad.join(' | ') || 'CLEAN');
});
</script>"""


def blanks(t: str) -> str:
    """[x] -> highlighted blank, ' / ' -> line break."""
    parts = re.split(r"(\[[^\]]*\])", t)
    out = []
    for part in parts:
        if part.startswith("["):
            words = part[1:-1].split(" ")
            # one highlight per word, so wrapped blanks look right in the browser PDF export too
            spans = "".join(f'<span class="bw">{w}{" " if k < len(words) - 1 else ""}</span>' for k, w in enumerate(words))
            out.append(f'<span class="blank">{spans}</span>')
        else:
            out.append(part.replace(" / ", "<br>"))
    return "".join(out)


def hook_page(i: int, h: dict) -> str:
    n = f"{i:02d}"
    shot, pid = POSTS[i - 1]
    why = "".join(f"<li>{w}</li>" for w in h["why"])
    also = ""
    if "also" in h:
        also = f'<div class="also"><span class="hand">also worked:</span> <a href="{post_url(ALSO_IDS[i])}">“{h["also"][0]}”</a> <span class="mute">{h["also"][1]}</span></div>'
    return f"""
<section class="page hook">
  <header class="top"><span class="eyebrow">hook {n} / 10</span></header>
  <div class="num">{n}</div>
  <span class="chip">{h["chip"]}</span>
  <h2>{h["name"][0]} <span class="mark">{h["name"][1]}</span></h2>
  <p class="lede">{h["lede"]}</p>

  <figure class="post card shot">
    <img src="shots/{shot}.png" alt="my linkedin post: {h["l1"]} {h["l2"]}">
    <figcaption class="stats">
      <span class="fact hi">{h["reactions"]} reactions</span><span class="fact">{h["comments"]} comment{"" if h["comments"] == 1 else "s"}</span>
      <a class="open" href="{post_url(pid)}">open the real post ↗</a>
    </figcaption>
  </figure>
  {also}

  <div class="cols">
    <div class="why">
      <h4 class="hand">why it works</h4>
      <ul>{why}</ul>
      <p class="watch"><b>watch out</b> {h["watch"]}</p>
    </div>
    <div class="tpl card">
      <h4 class="hand">steal the template</h4>
      <p>{blanks(h["tpl"])}</p>
    </div>
  </div>

  <div class="turn">
    <h4>your turn <span class="fact hi">5 min</span></h4>
    <p>{h["turn"]}</p>
    <div class="write"><div class="lines"><i></i><i></i></div><textarea class="field tfield" data-save="turn{n}" rows="2" placeholder="write it here…"></textarea></div>
  </div>
  {FOOT.format(n=i + 2)}
</section>"""


def build() -> str:
    css = (HERE / "style.css").read_text()
    inside = "".join(
        f'<li><span class="dot">{i}</span>{h["name"][0]} {h["name"][1]}</li>'
        for i, h in enumerate(HOOKS, 1)
    )

    cover = f"""
<section class="page cover">
  <div class="eyebrow">a free guide · gaurav sharma</div>
  {STAR.format(cls="star cover-star")}
  <div class="bubble hand">no pressure :)</div>
  <h1>10 hooks i <em>actually</em> posted</h1>
  <p class="lede big">not stolen from a viral thread. pulled from 29 of my own linkedin posts, ranked by what people actually reacted to. each one comes with a template to steal and a 5 minute task.</p>
  <div class="chips"><span class="fact hi">10 hooks</span><span class="fact">29 real posts</span><span class="fact">5 min each</span><span class="fact">zero “agree?” at the end</span></div>
  <div class="card inside">
    <h3>what's inside</h3>
    <p class="mute small">ranked by reactions, best first. yes, even the ones that flopped.</p>
    <ol>{inside}</ol>
  </div>
  <footer class="foot"><span>gaurav sharma · personal branding for B2B and D2C founders</span><span class="hand blue">made in delhi ncr</span></footer>
</section>"""

    rules = f"""
<section class="page rules">
  <div class="eyebrow">read this first</div>
  {STAR.format(cls="star rules-star")}
  <h2>your hook has <span class="mark">one job</span></h2>
  <p class="lede">make them read line two. not go viral, not sound smart. just line two.</p>

  <div class="rule card"><span class="dot big">1</span><div><h3>two lines, then a gap</h3>
    <p>line 1 is the tension, line 2 is the promise. keep it under ~15 words before “see more” cuts you off, and make line 1 fit on one phone line.</p></div></div>
  <div class="rule card"><span class="dot big">2</span><div><h3>who + problem + hold back</h3>
    <p>name who it's for, touch a problem they actually have, and don't hand over the answer in the hook.</p></div></div>
  <div class="rule card"><span class="dot big">3</span><div><h3>write 5, post 1</h3>
    <p>write the same hook 5 ways, each in a different style from this guide. post the one that makes <i>you</i> want to read the next line.</p></div></div>

  <div class="data">
    <div class="x">~3x</div>
    <div>
      <p><b>what my own data told me:</b> posts about my actual life got 105 to 175 reactions. my “here are 5 tips” posts got 36 to 52.</p>
      <p class="hand">(yes i checked. it hurt a little.)</p>
      <p>so every hook in here starts with something that happened to you. not “you should”.</p>
    </div>
  </div>
  {FOOT.format(n=2)}
</section>"""

    rows = "".join(
        f'<div class="row"><span class="chip">{s}</span>'
        f'<div class="wl"><span>line 1</span><input class="field wfield" data-save="w{k}a" placeholder="type here…"></div>'
        f'<div class="wl"><span>line 2</span><input class="field wfield" data-save="w{k}b"></div></div>'
        for k, s in enumerate( ["the confession", "the receipt", "the fake-out", "the withheld answer", "the mirror"])
    )
    worksheet = f"""
<section class="page sheet">
  <div class="eyebrow">your turn · 15 min</div>
  <h2>now you. <span class="mark">write 5.</span></h2>
  <p class="lede">pick the next post you're going to write. write its hook 5 ways, one style each. post the one that makes you want to read line two. fill it in on <a href="https://nowaygaurav.github.io/linkedin-hooks/">the web version</a> and download your own copy, or just print this and scribble.</p>
  <div class="card rows">{rows}</div>
  {FOOT.format(n=13)}
</section>"""

    checks = "".join(f"<li data-check='c{k}'><span class='box'></span><span>{c}</span></li>" for k, c in enumerate([
        "line 1 fits on one phone line",
        "under ~15 words before “see more”",
        "there's a real number, name or place in it",
        "i'd still stand by it if nobody reacted",
        "if i pasted it on a stranger's profile, it wouldn't make sense. <span class='mute'>(that's how you know it's yours)</span>",
    ]))
    check = f"""
<section class="page check">
  <div class="eyebrow">before you hit post</div>
  <h2>the 30 second <span class="mark">check</span></h2>
  <div class="card checklist"><ul>{checks}</ul></div>
  <p class="tick hand">all 5 ticked? post it. missing one? fix line 1, not the whole post.</p>

  <div class="leftout">
    <h3>the one i left out</h3>
    <p><b>fear hooks.</b> “if you don't use AI you'll be unemployable in 2 years.” they work. they also turn you into that guy.</p>
    <p>i'd rather be the guy who spent 1,15,643 in july and told you exactly where it went.</p>
  </div>
  {FOOT.format(n=14)}
</section>"""

    back = f"""
<section class="page back">
  {STAR.format(cls="star back-star")}
  <div class="eyebrow light">that's it. go post.</div>
  <h2>stuck on what your <span class="mark">story</span> even is?</h2>
  <p class="lede">hooks are easy once you know what you stand for. if you don't yet, i made a tiny thing for that.</p>
  <div class="card cta">
    <span class="chip">eight honest questions</span>
    <h3>why do you want a personal brand?</h3>
    <p>answer eight questions in your own words and walk away with one sentence you can actually post against. no sign up, no email, nothing saved.</p>
    <a class="btn" href="https://personal-branding-questionarrie.vercel.app/">take the 8 questions</a>
    <span class="url">personal-branding-questionarrie.vercel.app</span>
  </div>
  <p class="send">if this helped, send it to one friend who keeps saying <span class="hand">“i'll start posting from monday”</span></p>
  <p class="say">say hi on linkedin · <a href="https://www.linkedin.com/in/nowaygaurav/">linkedin.com/in/nowaygaurav</a></p>
  <p class="fine">the numbers are reactions and comments on 29 of my posts (#46 to #100 of my 365 day challenge), checked on 2026-09-23. small sample, real numbers. test your own, that's the whole point. hook types adapted from The LinkedIn Lab (Amney Mounir &amp; Karina), Episode 8.</p>
  <footer class="foot"><span>gaurav sharma · personal branding for B2B and D2C founders</span><span>15</span></footer>
</section>"""

    hooks = "".join(hook_page(i, h) for i, h in enumerate(HOOKS, 1))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>10 hooks i actually posted</title>
<meta name="description" content="10 linkedin hooks from my own posts, ranked by what people actually reacted to. each with a template to steal and a 5 minute task.">
<meta property="og:title" content="10 hooks i actually posted · gaurav sharma">
<meta property="og:description" content="10 linkedin hooks from my own posts, ranked by reactions. template + 5 minute task for each.">
<meta property="og:image" content="https://nowaygaurav.github.io/linkedin-hooks/cover.png">
<meta property="og:url" content="https://nowaygaurav.github.io/linkedin-hooks/">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Caveat:wght@600;700&family=Instrument+Sans:wght@400;500;600;700&display=block" rel="stylesheet">
<style>{css}</style></head>
<body>{SCREEN_TOP}{cover}{rules}{hooks}{worksheet}{check}{back}{SCREEN_UI}{DEBUG_JS if os.environ.get("DEBUG") else ""}</body></html>"""


SQUIG = ('<img class="squig" alt="" aria-hidden="true" src="data:image/svg+xml,'
         '%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 24%27 preserveAspectRatio=%27none%27%3E'
         '%3Cpath d=%27M4 16 C 60 6, 120 21, 180 11 S 262 7, 296 13%27 fill=%27none%27 stroke=%27%23FFC93D%27 '
         'stroke-width=%279%27 stroke-linecap=%27round%27/%3E%3C/svg%3E">')


def squiggles(html: str) -> str:
    """Hand-drawn marker underline as an <img> (html2canvas skips inline SVG, so the browser PDF export needs this)."""
    return re.sub(r'<span class="mark">(.*?)</span>', lambda m: f'<span class="mark">{m.group(1)}{SQUIG}</span>', html)


if __name__ == "__main__":
    (HERE / "index.html").write_text(squiggles(build()))
    print("wrote index.html")
