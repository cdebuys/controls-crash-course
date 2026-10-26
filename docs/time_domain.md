# 1. Time Domain and State Space

Control theory is about making physical things behave the way you want: a motor that
holds its speed, a robot joint that reaches its target without overshooting, an arm
that tracks a path. Before we can control anything, we need to describe how it moves
on its own. This chapter builds that description in the **time domain**: how a system's
variables evolve from one instant to the next.

By the end of the chapter you'll be able to write the equations of motion for simple
systems, read their behavior from a few parameters, put them in the matrix form that
every later chapter (and every robotics library) uses, and simulate them in code
without the simulation blowing up.

## Dynamic systems

A **dynamic system** is one whose output depends on its history, not just on its
current input. Push a shopping cart and let go: it keeps rolling. Its speed right now
depends on every push it has received, minus whatever friction has taken away since.

We describe dynamic systems with **differential equations**, which relate a quantity
to its rates of change. Three words come up constantly:

- The **input** $u(t)$ is what we can act on: a force, a voltage, a torque.
- The **output** $y(t)$ is what we measure or care about: a position, a speed.
- The **state** is the smallest set of variables that, together with future inputs,
  fully determines the future.

!!! tip "For software engineers"
    Think of the state as everything you'd need to serialize to pause a simulation and
    resume it later with identical results. The differential equation is the update
    rule that advances it.

## First-order systems

The simplest dynamic systems have a single state variable and are described by a
**first-order** differential equation: one that involves only the first derivative.

### Example: a cart with drag

A cart of mass $m$ rolls along a track. You push it with force $u$, and viscous drag
resists it with a force proportional to its speed, $-bv$. Newton's second law gives

$$
m\dot{v} + bv = u
$$

Suppose the cart starts at rest and at $t = 0$ you start pushing with a constant force
$u_0$, a **step input**. The solution is

$$
v(t) = \frac{u_0}{b}\left(1 - e^{-t/\tau}\right),
\qquad
\tau = \frac{m}{b}
$$

Two numbers capture everything about this response:

- **Steady-state value** $u_0/b$: where the speed ends up. Drag eventually balances the
  push.
- **Time constant** $\tau$ (seconds): how fast it gets there. A heavier cart (larger $m$)
  responds more slowly; more drag (larger $b$) makes it settle faster, at a lower speed.

The time constant has a precise meaning:

| Time elapsed | Fraction of final value reached |
|---|---|
| $\tau$ | 63% |
| $2\tau$ | 86% |
| $3\tau$ | 95% |
| $4\tau$ | 98% |

A useful rule of thumb: a first-order system has effectively finished responding after
about four time constants. Many things behave this way: a cup of coffee cooling, a
capacitor charging, a motor spinning up against friction.

## Second-order systems

Add a spring to the cart and things get more interesting. The system can now store
energy in two places, as motion and as spring stretch, and trade it back and forth.
That trade is what makes oscillation possible.

### The mass-spring-damper

A block of mass $m$ slides on a frictionless surface. A spring with stiffness $k$
connects it to a wall, a damper (think of a shock absorber) with coefficient $b$
resists its motion, and we can push on it with a force $u$.

Let $x(t)$ be the block's displacement from its resting position. Three forces act on
it:

- **The spring** pulls it back toward rest with a force proportional to displacement: $-kx$.
- **The damper** opposes motion with a force proportional to velocity: $-b\dot{x}$.
- **The input** pushes it: $u$.

Newton's second law, $m\ddot{x} = \sum F$, gives the governing equation:

$$
m\ddot{x} + b\dot{x} + kx = u
$$

This is a **second-order** equation: it involves $\ddot{x}$. It needs two initial
conditions, a starting position and a starting velocity, so the system has two state
variables. The mass-spring-damper is worth understanding deeply. A robot joint driven by
a motor under feedback control behaves, to a good approximation, exactly like this.

### Natural frequency and damping ratio

Dividing through by $m$ puts the equation in a standard form that shows up throughout
control theory:

$$
\ddot{x} + 2\zeta\omega_n\dot{x} + \omega_n^2 x = \frac{u}{m},
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

When the system is underdamped, it actually oscillates at the **damped natural
frequency** $\omega_d = \omega_n\sqrt{1 - \zeta^2}$, a little slower than $\omega_n$.

### Reading a step response

Apply a constant force and an underdamped system rises, overshoots, rings, and settles.
Engineers summarize that shape with a few standard numbers, and each one maps back to
$\omega_n$ and $\zeta$:

- **Rise time** $t_r$, from 10% to 90% of the final value: $t_r \approx 1.8/\omega_n$.
  Higher natural frequency means a faster system.
- **Overshoot** $M_p$, how far it goes past the final value as a fraction of that value:
  $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$. Overshoot depends *only* on the damping ratio.
- **Settling time** $t_s$, until it stays within 1% of the final value:
  $t_s \approx 4.6/(\zeta\omega_n)$. The product $\zeta\omega_n$ sets how fast the
  oscillation's envelope decays.

The overshoot formula is worth getting a feel for:

| $\zeta$ | 0.1 | 0.3 | 0.5 | 0.7 | 1.0 |
|---|---|---|---|---|---|
| Overshoot | 73% | 37% | 16% | 4.6% | 0% |

These formulas turn vague requirements into numbers. "Rise in under half a second and
overshoot by no more than 5%" becomes "$\omega_n \gtrsim 3.6$ rad/s and
$\zeta \gtrsim 0.7$." Choosing controller gains to hit targets like these is the
subject of Chapter 3.

### Impulse response

A step is a sustained push. An **impulse** is the opposite: a sharp strike, a large
force over a very short time, like a hammer tap. What matters is the impulse $J$, the
force integrated over the strike. It changes the block's velocity instantly by
$\Delta v = J/m$ without moving it.

Starting from rest, an underdamped mass-spring-damper struck with impulse $J$ responds
with

$$
x(t) = \frac{J}{m\,\omega_d}\, e^{-\zeta\omega_n t} \sin(\omega_d t)
$$

a sine wave at $\omega_d$ inside a decaying exponential envelope. The impulse response
is the system's fingerprint: Chapter 2 will show that it encodes everything about how a
linear system responds to *any* input.

### Try it

The block has mass $m = 1\text{ kg}$. Press **Impulse** to strike it. Here
$J = 1.5\text{ N·s}$, so each strike adds $1.5$ m/s to its velocity. Change $k$ and
$b$ at any time, even mid-swing, and watch how $\zeta$ changes the response.

- Set $b = 0$. The block oscillates forever.
- For $k = 10$ N/m, what value of $b$ gives critical damping? Check your answer
  against $\zeta = b/(2\sqrt{km})$.
- With $b = 0$, press Impulse repeatedly in time with the swing. The amplitude grows:
  this is resonance.

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

## State space

Solving differential equations by hand works for textbook examples, but a robot arm has
dozens of coupled equations. We need a uniform representation that a computer can
handle. That representation is **state space**, and it turns calculus into linear
algebra.

### From one $N$th-order equation to $N$ first-order equations

The trick is to give every derivative but the highest its own name. For the
mass-spring-damper, define two state variables:

$$
x_1 = x \quad \text{(position)},
\qquad
x_2 = \dot{x} \quad \text{(velocity)}
$$

Then the single second-order equation becomes two first-order ones:

$$
\dot{x}_1 = x_2,
\qquad
\dot{x}_2 = -\frac{k}{m}x_1 - \frac{b}{m}x_2 + \frac{1}{m}u
$$

The first equation is just the definition of velocity. The second is Newton's law,
solved for acceleration. The same recipe works for any order: an $N$th-order equation
becomes $N$ first-order equations, one per derivative.

### The matrix form

Stack the state variables into a **state vector** $\mathbf{x} = [x_1,\ x_2]^T$ (bold, to
tell it apart from the displacement $x$) and the equations become one matrix equation:

$$
\dot{\mathbf{x}} = A\mathbf{x} + Bu,
\qquad
y = C\mathbf{x} + Du
$$

$$
A = \begin{bmatrix} 0 & 1 \\ -k/m & -b/m \end{bmatrix},
\qquad
B = \begin{bmatrix} 0 \\ 1/m \end{bmatrix},
\qquad
C = \begin{bmatrix} 1 & 0 \end{bmatrix},
\qquad
D = 0
$$

Each matrix has a job:

- $A$ (the **system matrix**) describes how the state evolves on its own. All of the
  system's natural behavior, its frequencies and damping, lives in $A$.
- $B$ (the **input matrix**) describes how inputs push the state.
- $C$ (the **output matrix**) picks out what we measure. Here it selects the position.
- $D$ (the **feedthrough matrix**) captures any direct path from input to output. It's
  zero for most mechanical systems.

This form scales without changing shape. A 7-joint robot arm linearized around a pose
has a 14-element state vector (seven angles, seven velocities) and a $14 \times 14$ $A$
matrix, but the equation is still $\dot{\mathbf{x}} = A\mathbf{x} + Bu$.

