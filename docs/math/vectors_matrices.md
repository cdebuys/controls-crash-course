# Vectors and Matrices

## Vectors

A **vector** is an ordered list of numbers, written as a column and in bold:
$\mathbf{a} = [a_1,\ a_2,\ a_3]^T$.

The **dot product** multiplies matching entries and adds them up:

$$
\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2 + a_3 b_3 = |\mathbf{a}|\,|\mathbf{b}|\cos\theta
$$

where $\theta$ is the angle between them. A dot product of zero means the vectors are
perpendicular.

The **cross product** exists only in 3D. It gives a vector perpendicular to both inputs,
with length $|\mathbf{a}|\,|\mathbf{b}|\sin\theta$ and direction given by the right-hand rule:

$$
\mathbf{a} \times \mathbf{b} =
\begin{bmatrix} a_2 b_3 - a_3 b_2 \\ a_3 b_1 - a_1 b_3 \\ a_1 b_2 - a_2 b_1 \end{bmatrix}
$$

## Matrices

A **matrix** is a grid of numbers. An $m \times n$ matrix has $m$ rows and $n$ columns.

Multiplying a matrix by a vector takes the dot product of each row with the vector:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\begin{bmatrix} 5 \\ 6 \end{bmatrix}
=
\begin{bmatrix} 1 \cdot 5 + 2 \cdot 6 \\ 3 \cdot 5 + 4 \cdot 6 \end{bmatrix}
=
\begin{bmatrix} 17 \\ 39 \end{bmatrix}
$$

Shapes must line up: an $m \times n$ matrix times an $n$-vector gives an $m$-vector.

The product $AB$ means "apply $B$, then $A$." Order matters: in general $AB \neq BA$.

The **transpose** $A^T$ swaps rows and columns. The **identity** $I$ has ones on the
diagonal and zeros elsewhere, so $I\mathbf{x} = \mathbf{x}$.

## In code

```cpp
#include <Eigen/Dense>

Eigen::Vector3d a(1, 0, 0), b(0, 1, 0);
double d = a.dot(b);            // 0: perpendicular
Eigen::Vector3d c = a.cross(b); // (0, 0, 1)

Eigen::Matrix2d A;
A << 1, 2,
     3, 4;
Eigen::Vector2d y = A * Eigen::Vector2d(5, 6);  // (17, 39)
Eigen::Matrix2d At = A.transpose();
```
