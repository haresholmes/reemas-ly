#!/usr/bin/env python3
"""Redraw the weak marks in logo-lab/assets and embed the brand fonts.

Usage: python3 refine_logos.py <assets dir> <fonts dir>

Each logo SVG has the same shape: a <defs> block with the shared gold
gradients, the mark (centred on 200,150), then three <text> lines. This
script replaces only the mark of the concepts listed in MARKS, and then
embeds a subset of IBM Plex Sans Arabic SemiBold and Jost (500/600) in
every file, because an SVG shown through <img> cannot load web fonts.
"""
import base64, io, math, os, re, sys

ASSETS, FONTS = sys.argv[1], sys.argv[2]
uid = [0]


def nid(p):
    uid[0] += 1
    return f"{p}{uid[0]}"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def pts(ps):
    return " ".join(f"{f(x)},{f(y)}" for x, y in ps)


def poly_d(ps, closed=False):
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in ps)
    return d + (" Z" if closed else "")


def grad(gid, x1=-70, y1=-70, x2=70, y2=70):
    """Gold gradient in the mark's own coordinates (works on straight lines)."""
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            '<stop offset="0" stop-color="#FFF0B8"/><stop offset="0.35" stop-color="#E5C058"/>'
            '<stop offset="0.72" stop-color="#B58525"/><stop offset="1" stop-color="#ECCF78"/></linearGradient>')


def sparkle(cx, cy, r, light="#FFF9D6", dark="#E5C058"):
    """Small brilliant: a rhombus split into a lit and a shaded half."""
    return (f'<polygon points="{pts([(cx, cy - r), (cx + r * .72, cy), (cx, cy + r), (cx - r * .72, cy)])}" fill="{light}"/>'
            f'<polygon points="{pts([(cx, cy - r), (cx, cy + r), (cx - r * .72, cy)])}" fill="{dark}" opacity="0.55"/>')


# ---------------------------------------------------------------- weaving
def seg_inter(p, q, r, s):
    d = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
    if abs(d) < 1e-9:
        return None
    t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / d
    u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / d
    if 0 <= t < 1 and 0 <= u < 1:
        return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])), t, u
    return None


def crossings(strands):
    """All crossings: (point, strand a, pos along a, strand b, pos along b)."""
    out = []
    for a in range(len(strands)):
        for b in range(a, len(strands)):
            A, B = strands[a]["p"], strands[b]["p"]
            for i in range(len(A) - 1):
                for j in range(len(B) - 1):
                    if a == b and abs(i - j) < 3:
                        continue
                    if a == b and j < i:
                        continue
                    hit = seg_inter(A[i], A[i + 1], B[j], B[j + 1])
                    if hit:
                        pt, t, u = hit
                        if any(math.dist(pt, c[0]) < 1.5 for c in out):
                            continue
                        out.append((pt, a, i + t, b, j + u))
    return out


