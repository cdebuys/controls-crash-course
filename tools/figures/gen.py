"""Generate the course figures as light and dark SVG files in a shared style.

Usage, from the repository root:

    python3 tools/figures/gen.py docs/assets/figures

Uses only the Python standard library. Each figure is a function below; edit it and
re-run to regenerate both variants. Pages link both files with Material's
#only-light / #only-dark suffixes. Avoid the U+2212 minus sign in labels: some fonts
render it as a box.
"""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/assets/figures")

THEMES = {
    "": {"BG": "#ffffff", "TEXT": "#222", "MUTED": "#666", "PRIMARY": "#3f51b5", "ACCENT": "#e65100"},
    "_dark": {"BG": "#1e2029", "TEXT": "#e2e4e9", "MUTED": "#9aa0ab", "PRIMARY": "#8c9eff", "ACCENT": "#ffab40"},
}

STYLE = """
    .text {fill:@TEXT@} .muted {fill:@MUTED@}
    .axis {stroke:@MUTED@; stroke-width:1.4; fill:none}
    .edge {stroke:@MUTED@; stroke-width:1.5}
    .guide {stroke:@MUTED@; stroke-width:1.2; stroke-dasharray:5 4; fill:none}
    .fill-p {fill:@PRIMARY@; fill-opacity:0.18} .fill-a {fill:@ACCENT@; fill-opacity:0.18}
    .shade-p {fill:@PRIMARY@; fill-opacity:0.07} .shade-a {fill:@ACCENT@; fill-opacity:0.07}
    .line-t {stroke:@TEXT@; stroke-width:2.2; fill:none}
    .line-p {stroke:@PRIMARY@; stroke-width:2.4; fill:none}
    .line-a {stroke:@ACCENT@; stroke-width:2.4; fill:none}
    .line-m {stroke:@MUTED@; stroke-width:1.6; fill:none}
    .thin-p {stroke:@PRIMARY@; stroke-width:1.6; fill:none}
    .thin-a {stroke:@ACCENT@; stroke-width:1.6; fill:none}
    .dash-p {stroke:@PRIMARY@; stroke-width:2; stroke-dasharray:6 4; fill:none}
    .dash-a {stroke:@ACCENT@; stroke-width:2; stroke-dasharray:6 4; fill:none}
    .dotted-a {stroke:@ACCENT@; stroke-width:2.2; stroke-dasharray:0.1 5; stroke-linecap:round; fill:none}
    .dot {fill:@TEXT@} .dot-p {fill:@PRIMARY@} .dot-a {fill:@ACCENT@} .dot-m {fill:@MUTED@}
    .faint {opacity:0.35} .bg {fill:@BG@}
"""

MARKERS = "".join(
    f'<marker id="head-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
    f'markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="@{c}@"/></marker>'
    for k, c in [("t", "TEXT"), ("p", "PRIMARY"), ("a", "ACCENT"), ("m", "MUTED")]
)


class Fig:
    def __init__(self, w, h, title, vy=0):
        self.w, self.h, self.title, self.parts, self.defs, self.vy = w, h, title, [], [], vy

    def add(self, s):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, cls="axis", head=None, extra=""):
        m = f' marker-end="url(#head-{head})"' if head else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"{m} {extra}/>')

    def arrow(self, x1, y1, x2, y2, color="t", cls=None):
        self.line(x1, y1, x2, y2, cls or f"line-{color}", head=color)

    def poly(self, pts, cls):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polygon points="{p}" class="{cls}"/>')

    def polyline(self, pts, cls, head=None, clip=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        m = f' marker-end="url(#head-{head})"' if head else ""
        c = f' clip-path="url(#{clip})"' if clip else ""
        self.add(f'<polyline points="{p}" class="{cls}"{m}{c}/>')

    def path(self, d, cls, head=None, extra=""):
        m = f' marker-end="url(#head-{head})"' if head else ""
        self.add(f'<path d="{d}" class="{cls}"{m} {extra}/>')

    def circle(self, x, y, r, cls="dot", extra=""):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="{cls}" {extra}/>')

    def rect(self, x, y, w, h, cls, extra=""):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" class="{cls}" {extra}/>')

    def text(self, x, y, s, size=14, anchor="start", cls="text", italic=False, bold=False):
        st = (' font-style="italic"' if italic else "") + (' font-weight="bold"' if bold else "")
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" class="{cls}"{st}>{s}</text>')

    def clip(self, cid, x, y, w, h):
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')

    def matrix2(self, x, y, rows, label="", size=13):
        """Draw a 2x2 matrix with brackets; (x, y) is the left baseline of the first row."""
        cx = x
        if label:
            self.text(x, y + 8, label, size=size, italic=True)
            cx = x + 9 * len(label) + 4
        colw = max(len(e) for r in rows for e in r) * 7 + 14
        top, bot = y - size, y + 2 + size + 4
        self.path(f"M{cx+5},{top} L{cx},{top} L{cx},{bot} L{cx+5},{bot}", "line-m", extra='stroke-width="1.3"')
        for i, r in enumerate(rows):
            for j, e in enumerate(r):
                self.text(cx + 8 + colw * j + colw / 2 - 7, y + i * (size + 4), e, size=size, anchor="middle")
        rx = cx + 8 + colw * 2 - 6
        self.path(f"M{rx-5},{top} L{rx},{top} L{rx},{bot} L{rx-5},{bot}", "line-m", extra='stroke-width="1.3"')

    def svg(self, theme):
        body = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {self.vy} {self.w} {self.h}" '
            f'font-family="sans-serif" role="img"><title>{self.title}</title>'
            f"<style>{STYLE}</style><defs>{MARKERS}{''.join(self.defs)}</defs>"
            + "\n".join(self.parts) + "</svg>\n"
        )
        for k, v in theme.items():
            body = body.replace(f"@{k}@", v)
        return body


