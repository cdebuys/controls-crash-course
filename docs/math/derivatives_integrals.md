# Derivatives and Integrals

## Derivatives

The **derivative** of $x(t)$ is its instantaneous rate of change, the slope of its graph:
$dx/dt$. Time derivatives are written with dots: $\dot{x}$ for the first derivative,
$\ddot{x}$ for the second. If $x$ is position, $\dot{x}$ is velocity and $\ddot{x}$ is
acceleration.

The rules you'll need:

| Function | Derivative |
|---|---|
| $t^n$ | $n t^{n-1}$ |
| $e^{at}$ | $a e^{at}$ |
| $\sin \omega t$ | $\omega \cos \omega t$ |
| $\cos \omega t$ | $-\omega \sin \omega t$ |
| $f(t)\,g(t)$ (product rule) | $\dot{f} g + f \dot{g}$ |
| $f(g(t))$ (chain rule) | $f'(g(t))\,\dot{g}(t)$ |

Derivatives are also linear: the derivative of $a f + b g$ is $a\dot{f} + b\dot{g}$.

## Integrals

The **integral** accumulates a quantity over time, the area under its graph. It undoes
the derivative:

$$
\int_{t_0}^{t_1} \dot{x}\, dt = x(t_1) - x(t_0)
$$

Integrate velocity and you get the change in position. Integrate force over a short
strike and you get the **impulse**, the change in momentum.

## The software view

On a computer, both become simple loops over small time steps $\Delta t$:

$$
\dot{x}(t_k) \approx \frac{x_{k+1} - x_k}{\Delta t},
\qquad
\int f\, dt \approx \sum_k f(t_k)\, \Delta t
$$