def weave(strands, gap=3.2, over=None, draw_order=None):
    """Draw strands so that at every crossing one passes visibly under the other.

    strands: list of {"p": [(x,y)...], "w": width, "stroke": paint, "closed": bool}
    over: list of booleans, one per crossing in crossings() order: True means the
          first strand of the pair is on top. Default: alternate along the path.
    """
    cs = crossings(strands)
    if over is None:
        # alternate over/under along the traversal of all strands in order
        events = []
        for k, (pt, a, ta, b, tb) in enumerate(cs):
            events.append((a, ta, k, 0))
            events.append((b, tb, k, 1))
        events.sort()
        state, over = {}, [None] * len(cs)
        flip = True
        for s, t, k, side in events:
            if over[k] is None:
                over[k] = flip if side == 0 else not flip
            flip = not flip
    defs, body = [], []
    masks = {i: [] for i in range(len(strands))}
    for k, (pt, a, ta, b, tb) in enumerate(cs):
        top, under = (a, b) if over[k] else (b, a)
        tpos = ta if top == a else tb
        if a == b:
            tpos = ta if over[k] else tb
        masks[under].append((pt, top, tpos))
    for i, s in enumerate(strands):
        d = poly_d(s["p"], s.get("closed"))
        attrs = f'fill="none" stroke="{s["stroke"]}" stroke-width="{s["w"]}" stroke-linecap="{s.get("cap", "round")}" stroke-linejoin="round"'
        if masks[i]:
            mid = nid("wm")
            parts = []
            for pt, top, tpos in masks[i]:
                cid = nid("wc")
                rad = (strands[top]["w"] + s["w"]) * 1.6 + gap
                defs.append(f'<clipPath id="{cid}"><circle cx="{f(pt[0])}" cy="{f(pt[1])}" r="{f(rad)}"/></clipPath>')
                tp = strands[top]["p"]; c0 = int(tpos)
                td = poly_d(tp[max(0, c0 - 12):c0 + 14])
                parts.append(f'<path d="{td}" fill="none" stroke="#000" stroke-width="{f(strands[top]["w"] + 2 * gap)}" clip-path="url(#{cid})"/>')
            defs.append(f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="400" height="400">'
                        f'<rect x="-200" y="-200" width="400" height="400" fill="#fff"/>{"".join(parts)}</mask>')
            body.append((i, f'<path d="{d}" {attrs} mask="url(#{mid})"/>'))
        else:
            body.append((i, f'<path d="{d}" {attrs}/>'))
    order = draw_order or range(len(strands))
    by = dict(body)
    extra = ""
    for k, (pt, a, ta, b, tb) in enumerate(cs):
        if a == b:  # self-crossing: put the over pass back on top of its own gap
            pos = ta if over[k] else tb; s = strands[a]; c0 = int(pos)
            extra += (f'<path d="{poly_d(s["p"][max(0, c0 - 8):c0 + 10])}" fill="none" stroke="{s["stroke"]}" '
                      f'stroke-width="{s["w"]}" stroke-linecap="butt"/>')
    return "".join(defs), "".join(by[i] for i in order) + extra, cs


def sample(fn, t0, t1, n):
    return [fn(t0 + (t1 - t0) * k / n) for k in range(n + 1)]


def bez(p0, p1, p2, p3, n=40):
    out = []
    for k in range(n + 1):
        t = k / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def chain(*segs):
    out = []
    for s in segs:
        out.extend(s if not out else s[1:])
    return out


# ---------------------------------------------------------------- marks
def mark04():  # The Infinite Gold Link: woven lemniscate
    g = nid("g")
    a = 80
    lem = sample(lambda t: (a * math.cos(t) / (1 + math.sin(t) ** 2),
                            1.35 * a * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2)), 0, 2 * math.pi, 360)
    d, b, cs = weave([{"p": lem, "w": 9, "stroke": f"url(#{g})", "closed": True}], gap=3.5, over=[True])
    return (f'<g transform="translate(200,158)"><defs>{grad(g, -80, -40, 80, 40)}{d}</defs>{b}'
            f'{sparkle(0, -56, 9)}</g>')


