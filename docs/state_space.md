# State Space, Stability, and Linearization

A robot arm has dozens of coupled equations of motion, so we need one uniform form that
software can handle. That form is **state space**.

## From one equation to many

Give every derivative except the highest its own name. For the mass-spring-damper, let
$x_1 = x$ (position) and $x_2 = \dot{x}$ (velocity):

$$
\dot{x}_1 = x_2,
\qquad
\dot{x}_2 = -\frac{k}{m}x_1 - \frac{b}{m}x_2 + \frac{1}{m}u
$$

An $N$th-order equation always becomes $N$ first-order equations this way.

## The matrix form

!!! info "Refresher"
    A matrix times a vector takes the dot product of each row with the vector.
    See [Vectors and Matrices](math/vectors_matrices.md).

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

- $A$ holds the system's own dynamics.
- $B$ says how the input pushes the state.
- $C$ picks out the measured output, here the position. $D$ is a direct path from input
  to output, usually zero.

A 7-joint arm needs bigger matrices, but the equation keeps the same shape.

## Stability

!!! info "Refresher"
    The solution of $\dot{\mathbf{x}} = A\mathbf{x}$ is a sum of modes $e^{\lambda t}\mathbf{v}$, one
    per eigenvalue of $A$. See [Differential Equations](math/differential_equations.md).

The eigenvalues of the mass-spring-damper's $A$ are the roots of

$$
\det(sI - A) = s^2 + \frac{b}{m}s + \frac{k}{m} = 0
$$

which is the characteristic equation from the previous page, divided by $m$. So the
eigenvalues of $A$ *are* the characteristic roots, and they decide how the system behaves:

- Every eigenvalue has a negative real part: the system returns to rest. It's
  **stable**.
- Any eigenvalue has a positive real part: some motion grows without bound. It's
  **unstable**.
- Eigenvalues on the imaginary axis, with none to the right: it oscillates forever
  without growing or decaying, like the undamped spring.

In the complex plane, stable means every eigenvalue sits in the left half. This figure
from [Complex Numbers](math/complex_numbers.md) shows the motion each location produces,
and that eigenvalues farther left decay faster:

![Root positions in the complex plane and the signal each produces](assets/figures/s_plane_map.svg#only-light)
![Root positions in the complex plane and the signal each produces](assets/figures/s_plane_map_dark.svg#only-dark)

In code, that's one call:

```cpp
#include <Eigen/Dense>

const double m = 1.0, b = 1.0, k = 10.0;
Eigen::Matrix2d A;
A << 0.0,    1.0,
     -k / m, -b / m;
Eigen::EigenSolver<Eigen::Matrix2d> solver(A);
// solver.eigenvalues() = -0.5 ± 3.12j: negative real parts, so stable
```

## Linearization

!!! info "Refresher"
    Near a point, $\mathbf{f}(\bar{\mathbf{x}} + \delta\mathbf{x}) \approx \mathbf{f}(\bar{\mathbf{x}}) + J\,\delta\mathbf{x}$,
    where $J$ is the Jacobian. See [Partial Derivatives and Jacobians](math/jacobians.md).

Real systems are nonlinear: $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, u)$. Near an
**equilibrium**, a state where $\mathbf{f} = 0$ and nothing changes, they behave almost
linearly, with $A$ equal to the Jacobian $\partial\mathbf{f}/\partial\mathbf{x}$ there.

A pendulum of length $l$ with mass $m$ at its tip, pivot friction $b$, and motor torque
$\tau$ follows

$$
ml^2\ddot{\theta} + b\dot{\theta} + mgl\sin\theta = \tau
$$

![A pendulum hanging down, which is stable, and balanced upright, which is unstable](assets/figures/pendulum.svg#only-light)
![A pendulum hanging down, which is stable, and balanced upright, which is unstable](assets/figures/pendulum_dark.svg#only-dark)

The figure shows both equilibria: hanging down, where gravity pulls it back, and balanced
upright, where gravity pulls it away.

Linearizing around an angle $\bar{\theta}$ gives

$$
A = \begin{bmatrix} 0 & 1 \\ -\dfrac{g}{l}\cos\bar{\theta} & -\dfrac{b}{ml^2} \end{bmatrix}
$$

- **Hanging down** ($\bar{\theta} = 0$): the bottom-left entry is $-g/l$, just like the
  spring's $-k/m$. Gravity acts as a spring, the eigenvalues have negative real parts, and
  the pendulum is stable.
- **Balanced upright** ($\bar{\theta} = \pi$): the entry flips to $+g/l$. The
  characteristic equation becomes $s^2 + \frac{b}{ml^2}s - \frac{g}{l} = 0$, which always has
  one positive real root. The pendulum is unstable: it falls.

The approximation only holds near the equilibrium, which is why controllers built on it
work best when they keep the system close to its operating point.

## Further reading

- Franklin, Powell, and Emami-Naeini, *Feedback Control of Dynamic Systems*. It writes
  state space as $F, G, H, J$ where we use $A, B, C, D$.
- Spong, Hutchinson, and Vidyasagar, *Robot Modeling and Control*, whose notation this
  course follows.

!!! note "Lab: `time_domain` (coming soon)"
    The C++ lab simulates the mass-spring-damper open loop and logs its step and impulse
    responses to Rerun.
