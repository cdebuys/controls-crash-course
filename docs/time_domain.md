# 1. Time Domain

## The mass-spring-damper

The mass-spring-damper is the "hello world" of dynamic systems. A block of mass $m$
slides on a frictionless surface. A spring with stiffness $k$ connects it to a wall,
and a damper (think of a shock absorber) with coefficient $b$ resists its motion.

Let $x(t)$ be the block's displacement from its resting position. Two forces act on it:

- **The spring** pulls it back toward rest with a force proportional to displacement: $-kx$.
- **The damper** opposes motion with a force proportional to velocity: $-b\dot{x}$.

Newton's second law, $m\ddot{x} = \sum F$, gives the governing differential equation:

$$
m\ddot{x} + b\dot{x} + kx = 0
$$

### Natural frequency and damping ratio

Dividing through by $m$ puts the equation in a standard form that shows up throughout
control theory:

$$
\ddot{x} + 2\zeta\omega_n\dot{x} + \omega_n^2 x = 0,
\qquad
\omega_n = \sqrt{\frac{k}{m}},
\qquad
\zeta = \frac{b}{2\sqrt{km}}
$$

The **natural frequency** $\omega_n$ (rad/s) sets how fast the system wants to
oscillate. The **damping ratio** $\zeta$ (no units) decides how the motion dies out:

| Damping ratio | Behavior |
|---|---|
| $\zeta = 0$ | **Undamped:** oscillates forever. |
| $0 < \zeta < 1$ | **Underdamped:** oscillates with a decaying envelope. |
| $\zeta = 1$ | **Critically damped:** fastest return to rest without overshooting. |
| $\zeta > 1$ | **Overdamped:** creeps back to rest without oscillating. |

### Simulating it

Equations like this one rarely get solved by hand in practice. A computer steps them
forward in time instead. Rewrite the second-order equation as two first-order ones,

$$
\dot{x} = v,
\qquad
\dot{v} = -\frac{b\,v + k\,x}{m},
$$


and advance $(x, v)$ by a small time step $\Delta t$ over and over. The widget below
does exactly that, live, with the fourth-order Runge-Kutta method (RK4) and
$\Delta t = 1\text{ ms}$.

## Try it

The block has mass $m = 1\text{ kg}$. Press **Impulse** to strike it. An impulse $J$
changes the block's velocity instantly by $\Delta v = J/m$; here
$J = 1.5\text{ N·s}$. Change $k$ and $b$ at any time, even mid-swing, and watch how
$\zeta$ changes the response. For a given stiffness, can you find the damping that
gives critical damping?

<style>
.msd-widget { border: 1px solid var(--md-default-fg-color--lightest); border-radius: 0.2rem; padding: 0.8rem 1rem; margin: 1em 0; }
.msd-controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 0.4rem 1.5rem; align-items: end; }
.msd-controls label { display: flex; flex-direction: column; gap: 0.2rem; }
.msd-controls input[type="range"] { width: 100%; accent-color: var(--md-accent-fg-color); }
.msd-controls .md-button { margin: 0; justify-self: start; }
.msd-readout { margin: 0.6rem 0; font-size: 0.75rem; color: var(--md-default-fg-color--light); }
.msd-anim { display: block; width: 100%; height: 120px; }
.msd-plot { position: relative; height: 280px; }
</style>
<div class="msd-widget">
  <div class="msd-controls">
    <label>
      <span>Spring constant <em>k</em> = <output id="msd-k-val"></output> N/m</span>
      <input type="range" id="msd-k" min="1" max="50" step="0.5" value="10">
    </label>
    <label>
      <span>Damping coefficient <em>b</em> = <output id="msd-b-val"></output> N·s/m</span>
      <input type="range" id="msd-b" min="0" max="10" step="0.1" value="1">
    </label>
    <button type="button" class="md-button md-button--primary" id="msd-impulse">Impulse</button>
  </div>
  <p class="msd-readout" id="msd-readout"></p>
  <canvas class="msd-anim" id="msd-anim"></canvas>
  <div class="msd-plot"><canvas id="msd-plot"></canvas></div>