def mark07():  # Continuous Line Art: one unbroken stroke draws a brilliant cut
    g = nid("g")
    V = {"T1": (-30, -40), "M": (0, -40), "T3": (30, -40), "A": (-58, -12), "B": (-20, -12),
         "D": (20, -12), "E": (58, -12), "C": (0, 60)}
    edges = [("A", "T1"), ("T1", "M"), ("M", "T3"), ("T3", "E"), ("M", "B"), ("M", "D"), ("A", "B"),
             ("B", "D"), ("D", "E"), ("A", "C"), ("B", "C"), ("D", "C"), ("E", "C")]
    adj = {k: [] for k in V}
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i)); adj[v].append((u, i))
    used, stack, path = set(), ["A"], []
    while stack:  # Hierholzer: every edge exactly once, A to E
        u = stack[-1]
        nxt = next(((v, i) for v, i in adj[u] if i not in used), None)
        if nxt:
            used.add(nxt[1]); stack.append(nxt[0])
        else:
            path.append(stack.pop())
    path.reverse()
    assert len(path) == len(edges) + 1 and {path[0], path[-1]} == {"A", "E"}
    walk = " L".join(f"{V[k][0]},{V[k][1]}" for k in path)
    sx = -1 if path[0] == "A" else 1
    return (f'<g transform="translate(200,146)"><defs>{grad(g)}</defs>'
            f'<path d="M{sx * 86},-12 L{walk} L{-sx * 86},-12" fill="none" stroke="url(#{g})" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{sx * 86}" cy="-12" r="2.6" fill="#E5C058"/>{sparkle(-sx * 92, -12, 6)}</g>')


def mark09():  # Divine Golden Ratio: true Fibonacci construction
    g = nid("g")
    fib = [1, 1, 2, 3, 5, 8, 13, 21]
    sq = [(0, 0, 1, None)]  # x, y, side, bounding box before this square (y down)
    x0, y0, x1, y1 = 0, 0, 1, 1
    dirs = ["R", "D", "L", "U"]
    for k, s in enumerate(fib[1:]):
        dr, old = dirs[k % 4], (x0, y0, x1, y1)
        if dr == "R": sq.append((x1, y0, s, old)); x1 += s
        if dr == "D": sq.append((x0, y1, s, old)); y1 += s
        if dr == "L": sq.append((x0 - s, y0, s, old)); x0 -= s
        if dr == "U": sq.append((x0, y0 - s, s, old)); y0 -= s
    # quarter arcs: centre is the corner on the edge shared with the old rectangle
    P, arcs = (0, 1), []
    for (x, y, s, old) in sq:
        cs = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
        if old is None:
            C, E = (0, 0), (1, 0)
        else:
            on_old = lambda c: old[0] <= c[0] <= old[2] and old[1] <= c[1] <= old[3]
            C = next(c for c in cs if c != P and on_old(c))
            E = next(c for c in cs if c != P and c != C and abs(math.dist(c, C) - s) < 1e-9)
        arcs.append((P, C, E, s))
        P = E
    W, H = x1 - x0, y1 - y0
    sc = 150 / max(W, H)
    T = lambda p: ((p[0] - (x0 + W / 2)) * sc, (p[1] - (y0 + H / 2)) * sc)
    grid = "".join(f'<rect x="{f(T((x, y))[0])}" y="{f(T((x, y))[1])}" width="{f(s * sc)}" height="{f(s * sc)}"/>' for x, y, s, _ in sq)
    d = ""
    for P0, C, E, s in arcs:
        a0 = math.atan2(P0[1] - C[1], P0[0] - C[0]); a1 = math.atan2(E[1] - C[1], E[0] - C[0])
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        sweep = 1 if da > 0 else 0
        p, e = T(P0), T(E)
        d += (f"M{f(p[0])},{f(p[1])}" if not d else "") + f" A{f(s * sc)},{f(s * sc)} 0 0 {sweep} {f(e[0])},{f(e[1])}"
    st = T(arcs[0][0])
    return (f'<g transform="translate(200,150)"><defs>{grad(g, -75, -46, 75, 46)}</defs>'
            f'<g fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.32">{grid}</g>'
            f'<path d="{d}" fill="none" stroke="url(#{g})" stroke-width="4.2" stroke-linecap="round"/>'
            f'{sparkle(st[0], st[1], 6.5)}</g>')


