# Solving Linear Systems

Many problems in this course come down to: given a matrix $A$ and a vector $\mathbf{b}$,
find $\mathbf{x}$ such that

$$
A\mathbf{x} = \mathbf{b}
$$

## The inverse

If $A$ is square and **invertible**, there is a matrix $A^{-1}$ with $A^{-1}A = I$, and the
unique solution is $\mathbf{x} = A^{-1}\mathbf{b}$.

!!! tip "In code"
    Don't form the inverse explicitly. Ask a solver instead, which is faster and more
    accurate: `Eigen::VectorXd x = A.colPivHouseholderQr().solve(b);`

## The determinant

The **determinant** of a square matrix is a single number. For a $2 \times 2$ matrix,

$$
\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
$$

Geometrically, it's how much $A$ scales area (or volume). If $\det A = 0$, $A$ squashes
space flat, information is lost, and $A$ has no inverse. Such a matrix is **singular**.

## Rank and null space

The **rank** of a matrix is the number of independent directions it can produce: the
dimension of the set of all possible outputs $A\mathbf{x}$. A matrix that reaches every
direction it could is **full rank**.

The **null space** is the set of inputs that $A$ maps to zero: all $\mathbf{n}$ with
$A\mathbf{n} = 0$. If it contains anything besides zero, solutions aren't unique: if
$\mathbf{x}$ solves $A\mathbf{x} = \mathbf{b}$, so does $\mathbf{x} + \mathbf{n}$.

## The pseudo-inverse

When $A$ isn't square, or isn't invertible, the **pseudo-inverse** $A^+$ gives the best
available answer $\mathbf{x} = A^+\mathbf{b}$:

- **More equations than unknowns** (tall $A$, usually no exact solution): $A^+\mathbf{b}$
  is the **least-squares** solution, the one that makes $|A\mathbf{x} - \mathbf{b}|$ as small as
  possible. For full-rank $A$, $A^+ = (A^TA)^{-1}A^T$.
- **Fewer equations than unknowns** (wide $A$, infinitely many solutions): $A^+\mathbf{b}$ is
  the solution with the smallest $|\mathbf{x}|$. For full-rank $A$, $A^+ = A^T(AA^T)^{-1}$.

In Eigen: `A.completeOrthogonalDecomposition().pseudoInverse()`.