def save(fig, name):
    for suffix, theme in THEMES.items():
        (OUT / f"{name}{suffix}.svg").write_text(fig.svg(theme))


def nearest_on_rect(px, py, bx, by, bw, bh):
    return min(max(px, bx), bx + bw), min(max(py, by), by + bh)


# ---------------------------------------------------------------- 0.1 s-plane map
def s_plane_map():
    f = Fig(760, 462, "Where a root s sits in the complex plane, and the signal e^(st) it produces", vy=60)
    O, S = (380, 300), 70
    P = lambda s, w: (O[0] + S * s, O[1] - S * w)
    f.rect(142, 80, O[0] - 142, 410, "shade-p")
    f.rect(O[0], 80, 618 - O[0], 410, "shade-a")
    f.line(142, O[1], 625, O[1], "axis", head="m")
    f.line(O[0], 490, O[0], 72, "axis", head="m")
    f.text(632, O[1] + 5, "σ", size=16, italic=True)
    f.text(O[0] - 8, 76, "jω", size=16, italic=True, anchor="end")
    f.text(150, 512, "left half-plane: decays", size=14, cls="muted")
    f.text(612, 512, "right half-plane: grows", size=14, anchor="end", cls="muted")
    W, H, T = 100, 56, 6.0
    roots = [  # sigma, omega, box x, box y, color
        (-2.0, 0.0, 150, 322, "p"), (-0.8, 2.0, 150, 96, "p"), (-0.3, 2.0, 265, 195, "p"),
        (0.0, 2.5, 395, 88, "t"), (0.0, 0.0, 325, 322, "t"), (0.9, 0.0, 450, 322, "a"),
        (0.45, 2.0, 515, 104, "a"),
    ]
    for sg, om, bx, by, c in roots:
        x, y = P(sg, om)
        nx, ny = nearest_on_rect(x, y, bx, by, W, H)
        f.line(x, y, nx, ny, "guide")
        f.rect(bx, by, W, H, "bg edge", extra='stroke-width="1"')
        f.line(bx + 4, by + H / 2, bx + W - 4, by + H / 2, "guide", extra='stroke-width="0.8"')
        ts = [T * i / 160 for i in range(161)]
        vs = [math.exp(sg * t) * math.cos(om * t) for t in ts]
        m = max(abs(v) for v in vs)
        pts = [(bx + 4 + (W - 8) * t / T, by + H / 2 - (H / 2 - 6) * v / m) for t, v in zip(ts, vs)]
        f.polyline(pts, {"p": "line-p", "a": "line-a", "t": "line-t"}[c] + '" stroke-width="2')
        dot = {"p": "dot-p", "a": "dot-a", "t": "dot"}[c]
        f.circle(x, y, 5, dot)
        if om:
            mx, my = P(sg, -om)
            f.circle(mx, my, 5, dot, extra='opacity="0.35"')
    f.text(395, 296, "0", size=13, cls="muted")
    f.line(352, 141, 300, 141, "line-m", head="m")
    f.text(326, 132, "faster decay", size=12, anchor="middle", cls="muted")
    save(f, "s_plane_map")


# ---------------------------------------------------------------- 0.1 polar form
def complex_polar():
    f = Fig(440, 300, "A complex number z = a + jb as a point with magnitude |z| and angle")
    O, S = (80, 160), 55
    f.line(40, O[1], 400, O[1], "axis", head="m")
    f.line(O[0], 290, O[0], 18, "axis", head="m")
    f.text(406, O[1] + 5, "Re", size=14, cls="muted")
    f.text(O[0] + 8, 22, "Im", size=14, cls="muted")
    zx, zy = O[0] + 4 * S, O[1] - 2 * S
    f.line(zx, zy, zx, O[1], "guide")
    f.line(zx, zy, O[0], zy, "guide")
    f.arrow(O[0], O[1], zx - 6.3, zy + 3.2, "p")
    f.circle(zx, zy, 5, "dot-p")
    ang = math.atan2(2, 4)
    r = 38
    f.path(f"M{O[0]+r},{O[1]} A{r},{r} 0 0 0 {O[0]+r*math.cos(ang):.1f},{O[1]-r*math.sin(ang):.1f}", "line-m")
    f.text(O[0] + 46, O[1] - 7, "angle", size=13, cls="muted")
    f.text(O[0] + 2 * S - 8, O[1] - S - 12, "|z|", size=15, italic=True)
    f.text(zx + 10, zy - 6, "z = a + jb", size=15, italic=True)
    f.text(zx - 7, O[1] + 20, "a", size=14, anchor="end", italic=True)
    f.text(O[0] - 10, zy + 5, "b", size=14, anchor="end", italic=True)
    cy = O[1] + 2 * S
    f.line(zx, O[1], zx, cy, "guide")
    f.circle(zx, cy, 5, "dot-p", extra='opacity="0.4"')
    f.text(zx + 10, cy + 5, "conjugate: a - jb", size=14, cls="muted")
    save(f, "complex_polar")