</div>
<script>
(function () {
  "use strict";
  const M = 1.0;            // mass (kg)
  const IMPULSE = 1.5;      // impulse per button press (N·s)
  const DT = 0.001;         // RK4 step (s)
  const SAMPLE_EVERY = 20;  // keep every 20th step for the plot (50 Hz)
  const WINDOW = 10.0;      // seconds of history shown on the plot
  const MAX_FRAME_DT = 0.05;  // cap per-frame catch-up, e.g. after a background tab
  const X_VIEW = 1.6;       // displacement range shown (m)
  // Returns [dx/dt, dv/dt] for state (x, v).
  function deriv(x, v, k, b) {
    return [v, -(b * v + k * x) / M];
  }
  function rk4Step(s, k, b) {
    const k1 = deriv(s.x, s.v, k, b);
    const k2 = deriv(s.x + 0.5 * DT * k1[0], s.v + 0.5 * DT * k1[1], k, b);
    const k3 = deriv(s.x + 0.5 * DT * k2[0], s.v + 0.5 * DT * k2[1], k, b);
    const k4 = deriv(s.x + DT * k3[0], s.v + DT * k3[1], k, b);
    s.x += (DT / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
    s.v += (DT / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
  }
  // Reads colors from the Material theme so the widget follows light/dark mode.
  function themeColors() {
    const s = getComputedStyle(document.body);
    const get = (name, fallback) => s.getPropertyValue(name).trim() || fallback;
    return {
      fg: get("--md-default-fg-color", "#000"),
      fgLight: get("--md-default-fg-color--light", "#666"),
      fgLightest: get("--md-default-fg-color--lightest", "#ddd"),
      primary: get("--md-primary-fg-color", "#3f51b5"),
    };
  }
  function init() {
    const kInput = document.getElementById("msd-k");
    const bInput = document.getElementById("msd-b");
    const kVal = document.getElementById("msd-k-val");
    const bVal = document.getElementById("msd-b-val");
    const readout = document.getElementById("msd-readout");
    const anim = document.getElementById("msd-anim");
    const ctx = anim.getContext("2d");
    let colors = themeColors();
    let k = 0, b = 0;
    const state = { x: 0, v: 0 };
    let t = 0, steps = 0, accumulator = 0, lastTs = null;
    const samples = [{ x: 0, y: 0 }];
    const chart = new Chart(document.getElementById("msd-plot"), {
      type: "line",
      data: { datasets: [{ data: samples, borderWidth: 2, pointRadius: 0 }] },
      options: {
        animation: false,
        parsing: false,
        responsive: true,
        maintainAspectRatio: false,
        events: [],
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
        scales: {
          x: { type: "linear", min: 0, max: WINDOW, title: { display: true, text: "Time t (s)" } },
          y: { min: -X_VIEW, max: X_VIEW, title: { display: true, text: "Displacement x (m)" } },
        },
      },
    });
    function applyChartTheme() {
      chart.data.datasets[0].borderColor = colors.primary;
      for (const axis of [chart.options.scales.x, chart.options.scales.y]) {
        axis.ticks = { color: colors.fgLight, precision: 1 };
        axis.grid = { color: colors.fgLightest };
        axis.title.color = colors.fgLight;
      }
      chart.update("none");
    }
    // Sliders only change the parameters; the motion carries on from its current state.
    function readParams() {
      k = parseFloat(kInput.value);
      b = parseFloat(bInput.value);
      kVal.textContent = k.toFixed(1);
      bVal.textContent = b.toFixed(1);
      const wn = Math.sqrt(k / M);
      const zeta = b / (2 * Math.sqrt(k * M));
      let regime;
      if (zeta === 0) regime = "undamped";
      else if (Math.abs(zeta - 1) < 0.01) regime = "critically damped";
      else if (zeta < 1) regime = "underdamped";
      else regime = "overdamped";
      readout.textContent = "ω_n = " + wn.toFixed(2) + " rad/s, ζ = " + zeta.toFixed(3) + " (" + regime + ")";
    }
    function applyImpulse() {
      state.v += IMPULSE / M;
    }
    // Advances the simulation by `elapsed` seconds of wall-clock time in fixed RK4 steps.
    function advance(elapsed) {
      accumulator += elapsed;
      while (accumulator >= DT) {
        rk4Step(state, k, b);
        accumulator -= DT;
        t += DT;
        steps++;
        if (steps % SAMPLE_EVERY === 0) samples.push({ x: t, y: state.x });
      }
      while (samples.length > 0 && samples[0].x < t - WINDOW) samples.shift();
    }
    function resizeAnim() {
      const dpr = window.devicePixelRatio || 1;
      anim.width = Math.round(anim.clientWidth * dpr);
      anim.height = Math.round(anim.clientHeight * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function drawScene(x) {
      const w = anim.clientWidth, h = anim.clientHeight;
      const wallX = 16, blockW = 48, blockH = 48;
      const groundY = h - 16;
      const restCenter = w / 2;
      // Scale so the block stays on screen over x in [-X_VIEW, X_VIEW]; clamp beyond that.
      const scale = (w / 2 - wallX - blockW) / X_VIEW;
      const shownX = Math.max(-X_VIEW, Math.min(X_VIEW, x));
      const blockLeft = restCenter + shownX * scale - blockW / 2;
      const midY = groundY - blockH / 2;
      ctx.clearRect(0, 0, w, h);
      ctx.lineWidth = 2;
      // Wall and ground.
      ctx.strokeStyle = colors.fgLight;
      ctx.beginPath();
      ctx.moveTo(wallX, groundY - blockH - 16);
      ctx.lineTo(wallX, groundY);
      ctx.lineTo(w - 8, groundY);
      ctx.stroke();
      // Resting position marker.
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = colors.fgLightest;
      ctx.beginPath();
      ctx.moveTo(restCenter, 8);
      ctx.lineTo(restCenter, groundY);
      ctx.stroke();
      ctx.setLineDash([]);
      // Spring: straight leads at each end with a zigzag in between.
      const coils = 12, amp = 10, lead = 10;
      const zigStart = wallX + lead, zigEnd = blockLeft - lead;
      const pitch = (zigEnd - zigStart) / coils;
      ctx.strokeStyle = colors.fg;
      ctx.beginPath();
      ctx.moveTo(wallX, midY);
      ctx.lineTo(zigStart, midY);
      for (let i = 0; i < coils; i++) {
        ctx.lineTo(zigStart + (i + 0.25) * pitch, midY - amp);
        ctx.lineTo(zigStart + (i + 0.75) * pitch, midY + amp);
      }
      ctx.lineTo(zigEnd, midY);
      ctx.lineTo(blockLeft, midY);
      ctx.stroke();
      // Mass.
      ctx.fillStyle = colors.primary;
      ctx.fillRect(blockLeft, groundY - blockH, blockW, blockH);
      ctx.fillStyle = "#fff";
      ctx.font = "bold 14px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("m", blockLeft + blockW / 2, midY);
    }
    // Runs the simulation in real time. Only frame timestamps are used for timing.
    function frame(ts) {
      if (lastTs !== null) advance(Math.min(MAX_FRAME_DT, Math.max(0, (ts - lastTs) / 1000)));
      lastTs = ts;
      chart.options.scales.x.min = Math.max(0, t - WINDOW);
      chart.options.scales.x.max = Math.max(WINDOW, t);
      chart.update("none");
      drawScene(state.x);
      requestAnimationFrame(frame);
    }
    kInput.addEventListener("input", readParams);
    bInput.addEventListener("input", readParams);
    document.getElementById("msd-impulse").addEventListener("click", applyImpulse);
    window.addEventListener("resize", resizeAnim);
    // Material toggles light/dark by changing this attribute on <body>.
    new MutationObserver(() => {
      colors = themeColors();
      applyChartTheme();
    }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
    resizeAnim();
    applyChartTheme();
    readParams();
    applyImpulse();  // start with one strike so the page isn't static on load
    requestAnimationFrame(frame);
  }
  // MkDocs loads extra_javascript (Chart.js) after the page content, so wait for it.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