def mark13():  # Precision Assay Scales
    g, gv = nid("g"), nid("g")
    pans = ""
    for sx in (-1, 1):
        cx = 56 * sx
        pans += (f'<path d="M{cx},-36 L{cx - 21},8 M{cx},-36 L{cx + 21},8" stroke="url(#{g})" stroke-width="1.4" fill="none"/>'
                 f'<path d="M{cx - 25},8 Q{cx},30 {cx + 25},8 Z" fill="url(#{gv})"/>'
                 f'<circle cx="{cx}" cy="-36" r="2.6" fill="#E5C058"/>'
                 f'{sparkle(cx, -1, 7.5)}')
    return (f'<g transform="translate(200,146)"><defs>{grad(g)}'
            f'<linearGradient id="{gv}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FDE08A"/><stop offset="1" stop-color="#A37A20"/></linearGradient></defs>'
            f'<rect x="-3" y="-38" width="6" height="96" fill="url(#{gv})"/>'
            f'<path d="M-62,-40 Q0,-48 62,-40 L62,-35 Q0,-43 -62,-35 Z" fill="url(#{g})"/>'
            f'<path d="M-30,72 L30,72 L22,62 L-22,62 Z" fill="url(#{g})"/>'
            f'<rect x="-40" y="73.5" width="80" height="3" rx="1.5" fill="#B58525"/>'
            f'{pans}{sparkle(0, -56, 10)}</g>')


def mark16():  # Eternal Bond Rings, now properly interlocked
    g = nid("g")
    def ell(cx, ang):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        return sample(lambda t: (cx + 34 * math.cos(t) * c - 48 * math.sin(t) * s,
                                 34 * math.cos(t) * s + 48 * math.sin(t) * c), 0, 2 * math.pi, 240)
    d, b, cs = weave([{"p": ell(-17, -18), "w": 5, "stroke": f"url(#{g})", "closed": True},
                      {"p": ell(17, 18), "w": 5, "stroke": f"url(#{g})", "closed": True}], gap=3)
    return f'<g transform="translate(200,150)"><defs>{grad(g, -60, -55, 60, 55)}{d}</defs>{b}</g>'


def mark19():  # Fine Milligram Quill
    g, m = nid("g"), nid("m")
    vane = ("M0,-80 C30,-56 34,-6 10,40 L0,50 L-8,40 C-26,-4 -22,-54 0,-80 Z")
    slits = ""
    for k, y in enumerate(range(-46, 34, 13)):
        slits += f'<path d="M1,{y} L34,{y - 20}" /><path d="M-1,{y + 6} L-28,{y - 12}"/>'
    return (f'<g transform="translate(206,150) rotate(-28)"><defs>{grad(g, -30, -80, 30, 80)}'
            f'<mask id="{m}" maskUnits="userSpaceOnUse" x="-100" y="-100" width="200" height="200"><rect x="-100" y="-100" width="200" height="200" fill="#fff"/>'
            f'<g stroke="#000" stroke-width="2.2" stroke-linecap="round">{slits}</g>'
            f'<path d="M0,-70 L0,46" stroke="#000" stroke-width="2.4"/>'
            f'<path d="M-30,6 L-14,-4" stroke="#000" stroke-width="5"/></mask></defs>'
            f'<path d="{vane}" fill="url(#{g})" mask="url(#{m})"/>'
            f'<path d="M0,-66 L0,70" stroke="#FFF0B8" stroke-width="1.3"/>'
            f'<path d="M-2.4,48 L0,70 L2.4,48 Z" fill="#E5C058"/>'
            f'{sparkle(0, 79, 7)}</g>')