# ---------------------------------------------------------------- 0.2 dot and cross
def dot_cross_products():
    f = Fig(760, 300, "Dot product as an angle and projection; cross product perpendicular to both vectors")
    O = (70, 230)
    th = math.radians(50)
    ax, ay = O[0] + 230, O[1]
    bx, by = O[0] + 150 * math.cos(th), O[1] - 150 * math.sin(th)
    f.line(bx, by, bx, O[1], "guide")
    f.line(O[0], O[1] + 12, bx, O[1] + 12, "line-m", extra='stroke-width="1.2"')
    f.text((O[0] + bx) / 2, O[1] + 30, "|b| cos θ", size=13, anchor="middle", cls="muted")
    f.arrow(O[0], O[1], ax, ay, "p")
    f.arrow(O[0], O[1], bx, by, "a")
    r = 36
    f.path(f"M{O[0]+r},{O[1]} A{r},{r} 0 0 0 {O[0]+r*math.cos(th):.1f},{O[1]-r*math.sin(th):.1f}", "line-m")
    f.text(O[0] + 44, O[1] - 14, "θ", size=15, italic=True)
    f.text(ax + 8, ay + 5, "a", size=16, italic=True, bold=True)
    f.text(bx + 6, by - 6, "b", size=16, italic=True, bold=True)
    f.text(70, 44, "a · b = |a| |b| cos θ", size=15, italic=True)
    f.text(70, 64, "zero when a and b are perpendicular", size=13, cls="muted")
    # Cross product (oblique 3D)
    O2 = (510, 230)
    a2, b2 = (140, 0), (60, -55)
    pa, pb = (O2[0] + a2[0], O2[1] + a2[1]), (O2[0] + b2[0], O2[1] + b2[1])
    pab = (O2[0] + a2[0] + b2[0], O2[1] + a2[1] + b2[1])
    f.poly([O2, pa, pab, pb], "fill-p")
    f.arrow(O2[0], O2[1], *pa, "p")
    f.arrow(O2[0], O2[1], *pb, "a")
    f.arrow(O2[0], O2[1], O2[0], 80, "t")
    f.path(f"M{O2[0]},{O2[1]-14} L{O2[0]+12},{O2[1]-14} L{O2[0]+12},{O2[1]}", "line-m", extra='stroke-width="1.2"')
    f.text(pa[0] + 8, pa[1] + 5, "a", size=16, italic=True, bold=True)
    f.text(pb[0] + 4, pb[1] - 6, "b", size=16, italic=True, bold=True)
    f.text(O2[0] + 10, 92, "a × b", size=16, italic=True, bold=True)
    f.text(430, 268, "|a × b| = |a| |b| sin θ, the shaded area", size=13, cls="muted")
    f.text(430, 44, "a × b is perpendicular to a and b", size=15)
    f.text(430, 64, "right-hand rule: curl fingers from a to b", size=13, cls="muted")
    save(f, "dot_cross_products")


# ---------------------------------------------------------------- 0.3 determinant
def determinant_area():
    f = Fig(760, 400, "The unit square mapped by A: its area scales by det A, and collapses to a line when det A = 0")
    S = 40

    def panel(O, c1, c2, fill, singular=False):
        f.line(O[0] - 20, O[1], O[0] + 150, O[1], "axis")
        f.line(O[0], O[1] + 20, O[0], O[1] - 260 if singular else O[1] - 120, "axis")
        p1 = (O[0] + S * c1[0], O[1] - S * c1[1])
        p2 = (O[0] + S * c2[0], O[1] - S * c2[1])
        p12 = (O[0] + S * (c1[0] + c2[0]), O[1] - S * (c1[1] + c2[1]))
        if singular:
            f.line(O[0], O[1], *p12, "line-p", extra='stroke-width="7" stroke-opacity="0.35"')
        else:
            f.poly([O, p1, p12, p2], fill)
        f.arrow(O[0], O[1], *p2, "a")
        f.arrow(O[0], O[1], *p1, "p")
        return p1, p2

    O1, O2, O3 = (70, 320), (240, 320), (520, 320)
    p1, p2 = panel(O1, (1, 0), (0, 1), "fill-p")
    f.text(O1[0] - 6, 40, "unit square", size=14, bold=True)
    f.text(O1[0] - 6, 60, "area 1", size=13, cls="muted")
    panel(O2, (2, 0.5), (1, 1.5), "fill-p")
    f.text(O2[0] - 6, 40, "area = det A = 2.5", size=14, bold=True)
    f.matrix2(O2[0] - 6, 72, [["2", "1"], ["0.5", "1.5"]], label="A =")
    panel(O3, (1, 2), (2, 4), "fill-p", singular=True)
    f.text(O3[0] - 130, 40, "det A = 0: flattened onto a line", size=14, bold=True)
    f.matrix2(O3[0] - 130, 72, [["1", "2"], ["2", "4"]], label="A =")
    nx, ny = O3[0] + 2 * S, O3[1] + 1 * S
    f.line(O3[0], O3[1], nx, ny, "dash-a", head="a")
    f.text(nx + 8, ny + 5, "[2, -1] is sent to 0", size=13, cls="muted")
    f.text(O1[0] + 4, O1[1] + 36, "columns of A:", size=13, cls="muted")
    f.circle(O1[0] + 98, O1[1] + 32, 4, "dot-p")
    f.text(O1[0] + 106, O1[1] + 36, "first", size=13, cls="muted")
    f.circle(O1[0] + 150, O1[1] + 32, 4, "dot-a")
    f.text(O1[0] + 158, O1[1] + 36, "second", size=13, cls="muted")
    save(f, "determinant_area")


