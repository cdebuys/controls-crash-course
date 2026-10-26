# 1. Time Domain

## The mass-spring-damper

The mass-spring-damper is the "hello world" of dynamic systems. A block of mass $m$
slides on a frictionless surface. A spring with stiffness $k$ connects it to a wall,
and a damper (think of a shock absorber) with coefficient $c$ resists its motion.

Let $x(t)$ be the block's displacement from its resting position. Two forces act on it:

- **The spring** pulls it back toward rest with a force proportional to displacement: $-kx$.
- **The damper** opposes motion with a force proportional to velocity: $-c\dot{x}$.

Newton's second law, $m\ddot{x} = \sum F$, gives the governing differential equation:

$$
m\ddot{x} + c\dot{x} + kx = 0
$$

### Natural frequency and damping ratio

Dividing through by $m$ puts the equation in a standard form that shows up throughout
control theory:

$$
\ddot{x} + 2\zeta\omega_n\dot{x} + \omega_n^2 x = 0,
\qquad
\omega_n = \sqrt{\frac{k}{m}},
\qquad
\zeta = \frac{c}{2\sqrt{km}}
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
\dot{v} = -\frac{c\,v + k\,x}{m},
$$

and advance $(x, v)$ by a small time step $\Delta t$ over and over. The widget below
does exactly that with the fourth-order Runge-Kutta method (RK4), using
$\Delta t = 1\text{ ms}$.

## Try it

The block has mass $m = 1\text{ kg}$ and starts at rest, pulled out to
$x_0 = 1\text{ m}$. Move the sliders and watch how $\zeta$ changes the response.
Can you find the stiffness and damping that give critical damping?

<style>
.msd-widget { border: 1px solid var(--md-default-fg-color--lightest); border-radius: 0.2rem; padding: 0.8rem 1rem; margin: 1em 0; }
.msd-controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 0.4rem 1.5rem; }
.msd-controls label { display: flex; flex-direction: column; gap: 0.2rem; }
.msd-controls input[type="range"] { width: 100%; accent-color: var(--md-accent-fg-color); }
.msd-readout { margin: 0.6rem 0; font-size: 0.75rem; color: var(--md-default-fg-color--light); }
.msd-anim { display: block; width: 100%; height: 120px; }
.msd-plot { position: relative; height: 280px; }
</style>
<div class="msd-widget">
  <div class="msd-controls">
    <label>
      <span>Spring constant <em>k</em> = <output id="msd-k-val"></output> N/m</span>
      <input type="range" id="msd-k" min="0.5" max="50" step="0.5" value="10">
    </label>
    <label>
      <span>Damping coefficient <em>c</em> = <output id="msd-c-val"></output> N·s/m</span>
      <input type="range" id="msd-c" min="0" max="10" step="0.1" value="1">
    </label>
  </div>
  <p class="msd-readout" id="msd-readout"></p>
  <canvas class="msd-anim" id="msd-anim"></canvas>
  <div class="msd-plot"><canvas id="msd-plot"></canvas></div>