def mark24():  # Trilliant Ingot: three trapezoid ingots, each laid over the next
    n, u = 5, 27.0
    def L(i, j):  # lattice (i along the base, j up the left side) to mark coordinates, centred
        ci, cj = n / 3, n / 3
        return ((i - ci + (j - cj) / 2) * u, -(j - cj) * math.sqrt(3) / 2 * u + 6)
    base = [(0, 0), (4, 0), (3, 1), (0, 1)]  # one ingot; the next one covers its far end
    def rot(p, k):
        i, j = p
        for _ in range(k):
            i, j = n - i - j, i
        return (i, j)
    fills = ["url(#P24a)", "url(#P24b)", "url(#P24c)"]
    polys = "".join(f'<polygon points="{pts([L(*rot(p, k)) for p in base])}" fill="{fills[k]}"/>' for k in range(3))
    return ('<g transform="translate(200,150)"><defs>'
            '<linearGradient id="P24a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF0B8"/><stop offset="1" stop-color="#D9AE45"/></linearGradient>'
            '<linearGradient id="P24b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C99A35"/><stop offset="1" stop-color="#8A6418"/></linearGradient>'
            '<linearGradient id="P24c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E5C058"/><stop offset="1" stop-color="#A37A20"/></linearGradient></defs>'
            f'{polys}{sparkle(0, 6, 9)}</g>')


def mark25():  # Haute Joaillerie Diadem
    g, gf = nid("g"), nid("g")
    crown = ("M-64,34 C-60,14 -48,6 -38,-10 C-32,2 -24,8 -14,6 C-8,-4 -4,-22 0,-40 "
             "C4,-22 8,-4 14,6 C24,8 32,2 38,-10 C48,6 60,14 64,34")
    band = "M-64,34 Q0,52 64,34"
    dots = "".join(f'<circle cx="{f(x)}" cy="{f(28 + 0.0040 * (64 ** 2 - x * x) * 1.6 / 1.6 * 0.95)}" r="1.9" fill="#FFF0B8"/>'
                   for x in (-40, -20, 0, 20, 40))
    return (f'<g transform="translate(200,150)"><defs>{grad(g, -64, -40, 64, 44)}'
            f'<linearGradient id="{gf}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5C058" stop-opacity="0.22"/><stop offset="1" stop-color="#E5C058" stop-opacity="0.04"/></linearGradient></defs>'
            f'<path d="{crown}" fill="none" stroke="url(#{g})" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{band}" fill="none" stroke="url(#{g})" stroke-width="3.4" stroke-linecap="round"/>'
            f'<path d="M-56,24 Q0,40 56,24" fill="none" stroke="url(#{g})" stroke-width="1.3" opacity="0.8"/>'
            f'{dots}<circle cx="-38" cy="-17" r="3.4" fill="#FFF0B8"/><circle cx="38" cy="-17" r="3.4" fill="#FFF0B8"/>'
            f'{sparkle(0, -54, 11)}</g>')


def baguette(x, y, w, h):
    inset = 3.2
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="1.2" fill="url(#BAGG)"/>'
            f'<rect x="{f(x + inset)}" y="{f(y + inset)}" width="{f(w - 2 * inset)}" height="{f(h - 2 * inset)}" fill="#FFF0B8" opacity="0.28"/>')


def mark27():  # Art Deco Baguette Monogram
    g = nid("g")
    s = ""
    s += baguette(-44, -66, 14, 62)   # stem, upper stone
    s += baguette(-44, 4, 14, 62)     # stem, lower stone
    s += baguette(-24, -66, 44, 14)   # bowl, top
    s += baguette(26, -66, 14, 14)    # bowl, upper corner
    s += baguette(26, -46, 14, 32)    # bowl, right
    s += baguette(26, -8, 14, 14)     # bowl, lower corner
    s += baguette(-24, -8, 44, 14)    # bowl, middle
    # leg: a baguette laid on the diagonal from the bowl to the baseline
    p0, p1 = (6, 15), (38, 66)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; ln = math.hypot(dx, dy)
    nx, ny = -dy / ln * 7, dx / ln * 7
    leg = [(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)]
    ix, iy = nx * 0.54, ny * 0.54
    ux, uy = dx / ln * 3.2, dy / ln * 3.2
    inner = [(p0[0] + ix + ux, p0[1] + iy + uy), (p1[0] + ix - ux, p1[1] + iy - uy), (p1[0] - ix - ux, p1[1] - iy - uy), (p0[0] - ix + ux, p0[1] - iy + uy)]
    s += f'<polygon points="{pts(leg)}" fill="url(#BAGG)"/><polygon points="{pts(inner)}" fill="#FFF0B8" opacity="0.28"/>'
    s = s.replace("BAGG", g)
    return (f'<g transform="translate(200,150)"><defs>{grad(g, -44, -66, 40, 66)}</defs>{s}'
            f'{sparkle(-2, -30, 9)}</g>')


