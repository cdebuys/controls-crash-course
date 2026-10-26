# Differential Equations

A **differential equation** relates a function to its own derivatives. Its solution is a
whole function, not a number, and pinning down a single solution takes one **initial
condition** per order: a starting value for $x$, plus one for $\dot{x}$ if the equation
involves $\ddot{x}$, and so on.

## First order

$$
\dot{x} = ax
\qquad\Longrightarrow\qquad
x(t) = x(0)\, e^{at}
$$

Check it: the derivative of $x(0)e^{at}$ is $a\,x(0)e^{at} = ax$. The solution decays to
zero if $a < 0$ and grows if $a > 0$.

## Second order

Here's the equation of a mass-spring-damper; Chapter 1 explains the physics. For now,
just solve it:

$$
m\ddot{x} + b\dot{x} + kx = 0
$$

Guess $x = e^{st}$. Substituting gives $(ms^2 + bs + k)\,e^{st} = 0$, which holds when

$$
ms^2 + bs + k = 0
\qquad\Longrightarrow\qquad
s = \frac{-b \pm \sqrt{b^2 - 4mk}}{2m}
$$

This is the **characteristic equation**, and its two roots decide the solution:

| Roots | Solution |
|---|---|
| Two different real roots $s_1, s_2$ | $x = c_1 e^{s_1 t} + c_2 e^{s_2 t}$ |
| One repeated real root $s$ | $x = (c_1 + c_2 t)\, e^{st}$ |
| Complex pair $\sigma \pm j\omega$ | $x = e^{\sigma t}(c_1 \cos\omega t + c_2 \sin\omega t)$ |

The constants $c_1, c_2$ come from the initial conditions. As in
[Complex Numbers](complex_numbers.md), the real part of each root decides decay or
growth, and an imaginary part means oscillation. If every root has a negative real part,
the solution decays to zero.

## Systems of equations

Several first-order equations together form a vector equation:

$$
\dot{\mathbf{x}} = A\mathbf{x}
$$

If $A$ has eigenvalues $\lambda_i$ with eigenvectors $\mathbf{v}_i$, the solution is

$$
\mathbf{x}(t) = c_1 e^{\lambda_1 t}\mathbf{v}_1 + c_2 e^{\lambda_2 t}\mathbf{v}_2 + \cdots
$$

Each eigenvector is a **mode** that evolves on its own, at a rate set by its eigenvalue.
For the matrix in the [eigenvalue example](eigenvalues.md#example), the modes are
$e^{-t}$ and $e^{-2t}$: both decay. Same rule as before: if every eigenvalue has a
negative real part, the solution decays to zero.

Equations with an input, such as $m\ddot{x} + b\dot{x} + kx = u(t)$, are handled in
Chapter 2.
