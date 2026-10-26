# State Space and Linearization

A robot arm has dozens of coupled equations of motion, so we need one uniform form that a
computer can handle. **State space** is that form, and it turns calculus into linear
algebra.

## From one equation to many

Give every derivative except the highest its own name. For the mass-spring-damper, let
$x_1 = x$ (position) and $x_2 = \dot{x}$ (velocity). The second-order equation becomes two
first-order ones:

$$
\dot{x}_1 = x_2,
\qquad
\dot{x}_2 = -\frac{k}{m}x_1 - \frac{b}{m}x_2 + \frac{1}{m}u
$$

An $N$th-order equation always becomes $N$ first-order equations this way.

## The matrix form

Stack the states into a vector $\mathbf{x} = [x_1,\ x_2]^T$ (bold, to tell it apart from
the displacement $x$):

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

- $A$ holds the system's own dynamics. Its frequencies and damping live here.
- $B$ says how the input pushes the state.
- $C$ picks out the measured output, here the position. $D$ is a direct path from input
  to output, usually zero.

A 7-joint robot arm needs bigger matrices, but the equation keeps the same shape. In C++
with Eigen:

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
  x += dt * (A * x + B * u);  // one forward Euler step (see Discrete Time)
}
```

## Linearization

Real systems are nonlinear: $\dot{\mathbf{x}} = f(\mathbf{x}, u)$. But near an
**equilibrium**, a state where $f = 0$ and nothing changes, they behave almost linearly.
The $A$ matrix is then $\partial f / \partial \mathbf{x}$ evaluated at the equilibrium, a
matrix of partial derivatives called a **Jacobian**.

A pendulum of length $l$ with mass $m$ at its tip, pivot friction $b$, and motor torque
$\tau$ follows

$$
ml^2\ddot{\theta} + b\dot{\theta} + mgl\sin\theta = \tau
$$

Linearizing around an angle $\bar{\theta}$ gives

$$
A = \begin{bmatrix} 0 & 1 \\ -\dfrac{g}{l}\cos\bar{\theta} & -\dfrac{b}{ml^2} \end{bmatrix}
$$

- **Hanging down** ($\bar{\theta} = 0$): the bottom-left entry is $-g/l$, just like the
  spring's $-k/m$. Gravity acts as a spring.
- **Balanced upright** ($\bar{\theta} = \pi$): it flips to $+g/l$, a "negative spring"
  that pushes the pendulum away. It falls. Chapter 2 shows how to test for this.

The approximation only holds near the equilibrium, which is why controllers built on it
work best when they keep the system close to its operating point.