# ---------------------------------------------------------------- shared oblique 3D plane
PLANE = [(229.8, 197.6), (58.2, 322.4), (370.2, 322.4), (541.8, 197.6)]
O3D = (300, 260)


def least_squares_projection():
    f = Fig(620, 260, "Least squares: the closest point to b in the column space, with the error perpendicular to it", vy=130)
    f.poly(PLANE, "fill-p")
    f.poly(PLANE, "edge" + '" fill="none')
    bt, pt = (368.4, 156.8), (368.4, 288.8)
    f.arrow(O3D[0], O3D[1], pt[0] - 2.1, pt[1] - 0.9, "p")
    f.arrow(O3D[0], O3D[1], bt[0] - 1.5, bt[1] + 2.4, "t")
    f.arrow(pt[0], pt[1], bt[0], bt[1] + 3, "a")
    f.path(f"M{pt[0]},{pt[1]-13} L{pt[0]-12},{pt[1]-18} L{pt[0]-12},{pt[1]-5}", "line-m", extra='stroke-width="1.2"')
    f.circle(*O3D, 4)
    f.circle(*pt, 4, "dot-p")
    f.text(bt[0] + 10, bt[1] - 2, "b", size=17, italic=True, bold=True)
    f.line(pt[0] + 4, pt[1] + 6, 392, 336, "guide")
    f.text(396, 344, "closest point in C(A)", size=14)
    f.text(bt[0] + 14, 186, "error: perpendicular to C(A)", size=14, cls="muted")
    f.text(O3D[0] - 14, O3D[1] + 19, "0", size=14, anchor="end")
    f.text(60, 350, "column space C(A)", size=14, bold=True)
    f.text(60, 368, "every output A can produce", size=14, cls="muted")
    save(f, "least_squares_projection")


# ---------------------------------------------------------------- 0.4 eigenvectors
def eigenvectors():
    f = Fig(520, 450, "Eigenvectors stay on their own line when multiplied by A; other vectors turn")
    O, S = (180, 290), 55
    P = lambda x, y: (O[0] + S * x, O[1] - S * y)
    f.clip("eig-clip", 30, 30, 270, 410)
    f.line(30, O[1], 300, O[1], "axis")
    f.line(O[0], 440, O[0], 30, "axis")
    for vx, vy in [(1, -1), (1, -2)]:
        a, b = P(-2.6 * vx, -2.6 * vy), P(2.6 * vx, 2.6 * vy)
        f.add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="guide" clip-path="url(#eig-clip)"/>')
    vecs = [  # before, after, color, labels
        ((1, -1), (-1, 1), "p", ("v₁", "Av₁ = -v₁")),
        ((1, -2), (-2, 4), "p", ("v₂", "Av₂ = -2v₂")),
        ((1, 0), (0, -2), "a", ("w", "Aw")),
    ]
    for (bx, by), (ax, ay), c, (lb, la) in vecs:
        p = P(bx, by)
        q = P(ax, ay)
        f.line(O[0], O[1], *p, "line-m", head="m")
        f.arrow(O[0], O[1], *q, c)
        lp = {"w": (p[0] + 4, p[1] - 10)}.get(lb, (p[0] + 8, p[1] + 5))
        f.text(*lp, lb, size=14, italic=True, cls="muted")
        lq = {"Av₂ = -2v₂": (q[0] + 10, q[1] - 2, "start"), "Av₁ = -v₁": (q[0] - 8, q[1] + 20, "end")}
        x, y, anc = lq.get(la, (q[0] + 8, q[1] + 16, "start"))
        f.text(x, y, la, size=14, italic=True, anchor=anc)
    f.circle(*O, 4)
    f.matrix2(320, 60, [["0", "1"], ["-2", "-3"]], label="A =")
    f.line(320, 120, 350, 120, "line-m", head="m")
    f.text(358, 125, "before", size=13, cls="muted")
    f.line(320, 145, 350, 145, "line-p", head="p")
    f.text(358, 150, "after: eigenvector", size=13, cls="muted")
    f.line(320, 170, 350, 170, "line-a", head="a")
    f.text(358, 175, "after: other vector", size=13, cls="muted")
    f.text(320, 210, "Eigenvectors stay on their", size=13, cls="muted")
    f.text(320, 228, "dashed line, only rescaled", size=13, cls="muted")
    f.text(320, 246, "(here, flipped). w turns.", size=13, cls="muted")
    save(f, "eigenvectors")


