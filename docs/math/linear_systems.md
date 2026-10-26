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
- The **row space** $C(A^T)$ is every combination of the rows of $A$. Its dimension is
  also $r$.

Each shape in the figure above stands for a whole space of vectors through the origin: a
line, a plane, or a higher-dimensional version. On each side the two spaces are at right
angles: every vector in one is perpendicular to every vector in the other. On the input
side, this follows from $A\mathbf{n} = 0$, which says each row of $A$ has a zero
[dot product](vectors_matrices.md#vectors) with $\mathbf{n}$. Their dimensions also add
up to the full space, so every vector is a sum of one piece from each.

For example, $A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$ keeps the first two
entries of $\mathbf{x}$ and drops the third. Its row space is the $xy$-plane and its null
space is the $z$-axis, as in the figure below:

![An input split into its row-space part in the xy-plane and its null-space part along the z-axis](../assets/figures/plane_and_line.svg#only-light)
![An input split into its row-space part in the xy-plane and its null-space part along the z-axis](../assets/figures/plane_and_line_dark.svg#only-dark)

The dashed lines split the input $\mathbf{x}$ into its part in the plane, $\mathbf{x}_r$
(blue), and its part along the line, $\mathbf{x}_n$ (orange). $A$ keeps $\mathbf{x}_r$
and discards $\mathbf{x}_n$, so $A\mathbf{x} = A\mathbf{x}_r$.

A matrix is **full rank** when $r$ is as large as its shape allows, the smaller of $m$
and $n$. The example above is full rank: its rank is 2, so it reaches every point in its
2D output space. Add a row of zeros, giving
$\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$, and it does the same
thing, but its outputs now live in 3D. It still only reaches the $xy$-plane, so its rank
of 2 falls short of 3: it isn't full rank, and its left null space is the $z$-axis, the
outputs it can never produce. A full-rank $3 \times 3$ matrix, by contrast, reaches all of
3D space and discards nothing.

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
$[2,\ -1]^T$ is in its null space. The figure shows the unit square mapped by an invertible
matrix and by this singular one. The middle panel's matrix has determinant 2.5, so it scales
the square's area by 2.5.

![The unit square mapped by an invertible matrix, and flattened onto a line by a singular one](../assets/figures/determinant_area.svg#only-light)
![The unit square mapped by an invertible matrix, and flattened onto a line by a singular one](../assets/figures/determinant_area_dark.svg#only-dark)

## The pseudo-inverse

When $A$ isn't square, or is singular, the **pseudo-inverse** $A^+$ still gives the best
available answer, $\mathbf{x} = A^+\mathbf{b}$. In terms of the four subspaces:

- **If $\mathbf{b}$ isn't in the column space**, there's no exact solution. $A^+$ solves for
  the closest point in the column space, where the error to $\mathbf{b}$ is perpendicular, as
  in the figure below. That makes $|A\mathbf{x} - \mathbf{b}|$ as small as possible.
  This is the **least-squares** solution. For a tall, full-rank $A$,
  $A^+ = (A^TA)^{-1}A^T$.
- **If the null space isn't just zero**, there are infinitely many solutions. $A^+$ picks
  the one with no null-space part, which lies entirely in the row space and has the
  smallest $|\mathbf{x}|$. For a wide, full-rank $A$, $A^+ = A^T(AA^T)^{-1}$.

The first case, least squares, looks like this:

![Least squares: the closest point to b in the column space, with the error perpendicular](../assets/figures/least_squares_projection.svg#only-light)
![Least squares: the closest point to b in the column space, with the error perpendicular](../assets/figures/least_squares_projection_dark.svg#only-dark)

In Eigen: `A.completeOrthogonalDecomposition().pseudoInverse()`.