def mark29():  # Celestial Orbit Solitaire
    g, gr = nid("g"), nid("g")
    th = math.radians(-20)
    ring = sample(lambda t: (74 * math.cos(t) * math.cos(th) - 24 * math.sin(t) * math.sin(th),
                             74 * math.cos(t) * math.sin(th) + 24 * math.sin(t) * math.cos(th)), 0, 2 * math.pi, 300)
    axis = [(0, -72), (0, 72)]
    d, b, cs = weave([{"p": ring, "w": 5, "stroke": f"url(#{g})", "closed": True},
                      {"p": axis, "w": 2.2, "stroke": f"url(#{g})", "cap": "round"}], gap=3,
                     over=None)
    # front crossing (y>0): ring on top; back crossing (y<0): axis on top
    over = [c[0][1] > 0 for c in cs]
    d, b, cs = weave([{"p": ring, "w": 5, "stroke": f"url(#{g})", "closed": True},
                      {"p": axis, "w": 2.2, "stroke": f"url(#{g})", "cap": "round"}], gap=3, over=over)
    t = math.radians(28)
    px = 74 * math.cos(t) * math.cos(th) - 24 * math.sin(t) * math.sin(th)
    py = 74 * math.cos(t) * math.sin(th) + 24 * math.sin(t) * math.cos(th)
    h = 11
    princess = (f'<g transform="translate({f(px)},{f(py)}) rotate(-20)">'
                f'<polygon points="{-h},{-h} {h},{-h} 0,0" fill="#FFF9D6"/><polygon points="{h},{-h} {h},{h} 0,0" fill="#ECCF78"/>'
                f'<polygon points="{h},{h} {-h},{h} 0,0" fill="#B58525"/><polygon points="{-h},{h} {-h},{-h} 0,0" fill="#E5C058"/></g>')
    return (f'<g transform="translate(200,150)"><defs>{grad(g, -74, -40, 74, 40)}'
            f'<radialGradient id="{gr}" cx="0.35" cy="0.35" r="0.75"><stop offset="0" stop-color="#FFF0B8"/><stop offset="1" stop-color="#A37A20"/></radialGradient>{d}</defs>'
            f'<circle cx="0" cy="0" r="9" fill="url(#{gr})"/>{b}{princess}'
            f'<circle cx="0" cy="-76" r="2.6" fill="#E5C058"/><circle cx="0" cy="76" r="2.6" fill="#E5C058"/></g>')


def mark31():  # The Knot of Hercules: a flat reef knot, two bights each holding the other
    g = nid("g")
    Lp = chain(bez((-74, -36), (-58, -34), (-50, -20), (-34, -20)),
               bez((-34, -20), (-10, -20), (6, -20), (14, -20)),
               sample(lambda t: (14 + 13 * math.cos(t), -7 + 13 * math.sin(t)), -math.pi / 2, math.pi / 2, 40),
               bez((14, 6), (6, 6), (-10, 6), (-34, 6)),
               bez((-34, 6), (-50, 6), (-58, 18), (-74, 24)))
    Rp = [(-x, -y) for x, y in Lp]
    d, b, cs = weave([{"p": Lp, "w": 7, "stroke": f"url(#{g})"},
                      {"p": Rp, "w": 7, "stroke": f"url(#{g})"}], gap=3)
    over = [c[0][0] < 0 for c in cs]
    d, b, cs = weave([{"p": Lp, "w": 7, "stroke": f"url(#{g})"},
                      {"p": Rp, "w": 7, "stroke": f"url(#{g})"}], gap=3, over=over)
    return f'<g transform="translate(200,150) scale(1.12)"><defs>{grad(g, -74, -36, 74, 36)}{d}</defs>{b}{sparkle(0, 0, 6.5)}</g>', cs