# ---------------------------------------------------------------- 0.7 linear approximation
def linear_approximation():
    f = Fig(440, 304, "sin(theta) and its tangent line theta agree near zero")
    O, Sx, Sy = (220, 150), 90, 80
    P = lambda x, y: (O[0] + Sx * x, O[1] - Sy * y)
    f.clip("la-clip", 40, 20, 370, 260)
    a, b = P(-0.45, 1.6), P(0.45, -1.6)
    f.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], "shade-p")
    f.line(36, O[1], 410, O[1], "axis", head="m")
    f.line(O[0], 282, O[0], 18, "axis", head="m")
    for v in (-1, 1):
        x, _ = P(v, 0)
        f.line(x, O[1] - 4, x, O[1] + 4, "axis")
        f.text(x, O[1] + 20, str(v).replace("-", "-"), size=12, anchor="middle", cls="muted")
        _, y = P(0, v)
        f.line(O[0] - 4, y, O[0] + 4, y, "axis")
        f.text(O[0] - 8, y + 4, str(v), size=12, anchor="end", cls="muted")
    xs = [-2 + 4 * i / 200 for i in range(201)]
    f.add('<polyline points="' + " ".join(f"{P(x, x)[0]:.1f},{P(x, x)[1]:.1f}" for x in xs)
          + '" class="dash-a" clip-path="url(#la-clip)"/>')
    f.polyline([P(x, math.sin(x)) for x in xs], "line-p")
    f.text(416, O[1] + 5, "θ", size=15, italic=True)
    f.text(P(1.5, 0)[0], P(0, math.sin(1.5))[1] + 22, "sin θ", size=15, italic=True)
    f.text(P(1.62, 1.6)[0] + 6, P(0, 1.6)[1] + 14, "θ", size=15, italic=True)
    f.text(44, 294, "dashed: the tangent line at 0", size=13, cls="muted")
    f.text(O[0] + 8, 272, "nearly equal near 0", size=13, cls="muted")
    save(f, "linear_approximation")


# ---------------------------------------------------------------- 0.7 Jacobian ellipse
def jacobian_ellipse():
    f = Fig(760, 320, "A small circle of inputs maps through the Jacobian to an ellipse of outputs")
    S, eps, rb, tb = 80, 0.35, 1.5, 0.6
    L0, R0 = (70, 270), (460, 270)
    f.line(L0[0] - 10, L0[1], L0[0] + 250, L0[1], "axis", head="m")
    f.line(L0[0], L0[1] + 10, L0[0], 40, "axis", head="m")
    f.text(L0[0] + 256, L0[1] + 5, "r", size=15, italic=True)
    f.text(L0[0] + 8, 44, "θ", size=15, italic=True)
    cx, cy = L0[0] + S * rb, L0[1] - S * tb * 2.2
    f.circle(cx, cy, S * eps, "fill-p")
    f.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{S*eps:.1f}" class="thin-p"/>')
    f.circle(cx, cy, 4, "dot-p")
    f.text(L0[0] + 10, 300, "inputs (r, θ): a small circle", size=14)
    f.line(R0[0] - 10, R0[1], R0[0] + 250, R0[1], "axis", head="m")
    f.line(R0[0], R0[1] + 10, R0[0], 40, "axis", head="m")
    f.text(R0[0] + 256, R0[1] + 5, "x", size=15, italic=True)
    f.text(R0[0] + 8, 44, "y", size=15, italic=True)
    px, py = R0[0] + S * rb * math.cos(tb), R0[1] - S * rb * math.sin(tb)
    f.line(R0[0], R0[1], px, py, "guide")
    deg = -math.degrees(tb)
    f.add(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{S*eps:.1f}" ry="{S*eps*rb:.1f}" '
          f'transform="rotate({deg:.1f} {px:.1f} {py:.1f})" class="fill-p"/>')
    f.add(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{S*eps:.1f}" ry="{S*eps*rb:.1f}" '
          f'transform="rotate({deg:.1f} {px:.1f} {py:.1f})" class="thin-p"/>')
    f.circle(px, py, 4, "dot-p")
    f.text(R0[0] + 10, 300, "outputs (x, y): an ellipse, stretched by r", size=14)
    f.path(f"M{cx+40:.0f},{cy-20:.0f} C{cx+130:.0f},{cy-90:.0f} {px-140:.0f},{py-80:.0f} {px-48:.0f},{py-30:.0f}", "line-t", head="t")
    f.text((cx + px) / 2, 70, "J", size=18, anchor="middle", italic=True, bold=True)
    save(f, "jacobian_ellipse")


