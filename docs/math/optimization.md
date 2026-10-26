# Quadratic Forms and Optimization

## Quadratic forms

For a symmetric matrix $Q$, the expression $\mathbf{x}^T Q \mathbf{x}$ is a single number, a
**quadratic form**. It's the matrix version of $qx^2$. Kinetic energy is one: for a single
mass it's $\tfrac{1}{2}mv^2$, and for a robot arm it's $\tfrac{1}{2}\dot{\mathbf{q}}^T M \dot{\mathbf{q}}$.

$Q$ is **positive definite** if $\mathbf{x}^T Q \mathbf{x} > 0$ for every nonzero $\mathbf{x}$.
Equivalently, all its eigenvalues are positive. Its graph is a bowl with a single lowest
point.

## Minimizing a quadratic

To minimize

$$
f(\mathbf{x}) = \tfrac{1}{2}\mathbf{x}^T Q \mathbf{x} - \mathbf{c}^T\mathbf{x}
$$

with $Q$ positive definite, set every partial derivative to zero. That gives a linear
system, $Q\mathbf{x} = \mathbf{c}$, with one solution: the bottom of the bowl.

## Least squares

When $A\mathbf{x} = \mathbf{b}$ has no exact solution, minimize the error
$|A\mathbf{x} - \mathbf{b}|^2$ instead. This is a quadratic, and setting its derivatives to zero
gives

$$
A^TA\,\mathbf{x} = A^T\mathbf{b}
$$

whose solution is the pseudo-inverse answer from
[Solving Linear Systems](linear_systems.md). Adding a penalty $\lambda^2|\mathbf{x}|^2$ that keeps
$\mathbf{x}$ small gives

$$
(A^TA + \lambda^2 I)\,\mathbf{x} = A^T\mathbf{b}
$$

which always has a solution, even when $A$ is singular. This **damped least squares**
returns in Chapter 4.

## Quadratic programs

A **quadratic program (QP)** minimizes a quadratic subject to linear constraints:
equalities $E\mathbf{x} = \mathbf{d}$ and inequalities $G\mathbf{x} \le \mathbf{h}$. With inequalities
there's no formula; solvers search for the answer iteratively. Chapter 7's whole-body
controller solves a QP every control cycle.