def mark32():  # Leptis Column & Emerald Gem
    g, gv = nid("g"), nid("g")
    flutes = "".join(f'<rect x="{f(-20 + k * 8.5)}" y="-16" width="6" height="58" fill="url(#{gv})"/>' for k in range(5))
    ow, oh, c = 42, 28, 9
    oct_ = lambda w, h, c: [(-w / 2 + c, -h / 2), (w / 2 - c, -h / 2), (w / 2, -h / 2 + c), (w / 2, h / 2 - c),
                            (w / 2 - c, h / 2), (-w / 2 + c, h / 2), (-w / 2, h / 2 - c), (-w / 2, -h / 2 + c)]
    outer = oct_(ow, oh, c); inner = oct_(22, 12, 4)
    sh = lambda ps, dy: [(x, y + dy) for x, y in ps]
    gem = (f'<polygon points="{pts(sh(outer, -52))}" fill="url(#{g})"/>'
           f'<polygon points="{pts(sh(inner, -52))}" fill="#FFF9D6"/>'
           + "".join(f'<line x1="{f(o[0])}" y1="{f(o[1] - 52)}" x2="{f(i[0])}" y2="{f(i[1] - 52)}" stroke="#8A6418" stroke-width="0.9"/>'
                     for o, i in zip(outer, inner)))
    return (f'<g transform="translate(200,150)"><defs>{grad(g, -40, -70, 40, 70)}'
            f'<linearGradient id="{gv}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FDE08A"/><stop offset="1" stop-color="#A37A20"/></linearGradient></defs>'
            f'{gem}'
            f'<rect x="-36" y="-32" width="72" height="7" rx="1" fill="url(#{g})"/>'
            f'<path d="M-30,-24 L30,-24 L23,-17 L-23,-17 Z" fill="#B58525"/>'
            f'<circle cx="-36" cy="-24" r="4.5" fill="none" stroke="url(#{g})" stroke-width="2"/>'
            f'<circle cx="36" cy="-24" r="4.5" fill="none" stroke="url(#{g})" stroke-width="2"/>'
            f'{flutes}'
            f'<rect x="-26" y="43" width="52" height="6" rx="3" fill="url(#{g})"/>'
            f'<rect x="-32" y="51" width="64" height="7" fill="url(#{g})"/>'
            f'<rect x="-42" y="60" width="84" height="5" fill="#B58525"/></g>')


def mark33():  # Bespoke AR ligature: R whose leg is the sweep of the Arabic ra
    g = nid("g")
    return (f'<g transform="translate(192,146)"><defs>{grad(g, -40, -60, 40, 76)}</defs>'
            f'<path d="M-28,52 L-28,-58 L0,-58 C22,-58 32,-46 32,-31 C32,-16 22,-5 0,-5 L-28,-5" '
            f'fill="none" stroke="url(#{g})" stroke-width="9" stroke-linejoin="round" stroke-linecap="butt"/>'
            f'<path d="M-6,-9.5 C14,-6 26,12 32,32 C37,48 44,62 58,70 L55,74 C36,68 24,54 18,38 C12,22 6,8 -6,-0.5 Z" fill="url(#{g})"/>'
            f'{sparkle(1, -31, 8)}</g>')