# ---------------------------------------------------------------- 0.8 bowl and saddle
def quadratic_bowl_saddle():
    f = Fig(680, 360, "Contours of a positive-definite quadratic (a bowl) and an indefinite one (a saddle)")
    S = 60
    for cid, x0 in (("bs-l", 30), ("bs-r", 370)):
        f.clip(cid, x0, 50, 280, 260)
        f.rect(x0, 50, 280, 260, "edge", extra='fill="none" stroke-width="1"')
    C1, C2 = (170, 180), (510, 180)
    # Bowl: Q = [[2, 0.6], [0.6, 1]]
    tr, det = 3.0, 2 * 1 - 0.36
    l1 = tr / 2 + math.sqrt(tr * tr / 4 - det)
    l2 = tr / 2 - math.sqrt(tr * tr / 4 - det)
    e1 = (0.6, l1 - 2)
    n = math.hypot(*e1)
    e1 = (e1[0] / n, e1[1] / n)
    e2 = (-e1[1], e1[0])
    for c in (0.3, 0.9, 1.8, 3.0):
        pts = []
        for i in range(121):
            t = 2 * math.pi * i / 120
            u, v = math.sqrt(c / l1) * math.cos(t), math.sqrt(c / l2) * math.sin(t)
            x, y = u * e1[0] + v * e2[0], u * e1[1] + v * e2[1]
            pts.append((C1[0] + S * x, C1[1] - S * y))
        f.polyline(pts, "thin-p", clip="bs-l")
    f.circle(*C1, 4.5, "dot-p")
    f.text(30, 30, "positive definite: a bowl", size=15, bold=True)
    f.text(30, 334, "all eigenvalues positive: one minimum (dot)", size=13, cls="muted")
    # Saddle: x^2 - y^2
    for a in (1, -1):
        f.add(f'<line x1="{C2[0]-200}" y1="{C2[1]+200*a}" x2="{C2[0]+200}" y2="{C2[1]-200*a}" '
              f'class="guide" clip-path="url(#bs-r)"/>')
    for c in (0.3, 1.0, 2.2):
        for sgn in (1, -1):
            for flip in (False, True):
                pts = []
                for i in range(81):
                    u = -2.2 + 4.4 * i / 80
                    a, b = sgn * math.sqrt(c) * math.cosh(u), math.sqrt(c) * math.sinh(u)
                    x, y = (b, a) if flip else (a, b)
                    pts.append((C2[0] + S * x, C2[1] - S * y))
                f.polyline(pts, "thin-p", clip="bs-r")
    f.circle(*C2, 4.5, "dot")
    f.text(370, 30, "indefinite: a saddle", size=15, bold=True)
    f.text(370, 334, "eigenvalues of both signs: no minimum", size=13, cls="muted")
    save(f, "quadratic_bowl_saddle")


# ---------------------------------------------------------------- Ch1 mass-spring-damper
def mass_spring_damper():
    f = Fig(560, 230, "Mass-spring-damper: a block on a frictionless surface, tied to a wall by a spring and a damper")
    wall, ground = 60, 190
    f.line(wall, 40, wall, ground, "line-m", extra='stroke-width="2"')
    for y in range(48, ground, 14):
        f.line(wall, y, wall - 12, y + 10, "line-m", extra='stroke-width="1.2"')
    f.line(wall, ground, 520, ground, "line-m", extra='stroke-width="2"')
    for x in range(wall + 6, 520, 14):
        f.line(x, ground, x - 10, ground + 12, "line-m", extra='stroke-width="1.2"')
    bl = 300
    f.rect(bl, 90, 80, 100, "fill-p", extra='stroke="none"')
    f.rect(bl, 90, 80, 100, "edge", extra='fill="none" stroke-width="2"')
    f.text(bl + 40, 146, "m", size=20, anchor="middle", italic=True, bold=True)
    # Spring
    y, coils, amp = 115, 9, 10
    x0, x1 = wall + 20, bl - 20
    pitch = (x1 - x0) / coils
    pts = [(wall, y), (x0, y)]
    for i in range(coils):
        pts += [(x0 + (i + 0.25) * pitch, y - amp), (x0 + (i + 0.75) * pitch, y + amp)]
    pts += [(x1, y), (bl, y)]
    f.polyline(pts, "line-t")
    f.text((wall + bl) / 2, y - 18, "k", size=16, anchor="middle", italic=True)
    # Damper (dashpot)
    y = 165
    f.line(wall, y, 150, y, "line-t")
    f.path(f"M200,{y-14} L150,{y-14} L150,{y+14} L200,{y+14}", "line-t")
    f.line(178, y - 10, 178, y + 10, "line-t", extra='stroke-width="3"')
    f.line(178, y, bl, y, "line-t")
    f.text(175, y - 20, "b", size=16, anchor="middle", italic=True)
    # Input force
    f.arrow(bl + 80, 140, bl + 150, 140, "a")
    f.text(bl + 158, 145, "u", size=16, italic=True)
    # Displacement from rest
    rest = 268
    f.line(rest, 50, rest, ground, "guide")
    f.text(rest, 44, "rest", size=12, anchor="middle", cls="muted")
    f.line(rest, 70, bl - 2, 70, "line-m", head="m")
    f.text((rest + bl) / 2, 64, "x", size=15, anchor="middle", italic=True)
    save(f, "mass_spring_damper")