!!! tip "For software engineers"
    State space is the representation your code will use. In C++ with Eigen, the
    mass-spring-damper is a few lines:

    ```cpp
    #include <Eigen/Dense>

    const double m = 1.0, b = 1.0, k = 10.0;
    Eigen::Matrix2d A;
    A << 0.0,    1.0,
         -k / m, -b / m;
    const Eigen::Vector2d B(0.0, 1.0 / m);

    Eigen::Vector2d x(1.0, 0.0);  // state: [position, velocity]
    const double dt = 0.001, u = 0.0;
    for (int i = 0; i < 10000; ++i) {
      x += dt * (A * x + B * u);  // one forward Euler step (see "Discrete time" below)
    }
    ```

    Swap in different matrices and the same loop simulates a different system.

## Linearization

Real systems are rarely linear. Robot arms certainly aren't: gravity's effect on a joint
depends on the sine of its angle. In general, a system's state evolves according to
some nonlinear function,

$$
\dot{\mathbf{x}} = f(\mathbf{x}, u)
$$

and the matrix form above doesn't directly apply. But zoom in close enough to any smooth
curve and it looks like a straight line. **Linearization** applies that idea to dynamic
systems.

### Equilibrium points

An **equilibrium** is a state $\bar{\mathbf{x}}$ and input $\bar{u}$ where nothing changes:
$f(\bar{\mathbf{x}}, \bar{u}) = 0$. Near an equilibrium, write the state as a small
deviation $\delta\mathbf{x} = \mathbf{x} - \bar{\mathbf{x}}$ and the input as
$\delta u = u - \bar{u}$. A first-order Taylor expansion gives a linear system for the
deviations:

$$
\delta\dot{\mathbf{x}} \approx A\,\delta\mathbf{x} + B\,\delta u,
\qquad
A = \left.\frac{\partial f}{\partial \mathbf{x}}\right|_{\bar{\mathbf{x}}, \bar{u}},
\qquad
B = \left.\frac{\partial f}{\partial u}\right|_{\bar{\mathbf{x}}, \bar{u}}
$$

$A$ and $B$ are matrices of partial derivatives, called **Jacobians**, evaluated at the
equilibrium. (Jacobians return in Chapter 4, where they relate joint motion to hand
motion.)

### Example: a pendulum

A rod of length $l$ with a mass $m$ at its tip swings about a motor-driven pivot. With
viscous friction $b$ at the pivot and motor torque $\tau$, its equation of motion is

$$
ml^2\ddot{\theta} + b\dot{\theta} + mgl\sin\theta = \tau
$$

The $\sin\theta$ makes it nonlinear. With state $\mathbf{x} = [\theta,\ \dot{\theta}]^T$
and input $u = \tau$,

$$
f(\mathbf{x}, u) =
\begin{bmatrix} \dot{\theta} \\ \dfrac{u - b\dot{\theta} - mgl\sin\theta}{ml^2} \end{bmatrix},
\qquad
A = \begin{bmatrix} 0 & 1 \\ -\dfrac{g}{l}\cos\bar{\theta} & -\dfrac{b}{ml^2} \end{bmatrix},
\qquad
B = \begin{bmatrix} 0 \\ \dfrac{1}{ml^2} \end{bmatrix}
$$

With zero torque, the pendulum has two equilibria:

- **Hanging down** ($\bar{\theta} = 0$): $\cos\bar{\theta} = 1$, so the bottom-left entry
  of $A$ is $-g/l$. Compare with the mass-spring-damper's $-k/m$: gravity acts like a
  spring pulling the pendulum back, and it swings at $\omega_n = \sqrt{g/l}$.
- **Balanced upright** ($\bar{\theta} = \pi$): $\cos\bar{\theta} = -1$, so the entry flips
  to $+g/l$. That's a "negative spring" that pushes the pendulum *away* from equilibrium.
  The slightest disturbance and it falls. Chapter 2 gives the precise test for this kind
  of instability.

Linearization is only an approximation, accurate for small deviations. Replacing
$\sin\theta$ with $\theta$ is off by about 1% at 14° and about 5% at 30°. That's why
controllers designed with linear tools work best when they keep the system near its
operating point, and why a robot controller often re-linearizes as the arm moves.

## Discrete time

So far time has been continuous. Computers aren't: they do things in steps. That
matters in two places.

