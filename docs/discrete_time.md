# Discrete Time

Computers work in steps. A simulator advances the state by a time step $\Delta t$ at a
time, and a controller reads its sensors and updates its command once per cycle.
Replacing smooth time with steps can go wrong.

## Forward Euler

The simplest method assumes the derivative stays constant over one step:

$$
\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta t\, f(\mathbf{x}_k, u_k)
$$

This is the line inside the loop of the Eigen example on the previous page.

## When it blows up

Apply it to the cart with no push, $\dot{v} = -v/\tau$. Each step multiplies the speed by
$1 - \Delta t/\tau$:

- $\Delta t < \tau$: the speed decays, as it should.
- $\tau < \Delta t < 2\tau$: the speed flips sign every step, an oscillation the real
  cart can't do.
- $\Delta t > 2\tau$: the speed grows without bound. The simulation is **numerically
  unstable**.

Oscillators are worse. For an undamped spring, forward Euler adds a little energy every
step, so the oscillation grows no matter how small $\Delta t$ is.

!!! tip "Rule of thumb"
    Keep the time step small compared to the system's fastest time scale: its smallest
    $\tau$ or $1/\omega_n$.

## Better integrators

Runge-Kutta 4 (RK4) evaluates the derivative four times per step and is far more accurate
and stable. The mass-spring-damper widget uses it with a 1 ms step. Chapter 3 covers the
controller side: how a loop's update rate limits its feedback.

## Further reading

- Franklin, Powell, and Emami-Naeini, *Feedback Control of Dynamic Systems*. It writes
  state space as $F, G, H, J$ where we use $A, B, C, D$.
- Spong, Hutchinson, and Vidyasagar, *Robot Modeling and Control*, whose notation this
  course follows.

!!! note "Lab: `time_domain` (coming soon)"
    The C++ lab simulates the mass-spring-damper open loop and logs its step and impulse
    responses to Rerun.
