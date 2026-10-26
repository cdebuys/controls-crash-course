# Solving Linear Systems

Many problems in this course come down to: given a matrix $A$ and a vector $\mathbf{b}$,
find $\mathbf{x}$ such that

$$
A\mathbf{x} = \mathbf{b}
$$

If $A$ is $m \times n$, it takes inputs $\mathbf{x}$ with $n$ entries and produces outputs
with $m$ entries. Whether this equation has a solution, and how many, depends on four
sets of vectors that every matrix comes with.

## The four subspaces

![The four fundamental subspaces of A](../assets/figures/four_subspaces.svg#only-light)
![The four fundamental subspaces of A](../assets/figures/four_subspaces_dark.svg#only-dark)

On the output side:

- The **column space** $C(A)$, also called the **range** or **image**, is the set of all
  outputs $A\mathbf{x}$ can produce. Its dimension is the **rank** $r$ of $A$.
- The **left null space** $N(A^T)$ holds the output directions $A$ can never produce. Its
  dimension is $m - r$.

On the input side:

- The **null space** $N(A)$, also called the **kernel**, is the set of inputs $A$ maps to
  zero: all $\mathbf{n}$ with $A\mathbf{n} = 0$. Its dimension is $n - r$.
- The **row space** $C(A^T)$ holds everything else. Its dimension is also $r$.

On each side the two spaces are at right angles, and together they cover everything. So
any input splits as $\mathbf{x} = \mathbf{x}_r + \mathbf{x}_n$, a row-space part plus a
null-space part, and $A\mathbf{x} = A\mathbf{x}_r$: the null-space part contributes nothing.

A matrix is **full rank** when $r$ is as large as its shape allows, the smaller of $m$
and $n$.

## What this means for solving

- A solution exists only if $\mathbf{b}$ is in the column space.
- If the null space contains anything besides zero, solutions aren't unique: if
  $\mathbf{x}$ solves $A\mathbf{x} = \mathbf{b}$, so does $\mathbf{x} + \mathbf{n}$ for any
  $\mathbf{n}$ in the null space.

## Square matrices: the inverse and the determinant

A square matrix is **invertible** when its null space is just zero. Then there's a matrix
$A^{-1}$ with $A^{-1}A = I$, and every $\mathbf{b}$ has exactly one solution,
$\mathbf{x} = A^{-1}\mathbf{b}$.

!!! tip "In code"
    Don't form the inverse explicitly. Ask a solver instead, which is faster and more
    accurate: `Eigen::VectorXd x = A.colPivHouseholderQr().solve(b);`

The **determinant** tests this with a single number. For a $2 \times 2$ matrix,

$$
\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
$$

Geometrically, it's how much $A$ scales area (or volume). If $\det A = 0$, the null
space contains a nonzero vector, so different inputs produce the same output, the input
can't be recovered, and $A$ has no inverse. Such a matrix is **singular**.

For example, in $\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ the second column is twice
the first. Its determinant is $1 \cdot 4 - 2 \cdot 2 = 0$, its rank is 1, and
$[2,\ -1]^T$ is in its null space.

## The pseudo-inverse

When $A$ isn't square, or is singular, the **pseudo-inverse** $A^+$ still gives the best
available answer, $\mathbf{x} = A^+\mathbf{b}$. In terms of the figure:

- **If $\mathbf{b}$ isn't in the column space**, there's no exact solution. $A^+$ solves for
  the closest point that is, which makes $|A\mathbf{x} - \mathbf{b}|$ as small as possible.
  This is the **least-squares** solution. For a tall, full-rank $A$,
  $A^+ = (A^TA)^{-1}A^T$.
- **If the null space isn't just zero**, there are infinitely many solutions. $A^+$ picks
  the one with no null-space part, which lies entirely in the row space and has the
  smallest $|\mathbf{x}|$. For a wide, full-rank $A$, $A^+ = A^T(AA^T)^{-1}$.

In Eigen: `A.completeOrthogonalDecomposition().pseudoInverse()`.
