# Eigenvalues and Eigenvectors

Multiplying a vector by a matrix usually changes its direction. An **eigenvector** of $A$
is a special vector whose direction doesn't change; it only gets scaled:

$$
A\mathbf{v} = \lambda\mathbf{v}
$$

The scale factor $\lambda$ is the **eigenvalue** that goes with $\mathbf{v}$.

## Finding them

Rearranging gives $(A - \lambda I)\mathbf{v} = 0$. A nonzero $\mathbf{v}$ can only solve this if
$A - \lambda I$ is singular, so the eigenvalues are the roots of

$$
\det(A - \lambda I) = 0
$$

This is a polynomial in $\lambda$, the **characteristic polynomial**. An $n \times n$
matrix has $n$ eigenvalues (counting repeats). They can be complex; for a real matrix,
complex eigenvalues come in conjugate pairs. Each eigenvector lies in the null space of
$A - \lambda I$.

## Example

$$
A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix},
\qquad
\det(A - \lambda I) = \lambda^2 + 3\lambda + 2 = (\lambda + 1)(\lambda + 2)
$$

So $\lambda_1 = -1$ and $\lambda_2 = -2$. Solving $(A - \lambda I)\mathbf{v} = 0$ for each gives

$$
\mathbf{v}_1 = \begin{bmatrix} 1 \\ -1 \end{bmatrix},
\qquad
\mathbf{v}_2 = \begin{bmatrix} 1 \\ -2 \end{bmatrix}
$$

The figure shows $A$ acting on both eigenvectors and on one other vector,
$\mathbf{w} = [1,\ 0]^T$. Each eigenvector stays on its own line; the eigenvalues here are
negative, so both flip. $\mathbf{w}$ lands on a different line.

![Eigenvectors stay on their own line under A, while another vector turns](../assets/figures/eigenvectors.svg#only-light)
![Eigenvectors stay on their own line under A, while another vector turns](../assets/figures/eigenvectors_dark.svg#only-dark)

## Why they matter

Along an eigenvector, a matrix acts like plain multiplication by a number. That makes
eigenvalues the key to systems of differential equations: in
[Differential Equations](differential_equations.md), each eigenvalue becomes an
exponential $e^{\lambda t}$ in the solution.

In Eigen: `Eigen::EigenSolver<Eigen::MatrixXd> solver(A); solver.eigenvalues();`