def mark36():  # Nautilus Golden Spiral
    g = nid("g")
    b = 0.19
    t0, t1 = -1.6 * math.pi, 2.15 * math.pi
    R = lambda t: math.exp(b * t)
    P = lambda t, k=1.0: (k * R(t) * math.cos(t), k * R(t) * math.sin(t))
    spiral = sample(P, t0, t1, 400)
    end_in = P(t1 - 2 * math.pi)
    xs = [p[0] for p in spiral]; ys = [p[1] for p in spiral]
    sc = 140 / max(max(xs) - min(xs), max(ys) - min(ys))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    T = lambda p: ((p[0] - cx) * sc, (p[1] - cy) * sc)
    sp = [T(p) for p in spiral]
    septa = ""
    for k in range(6):
        t = t1 - 0.45 - k * 0.62
        a, c = T(P(t)), T(P(t - 2 * math.pi))
        mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
        ctr = T((0, 0))
        q = (mx + (mx - ctr[0]) * 0.18, my + (my - ctr[1]) * 0.18)
        septa += f'<path d="M{f(a[0])},{f(a[1])} Q{f(q[0])},{f(q[1])} {f(c[0])},{f(c[1])}"/>'
    e1, e2 = T(spiral[-1]), T(end_in)
    core = T((0, 0))
    return (f'<g transform="translate(200,150)"><defs>{grad(g, -70, -70, 70, 70)}</defs>'
            f'<path d="{poly_d(sp)} Q{f((e1[0] + e2[0]) / 2 + 6)},{f((e1[1] + e2[1]) / 2 + 6)} {f(e2[0])},{f(e2[1])}" fill="none" stroke="url(#{g})" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<g fill="none" stroke="url(#{g})" stroke-width="1.6" opacity="0.85">{septa}</g>'
            f'{sparkle(core[0], core[1], 6)}</g>')


MARKS = {
    "04": mark04, "07": mark07, "09": mark09, "13": mark13, "16": mark16, "19": mark19,
    "25": mark25, "27": mark27, "29": mark29, "31": lambda: mark31()[0], "32": mark32, "24": mark24,
    "33": mark33, "36": mark36,
}


# ---------------------------------------------------------------- fonts
def font_css(text_ar, text_en):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    css = ""
    ar = TTFont(os.path.join(FONTS, "IBMPlexSansArabic-SemiBold.ttf"))
    jobs = [(ar, "IBM Plex Sans Arabic", 600, text_ar)]
    for w in (500, 600):
        jv = TTFont(os.path.join(FONTS, "Jost%5Bwght%5D.ttf"))
        jobs.append((instancer.instantiateVariableFont(jv, {"wght": w}), "Jost", w, text_en))
    for font, fam, w, txt in jobs:
        opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["*"]; opts.name_IDs = []
        opts.hinting = False; opts.desubroutinize = True
        sub = subset.Subsetter(opts); sub.populate(text=txt); sub.subset(font)
        buf = io.BytesIO(); font.flavor = "woff"; font.save(buf)
        css += (f"@font-face{{font-family:'{fam}';font-weight:{w};"
                f"src:url(data:font/woff;base64,{base64.b64encode(buf.getvalue()).decode()}) format('woff');}}")
    return f"<style>{css}</style>"


def main():
    for fn in sorted(os.listdir(ASSETS)):
        m = re.match(r"logo-(\d\d)-.*\.svg$", fn)
        if not m:
            continue
        path = os.path.join(ASSETS, fn)
        svg = open(path, encoding="utf-8").read()
        svg = re.sub(r"<style>@font-face.*?</style>", "", svg, flags=re.S)
        n = m.group(1)
        if n in MARKS:
            a = svg.index("</defs>") + len("</defs>")
            z = svg.index("<text")
            svg = svg[:a] + "\n  " + MARKS[n]() + "\n  " + svg[z:]
        texts = re.findall(r"<text[^>]*>(.*?)</text>", svg)
        ar = "".join(t for t in texts if re.search(r"[؀-ۿ]", t))
        en = "".join(t for t in texts if not re.search(r"[؀-ۿ]", t)).replace("&amp;", "&")
        svg = svg.replace("</defs>", font_css(ar + " ", en + " ") + "</defs>", 1)
        open(path, "w", encoding="utf-8").write(svg)
        print(fn, len(svg))


if __name__ == "__main__":
    main()
