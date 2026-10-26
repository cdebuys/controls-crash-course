# Partial Derivatives and Jacobians

## Partial derivatives

For a function of several variables, the **partial derivative** with respect to one of
them is the rate of change when only that variable moves and the rest are held fixed:

$$
f(x, y) = x^2 y
\qquad\Longrightarrow\qquad
\frac{\partial f}{\partial x} = 2xy,
\quad
\frac{\partial f}{\partial y} = x^2
$$

## Linear approximation

Near a point, a smooth function looks like a straight line (or a flat plane). For one
variable,

$$
f(\bar{x} + \delta x) \approx f(\bar{x}) + f'(\bar{x})\,\delta x
$$

For example, $\sin\theta \approx \theta$ near $\theta = 0$:

![sin theta and its tangent line theta agree near zero](../assets/figures/linear_approximation.svg#only-light)
![sin theta and its tangent line theta agree near zero](../assets/figures/linear_approximation_dark.svg#only-dark)

The dashed tangent line and the curve are almost identical inside the shaded band, and
drift apart outside it. With several variables, each one contributes its own partial derivative times its own
small change.

## The Jacobian

For a function that takes a vector in and gives a vector out, collect all the partial
derivatives into a matrix, the **Jacobian**:

$$
J_{ij} = \frac{\partial f_i}{\partial x_j},
\qquad
\mathbf{f}(\bar{\mathbf{x}} + \delta\mathbf{x}) \approx \mathbf{f}(\bar{\mathbf{x}}) + J\,\delta\mathbf{x}
$$

Each row is an output and each column is an input. The Jacobian answers: if I nudge the
inputs a little, how do the outputs move?

## Example

Converting polar coordinates $(r, \theta)$ to a position $(r\cos\theta,\ r\sin\theta)$:

$$
J = \begin{bmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{bmatrix},
\qquad
\det J = r
$$

A small circle of input changes around a point maps to an ellipse of position changes.
It's stretched by $r$ in the $\theta$ direction, because turning by $\theta$ moves the point
along an arc of radius $r$:

![A small circle of inputs maps through the Jacobian to an ellipse of outputs](../assets/figures/jacobian_ellipse.svg#only-light)
![A small circle of inputs maps through the Jacobian to an ellipse of outputs](../assets/figures/jacobian_ellipse_dark.svg#only-dark)

At $r = 0$ the determinant is zero, so $J$ is singular: the ellipse collapses to a line,
and changing $\theta$ does nothing to the position. A robot arm's Jacobian works the same way, and Chapter 4 is about exactly
these situations.