- **Simulation:** a simulator advances the state by a time step $\Delta t$ at a time.
- **Control:** a controller reads its sensors, computes a command, and sends it to the
  motors once per cycle, every $T$ seconds. Between updates the command is held constant,
  which is called a **zero-order hold**.

Both raise the same question: what happens when you replace smooth time with steps?

### Forward Euler

The simplest way to step a system forward is to assume the derivative stays constant
over one step:

$$
\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta t\, f(\mathbf{x}_k, u_k)
$$

This is the **forward Euler** method, and it's the line inside the loop of the Eigen
example above. For a linear system it becomes a matrix update:

$$
\mathbf{x}_{k+1} = (I + \Delta t\, A)\,\mathbf{x}_k + \Delta t\, B\, u_k
$$

It's simple, and it can fail badly.

### Time-step stability

Apply forward Euler to the cart with drag, with no input: $\dot{v} = -v/\tau$. Each step
multiplies the speed by the same factor:

$$
v_{k+1} = \left(1 - \frac{\Delta t}{\tau}\right) v_k
$$

The real cart's speed decays smoothly to zero. The simulated one does something that
depends on the step size:

- $\Delta t < \tau$: the factor is between 0 and 1, so the speed decays. Good.
- $\tau < \Delta t < 2\tau$: the factor is negative, so the simulated speed flips sign
  every step. The simulation oscillates, even though the real system can't.
- $\Delta t > 2\tau$: the factor's magnitude exceeds 1, so the simulated speed grows
  without bound. The simulation is **numerically unstable**.

Oscillating systems are even less forgiving. For the mass-spring-damper, forward Euler is
stable only when

$$
\Delta t < \frac{2\zeta}{\omega_n}
$$

With no damping ($\zeta = 0$), no time step is small enough: every step adds a little
energy, and the oscillation grows forever. For the widget's default settings
($k = 10$ N/m, $b = 1$ N·s/m) the limit is $\Delta t < 0.1$ s, much less than the
period of the oscillation.

The lesson: **the time step must be small compared to the system's fastest time scale**,
its smallest $\tau$ or $1/\omega_n$. Stiff springs and light masses make time scales
short, which is why physics engines struggle with stiff contacts.

### Better integrators

Forward Euler is rarely the right choice in practice.

- **Runge-Kutta 4 (RK4)** evaluates the derivative four times per step and combines
  the results. It's far more accurate, and it handles undamped oscillators as long as
  $\omega_n \Delta t < 2.8$. The widget above uses RK4 with $\Delta t = 1$ ms, far inside
  that limit.
- **Exact discretization.** For a linear system with a zero-order-hold input, the
  update can be computed exactly using the matrix exponential, $\mathbf{x}_{k+1} =
  e^{A\Delta t}\mathbf{x}_k + \dots$. It's exact at any step size, and it's the standard
  way to convert a continuous-time model for digital control design.

A controller's update rate raises the same issues, from the other side: a controller
that samples too slowly can destabilize a system that would be perfectly stable under
continuous control. Chapter 3 shows how the loop rate limits how aggressive feedback can
be.

## Summary

- A dynamic system's **state** is the minimal information needed to predict its future.
- **First-order** systems are characterized by a time constant $\tau$; they finish
  responding in about $4\tau$.
- **Second-order** systems are characterized by a natural frequency $\omega_n$ and a
  damping ratio $\zeta$. Overshoot depends only on $\zeta$; speed depends on $\omega_n$.
- Any $N$th-order linear system can be written in **state-space** form,
  $\dot{\mathbf{x}} = A\mathbf{x} + Bu$, the representation robotics software uses.
- Nonlinear systems can be **linearized** around an equilibrium, using Jacobians.
- Simulating or controlling in **discrete time** requires a time step that's small
  compared to the system's fastest dynamics.

## Further reading

- Franklin, Powell, and Emami-Naeini, *Feedback Control of Dynamic Systems*, covers
  dynamic response, step-response specifications, and state space in depth. It writes
  the state equations as $\dot{\mathbf{x}} = F\mathbf{x} + Gu$, $y = H\mathbf{x} + Ju$;
  this course uses $A$, $B$, $C$, $D$.
- Spong, Hutchinson, and Vidyasagar, *Robot Modeling and Control*, is the main reference
  for the robotics chapters of this course, and its notation is the one we follow.

!!! note "Lab: `time_domain` (coming soon)"
    The C++ lab for this chapter simulates the mass-spring-damper open loop and logs its
    step and impulse responses to Rerun, so you can compare them with the formulas above.