# ---------------------------------------------------------------- Ch1 first-order step
def first_order_step():
    f = Fig(540, 300, "First-order step response, with the time constant tau marked at 63 percent")
    O, Sx, Sy = (80, 240), 84, 180
    P = lambda t, v: (O[0] + Sx * t, O[1] - Sy * v)
    f.line(O[0], O[1], 520, O[1], "axis", head="m")
    f.line(O[0], O[1], O[0], 30, "axis", head="m")
    f.line(*P(0, 1), *P(5.2, 1), "guide")
    f.text(O[0] - 8, P(0, 1)[1] + 4, "u/b", size=13, anchor="end", italic=True)
    for k in range(1, 6):
        x, _ = P(k, 0)
        f.line(x, O[1] - 4, x, O[1] + 4, "axis")
        f.text(x, O[1] + 20, ("" if k == 1 else str(k)) + "τ", size=13, anchor="middle", italic=True, cls="muted")
    ts = [5.2 * i / 200 for i in range(201)]
    f.polyline([P(t, 1 - math.exp(-t)) for t in ts], "line-p")
    for k, lab in ((1, "63%"), (4, "98%")):
        x, y = P(k, 1 - math.exp(-k))
        f.line(x, O[1], x, y, "guide")
        if k == 1:
            f.line(O[0], y, x, y, "guide")
        f.circle(x, y, 4.5, "dot-p")
    f.text(O[0] - 8, P(0, 1 - math.exp(-1))[1] + 4, "63%", size=13, anchor="end", cls="muted")
    f.text(P(4, 0)[0] - 8, P(0, 0.72)[1], "98% at 4τ: essentially done", size=13, anchor="end", cls="muted")
    f.text(526, O[1] + 5, "t", size=15, italic=True)
    f.text(O[0] + 8, 34, "speed v", size=14, cls="muted")
    save(f, "first_order_step")


# ---------------------------------------------------------------- Ch1 roots vs zeta
def roots_vs_zeta():
    f = Fig(560, 390, "Roots of the mass-spring-damper as the damping ratio zeta increases")
    O, S = (420, 190), 120
    P = lambda s, w: (O[0] + S * s, O[1] - S * w)
    f.line(60, O[1], 530, O[1], "axis", head="m")
    f.line(O[0], 350, O[0], 30, "axis", head="m")
    f.text(536, O[1] + 5, "σ", size=16, italic=True)
    f.text(O[0] - 8, 38, "jω", size=16, italic=True, anchor="end")
    top, left, bot = P(0, 1), P(-1, 0), P(0, -1)
    f.path(f"M{top[0]},{top[1]} A{S},{S} 0 0 0 {left[0]},{left[1]}", "dash-p", head="p")
    f.path(f"M{bot[0]},{bot[1]} A{S},{S} 0 0 1 {left[0]},{left[1]}", "dash-p", head="p")
    f.line(left[0] + 8, O[1], P(-0.382, 0)[0] - 9, O[1], "dash-p", head="p")
    f.line(left[0] - 8, O[1], P(-2.618, 0)[0] + 9, O[1], "dash-p", head="p")
    p7 = P(-0.7, math.sqrt(1 - 0.49))
    f.line(O[0], O[1], *p7, "guide")
    f.text((O[0] + p7[0]) / 2 + 10, (O[1] + p7[1]) / 2 + 6, "ωₙ", size=15, italic=True)
    for z in (0.0, 0.3, 0.7):
        w = math.sqrt(1 - z * z)
        for sgn in (1, -1):
            x, y = P(-z, sgn * w)
            f.circle(x, y, 5.5, "dot-p")
        x, y = P(-z, w)
        ang = math.atan2(w, -z)
        if z == 0:
            f.text(x + 12, y - 8, "ζ = 0", size=13)
        else:
            f.text(x + 22 * math.cos(ang), y - 22 * math.sin(ang) + 4, f"ζ = {z:g}", size=13, anchor="end")
    f.circle(*left, 6.5, "dot-p")
    f.text(left[0] - 12, O[1] - 12, "ζ = 1", size=13, anchor="end")
    for s in (-1.5 + math.sqrt(1.25), -1.5 - math.sqrt(1.25)):
        x, y = P(s, 0)
        f.circle(x, y, 5.5, "dot-p")
        f.text(x, O[1] + 24, "ζ = 1.5", size=13, anchor="middle")
    f.text(60, 300, "0 < ζ < 1: complex pair on the circle", size=13, cls="muted")
    f.text(60, 320, "ζ = 1: the pair meets at -ωₙ", size=13, cls="muted")
    f.text(60, 340, "ζ > 1: two real roots, moving apart", size=13, cls="muted")
    save(f, "roots_vs_zeta")