</div>
<script>
(function () {
  "use strict";
  // Physical setup: fixed mass, released from rest at X0.
  const M = 1.0, X0 = 1.0, V0 = 0.0;
  // Simulation: RK4 with a 1 ms step over 10 s, keeping every 20th sample (50 Hz) for drawing.
  const T_END = 10.0, DT = 0.001, SAMPLE_EVERY = 20, SAMPLE_DT = DT * SAMPLE_EVERY;
  // Returns [dx/dt, dv/dt] for state (x, v).
  function deriv(x, v, k, c) {
    return [v, -(c * v + k * x) / M];
  }
  function simulate(k, c) {
    const steps = Math.round(T_END / DT);
    const points = [{ x: 0, y: X0 }];
    let x = X0, v = V0;
    for (let i = 1; i <= steps; i++) {
      const k1 = deriv(x, v, k, c);
      const k2 = deriv(x + 0.5 * DT * k1[0], v + 0.5 * DT * k1[1], k, c);
      const k3 = deriv(x + 0.5 * DT * k2[0], v + 0.5 * DT * k2[1], k, c);
      const k4 = deriv(x + DT * k3[0], v + DT * k3[1], k, c);
      x += (DT / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
      v += (DT / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
      if (i % SAMPLE_EVERY === 0) points.push({ x: i * DT, y: x });
    }
    return points;
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
      accent: get("--md-accent-fg-color", "#526cfe"),
    };
  }
  function init() {
    const kInput = document.getElementById("msd-k");
    const cInput = document.getElementById("msd-c");
    const kVal = document.getElementById("msd-k-val");
    const cVal = document.getElementById("msd-c-val");
    const readout = document.getElementById("msd-readout");
    const anim = document.getElementById("msd-anim");
    const ctx = anim.getContext("2d");
    let colors = themeColors();
    let points = [];
    let startTime = performance.now();
    let simTime = 0;
    // Draws a vertical line on the plot at the animation's current time.
    const timeCursor = {
      id: "msdTimeCursor",
      afterDatasetsDraw(chart) {
        const px = chart.scales.x.getPixelForValue(simTime);
        const area = chart.chartArea;
        chart.ctx.save();
        chart.ctx.strokeStyle = colors.accent;
        chart.ctx.lineWidth = 1;
        chart.ctx.beginPath();
        chart.ctx.moveTo(px, area.top);
        chart.ctx.lineTo(px, area.bottom);
        chart.ctx.stroke();
        chart.ctx.restore();
      },
    };
    const chart = new Chart(document.getElementById("msd-plot"), {
      type: "line",
      data: { datasets: [{ data: [], borderWidth: 2, pointRadius: 0 }] },
      options: {
        animation: false,
        parsing: false,
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "nearest", axis: "x", intersect: false },
        plugins: { legend: { display: false } },
        scales: {
          x: { type: "linear", min: 0, max: T_END, title: { display: true, text: "Time t (s)" } },
          y: { min: -1.1, max: 1.1, title: { display: true, text: "Displacement x (m)" } },
        },
      },
      plugins: [timeCursor],
    });
    function applyChartTheme() {
      const ds = chart.data.datasets[0];
      ds.borderColor = colors.primary;
      for (const axis of [chart.options.scales.x, chart.options.scales.y]) {
        axis.ticks = { color: colors.fgLight };
        axis.grid = { color: colors.fgLightest };
        axis.title.color = colors.fgLight;
      }
      chart.update("none");
    }
    function recompute() {
      const k = parseFloat(kInput.value);
      const c = parseFloat(cInput.value);
      kVal.textContent = k.toFixed(1);
      cVal.textContent = c.toFixed(1);
      const wn = Math.sqrt(k / M);
      const zeta = c / (2 * Math.sqrt(k * M));
      let regime;
      if (zeta === 0) regime = "undamped";
      else if (Math.abs(zeta - 1) < 0.01) regime = "critically damped";
      else if (zeta < 1) regime = "underdamped";
      else regime = "overdamped";
      readout.textContent = "ω_n = " + wn.toFixed(2) + " rad/s, ζ = " + zeta.toFixed(3) + " (" + regime + ")";
      points = simulate(k, c);
      chart.data.datasets[0].data = points;
      chart.update("none");
      startTime = performance.now();
    }
    // Linear interpolation of displacement at time t from the sampled trajectory.
    function displacementAt(t) {
      const f = t / SAMPLE_DT;
      const i = Math.min(Math.floor(f), points.length - 2);
      const a = f - i;
      return points[i].y * (1 - a) + points[i + 1].y * a;
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
      // Scale so the block stays on screen over the full range x in [-1.1, 1.1].
      const scale = (w / 2 - wallX - blockW) / 1.1;
      const blockLeft = restCenter + x * scale - blockW / 2;
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
    // Replays the trajectory in real time, looping every T_END seconds.
    function frame(now) {
      simTime = ((now - startTime) / 1000) % T_END;
      drawScene(displacementAt(simTime));
      chart.draw();
      requestAnimationFrame(frame);
    }
    kInput.addEventListener("input", recompute);
    cInput.addEventListener("input", recompute);
    window.addEventListener("resize", resizeAnim);
    // Material toggles light/dark by changing this attribute on <body>.
    new MutationObserver(() => {
      colors = themeColors();
      applyChartTheme();
    }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
    resizeAnim();
    applyChartTheme();
    recompute();
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
