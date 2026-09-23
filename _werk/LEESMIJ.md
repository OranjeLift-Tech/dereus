# Read this before you touch this repo

Deeper detail is in `website/BOUWPLAN.md`. This is what you need before your first command.

## The one rule

**The generator is the source.** Pages in the repo root (`index.html`, `contact/index.html`, ...) are
build output; edit them by hand and the next build silently reverts your work. Commit 7fe41fb put the
team photo back on `/contact/` by editing `contact/index.html` but never touched
`_werk/blokken/formulier.py`. It survived only because nobody dared run a build, and repairing it cost
real time on 22-09-2026.

Put your change in `_werk/blokken/`, `_werk/paginas/`, `website/content/*.md` or `css/`, then `--droog`
and confirm the rendered HTML is what you wanted.

## Commands, and what they cost

| Command | Cost | Safe while others work |
|---|---|---|
| `python _werk/build.py --droog` | 0,37 s | **Always.** Renders everything, runs the guards, writes nothing, takes no lock. |
| `python _werk/build.py` | 0,11 s idle, 0,37 s full | Only when nobody has generator files open. Takes a lock. |
| `python _werk/build.py --alles` | 0,37 s | Same. Ignores the cache and rebuilds everything. |
| `python _werk/build.py --alleen /diensten/` | under 0,1 s | Same. One page plus the shared files. |
| `node _werk/controle.cjs` | ~45 s, one browser | Yes, with a caveat below. Writes screenshots to `website/review/cleanup/`. |
| `node _werk/controle.cjs vangnet` | ~3 s, no browser | Yes. Checks every `src`, `srcset` and `url()` resolves. Run it after any image cleanup. |
| `node _ai-beelden/gereedschap/ronde.mjs <ronde.json>` | ~27 s, one image or five | Yes. Writes only into its own round folder under `website/review/`. See `_ai-beelden/LEESMIJ.md`. |
| `python _werk/opruimen-beelden.py --lijst <file> --droog` | seconds | Yes. Shows what it would move. |

`opruimen-beelden.py` is new and still untracked; dereus-80 owns it and its flags may change, so read
its docstring before trusting a flag. No measured cost for `controle.cjs --snel` yet; ask dereus-80.

`--droog` ends with the list of files a real build would touch: your check before and after any source
change. `controle.cjs` takes named checks (`layout headers`), `--snel` for two widths instead of five,
`--serie` to run sequentially, `--basis <url>` to reuse a running server. **A red `controle.cjs` during
someone else's build is not a conclusion**: it measures files as they sit on disk, so a build or splice
in flight gives failures that are gone five seconds later.

## Running alongside other sessions

A real build is safe since 22-09-2026: a lock (`_werk/.build.lock`) carries your session name and a
second build exits 3 naming the holder, every file is written atomically, identical content is never
rewritten, and the build names any file changed outside it before overwriting. Read those warnings.

Still, a real build rewrites shared output. If a teammate has `navigatie.py`, `kit.py`, `css/style.css`
or any block open, their half finished work lands in every page. **Ask before a real build.**

**A scoped build does not keep the other pages honest, and this WILL bite a room full of sessions.**
`--alleen /diensten/` writes its own page plus the shared files. Shared CSS is one file, so a change
to `css/style.css` or a block's CSS reaches every page the moment anyone builds anything. Markup is
not: a change to a shared source (`kit.py`, `navigatie.py`, a block used on six pages) only reaches
the page that session built. Every other page keeps its old HTML until somebody builds it.

With several sessions on `--alleen` all day that drift accumulates, and it does not look like drift.
It looks like work being undone: the source is right, the CSS is right, the page still shows the old
thing.

**Measure the drift before you explain it with this.** On 23-09-2026 `--droog` named three stale
pages and that was taken as the explanation for a "my work was reverted" report. It was not. Built
to a mirror and diffed, `index.html` was already identical and the other two differed only in the
`?v=` cache-busting hash on one stylesheet link, which changes nothing a visitor sees because the
path is the same file. The mechanism above is real, the instance was not. `--droog` tells you *which*
files a build would touch; it does not tell you *what* would change, and those are different
questions. Render to the mirror below and diff before you draw a conclusion from a file count.

**The fix is one full `python _werk/build.py`.** Before you run it, ask every session that is in a
shared source whether it is clean, because a full build publishes whatever is on disk at that moment
to all twelve pages. `--droog` first: it names the pages a real build would change, and prints a
`!!` line for every output that was edited outside the build, which is the only thing a full build
can actually destroy.

**The build cache is only written by a full build** (`cache_schrijven` runs when
`volledige_build = not alleen and not concept`). So a day of scoped builds leaves
`_werk/.bouwcache.json` pointing at the last full build. That is mostly harmless, `cache_actueel`
then reports "de invoer is veranderd" and rebuilds rather than skipping, but it does mean the cache
is no evidence of what is on disk, and the "changed outside the build" warning cannot see anything a
scoped build has written since.

**To see your own change while others work,** point `schrijf()` at a mirror in your scratchpad and
serve that. No lock, no real build, nothing written to the repo:

```python
import sys; sys.path.insert(0, "_werk"); import build
def naar_spiegel(doel, tekst):
    p = SPIEGEL / doel.resolve().relative_to(build.WORTEL)          # SPIEGEL = your scratchpad
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(tekst, encoding="utf-8"); return True
build.schrijf, build.DROOG = naar_spiegel, True   # DROOG keeps kopieer_merk() off the repo
build.bouw(alles=True)
```

The mirror gets the pages and `css/min`; serve it with a handler falling back to the repo root for
`js`, `img` and `fonts`, or copy those across (13 MB). Keep the same folder layout, because pages link
`/css/` and `/img/` absolutely, and never `rmtree` a mirror while a server still holds it on Windows.
Use port 8012 or higher, never `build.py --serve`; 8000 is the coordinator's.

**Check that your server actually bound before you believe a screenshot.** 8012 is what this file has
recommended all day, so on a busy day several sessions reach for it and only the first one gets it.
On 23-09-2026 that cost a session a full measurement round: its server never bound, it screenshotted
somebody else's mirror on the same port, and concluded its own image had not rendered. The
`EADDRINUSE` was in the log the whole time. Pick a free port, and fail loudly if the bind fails
rather than carrying on to the browser.
Playwright lives outside this repo at `C:/users/arnas/git_repos/tandartsvanschiedam/node_modules/playwright`
(`{channel:'msedge', headless:true}`); `controle-kit.cjs` finds it by itself.

## Traps that actually bit us

- **A filename grep cannot find is not evidence of anything.** Image paths go indirect five ways here:
  f-strings in blocks (`f"/img/kaart-{slug}.svg"`, so `kaart-delft.svg` is in no file yet eleven maps
  need it); a json manifest that is a build input (`img/headers/manifest.json`, read by `kit.py:258`,
  which looks like an asset because it sits in `img/`); tables where the label is not the filename
  (`treden.py:19` loads `stoel-rechts.webp` while `stoel.webp` is the dead one); `beeld:` lines in
  `website/content/*.md`; and branches behind a config switch (`over-foto-achter.webp` renders only
  when `FEITEN['TEAM_BEELD']` is empty). **Prove an image is unused by reading the block that would
  load it, not by searching for its name.** `_werk/beeldpaden.py` does this; a text search does not.
- **Browser profiles belong in the system temp folder, never in the repo.** Start a browser and you
  pass a `userDataDir` under `os.tmpdir()`. `controle-kit.cjs` will do this for you once dereus-80's
  fix lands; until then check it yourself, because a leftover `_prof-*` folder in the repo is a bug.
  Three are sitting in `website/review/_archief/hero-fold/` now (2797 files, 170,8 MB); clearing them
  goes through `opruimen-beelden.py` with `--mappen --groep browserprofielen`.
- **Do not run `build.py` to "see if it works".** Use `--droog`. A real build is a shared side effect.
- **`data-reveal` falsifies MEASUREMENTS too, not just screenshots.** The reveal is a transform, so
  a block caught mid-animation reports a position that is off by however far it still has to travel.
  Measuring the vragen block 800 ms after scrolling it into view gave `translateY(14.99px)` and made
  a card look 15 px out of line with the column beside it; it was already aligned to the pixel. Wait
  until the transform is back at zero before you read any coordinate off that block:
  `page.waitForFunction(() => Math.abs(new DOMMatrixReadOnly(getComputedStyle(el).transform).m42) < 0.5)`.
  A fixed `waitForTimeout` is a guess and will bite you on a slower run.
- **A screenshot of a section can lie about what is in it.** Two things hide content from an element
  screenshot that a visitor never misses. `.vragen__lijst` carries `data-reveal`, so the questions sit
  at opacity 0 until the block is scrolled into view, and any `loading="lazy"` image below the fold
  never starts loading at all. Shoot a section without scrolling to it and you photograph an empty
  right column and a hole where the figure belongs, then go hunting for a layout bug that is not
  there. Scroll the block into view, wait, and wait for the images, with a timeout on that wait: a
  lazy image that stays out of view never fires `load` and will hang the run forever.
- **`build.py` takes `--alleen <pad>`, and the path has slashes.** `python _werk/build.py werkwijze`
  ignores the bare word and quietly builds all twelve pages; `--alleen werkwijze` matches nothing and
  builds none. It is `--alleen /werkwijze/`. Check the "Klaar: N pagina's" line: if N is not what you
  meant, you did not build what you meant.

## Parallel rounds

- A session owns the files it was given. You do not edit another session's files, you report back.
- Before touching a shared file (`formulier.py`, `navigatie.py`, `css/style.css`), ask who is in it and
  say which lines you need. That one message costs less than a merge.
- **The header, drawer, footer and call bar are in `_werk/navigatie.py`, not in `_werk/blokken/`.**
  Looking for the footer among the blocks is a dead end and has cost time.
- Find something outside your task? Report it, do not fix it. Deliver exactly what was asked; if you
  think the task is wrong, say so in a line, then deliver.
- **Measure before you build machinery.** Everyone hand spliced pages because a build was assumed to be
  slow. It took 0,30 seconds. The problem was safety, not speed.