# ---------------------------------------------------------------- Ch1 pendulum
def pendulum():
    f = Fig(560, 320, "A pendulum hanging down (stable) and balanced upright (unstable)")
    L = 150

    def draw(px, py, theta, caption, sub, up):
        # Support
        hy = py - 8 if not up else py + 8
        f.line(px - 30, hy, px + 30, hy, "line-m", extra='stroke-width="2"')
        for x in range(px - 28, px + 30, 10):
            f.line(x, hy, x + 8, hy - 8 if not up else hy + 8, "line-m", extra='stroke-width="1.2"')
        bx, by = px + L * math.sin(theta), py - L * math.cos(theta) * (1 if up else -1)
        if up:
            bx, by = px + L * math.sin(theta), py - L * math.cos(theta)
        else:
            bx, by = px + L * math.sin(theta), py + L * math.cos(theta)
        ref = (px, py - L - 10) if up else (px, py + L + 10)
        f.line(px, py, *ref, "guide")
        f.line(px, py, bx, by, "line-t")
        r = 46
        if up:
            f.path(f"M{px},{py-r} A{r},{r} 0 0 1 {px+r*math.sin(theta):.1f},{py-r*math.cos(theta):.1f}", "line-m")
        else:
            f.path(f"M{px},{py+r} A{r},{r} 0 0 0 {px+r*math.sin(theta):.1f},{py+r*math.cos(theta):.1f}", "line-m")
        f.circle(bx, by, 13, "dot-p")
        f.text(bx + 18, by + 5, "m", size=15, italic=True)
        f.arrow(bx, by + 14, bx, by + 54, "a")
        f.text(bx + 8, by + 50, "mg", size=14, italic=True)
        f.text((px + bx) / 2 - 12, (py + by) / 2, "l", size=15, italic=True, anchor="end")
        f.circle(px, py, 4.5, "dot")
        rr = 22
        a0, a1 = (math.radians(170), math.radians(255)) if not up else (math.radians(100), math.radians(185))
        sx, sy = px + rr * math.cos(a0), py - rr * math.sin(a0)
        ex, ey = px + rr * math.cos(a1), py - rr * math.sin(a1)
        f.path(f"M{sx:.1f},{sy:.1f} A{rr},{rr} 0 0 0 {ex:.1f},{ey:.1f}", "line-a", head="a")
        f.text(px - 30, py + (22 if not up else -12), "τ", size=15, italic=True, anchor="end")
        f.text(px, 296, caption, size=14, anchor="middle", bold=True)
        f.text(px, 314, sub, size=13, anchor="middle", cls="muted")
        return bx, by

    draw(140, 60, math.radians(22), "hanging: θ = 0", "gravity pulls it back: stable", up=False)
    draw(420, 220, math.radians(18), "upright: θ = π", "gravity pulls it away: unstable", up=True)
    f.text(140 + 30, 60 + 66, "θ", size=15, italic=True)
    save(f, "pendulum")


# ---------------------------------------------------------------- 0.1 decaying sinusoid
def decaying_sinusoid():
    f = Fig(645, 290, "A decaying sinusoid e^(sigma t) cos(omega t) inside its exponential envelope")
    O, Sx, Sy, T = (60, 145), 88, 105, 6.0
    sg, om = -0.5, 4.0
    P = lambda t, v: (O[0] + Sx * t, O[1] - Sy * v)
    f.line(O[0], O[1], O[0] + Sx * T + 24, O[1], "axis", head="m")
    f.line(O[0], 265, O[0], 20, "axis", head="m")
    for k in range(1, 7):
        x, _ = P(k, 0)
        f.line(x, O[1] - 4, x, O[1] + 4, "axis")
    for v in (1, -1):
        _, y = P(0, v)
        f.line(O[0] - 4, y, O[0] + 4, y, "axis")
        f.text(O[0] - 8, y + 4, str(v), size=12, anchor="end", cls="muted")
    ts = [T * i / 400 for i in range(401)]
    for sgn in (1, -1):
        f.polyline([P(t, sgn * math.exp(sg * t)) for t in ts], "dotted-a")
    f.polyline([P(t, math.exp(sg * t) * math.cos(om * t)) for t in ts], "line-p")
    f.text(O[0] + Sx * T + 30, O[1] + 5, "t", size=15, italic=True)
    # Labels, with superscripts as raised tspans
    sup = lambda base, exp: (f'{base}<tspan dy="-7" font-size="11">{exp}</tspan><tspan dy="7"> </tspan>')
    f.add(f'<text x="{P(1.15, 0)[0]:.0f}" y="{P(0, 0.80)[1]:.0f}" font-size="15" class="text" font-style="italic">'
          + sup("e", "σt") + 'cos ωt</text>')
    f.add(f'<text x="{P(2.6, 0)[0]:.0f}" y="{P(0, math.exp(sg * 2.6))[1] - 10:.0f}" font-size="14" class="text" font-style="italic">'
          + sup("e", "σt") + '</text>')
    f.add(f'<text x="{P(2.6, 0)[0]:.0f}" y="{P(0, -math.exp(sg * 2.6))[1] + 22:.0f}" font-size="14" class="text" font-style="italic">-'
          + sup("e", "σt") + '</text>')
    f.text(P(3.6, 0)[0], P(0, 0.62)[1], "envelope: a first-order decay", size=13, cls="muted")
    save(f, "decaying_sinusoid")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (s_plane_map, complex_polar, dot_cross_products, determinant_area, least_squares_projection,
               eigenvectors, linear_approximation, jacobian_ellipse, quadratic_bowl_saddle,
               mass_spring_damper, first_order_step, roots_vs_zeta, pendulum, decaying_sinusoid):
        fn()
        print("wrote", fn.__name__)
