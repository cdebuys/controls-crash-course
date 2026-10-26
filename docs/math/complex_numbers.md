# Complex Numbers

Control theory describes oscillation with complex numbers. You need four facts.

## The basics

Engineers write $j = \sqrt{-1}$ (reserving $i$ for electric current). A complex number
$z = a + jb$ has a **real part** $a$ and an **imaginary part** $b$, and you can picture it
as the point $(a, b)$ on the **complex plane**.

Arithmetic works as usual, with $j^2 = -1$:

$$
(1 + 2j)(3 - j) = 3 - j + 6j - 2j^2 = 5 + 5j
$$

The **conjugate** flips the sign of the imaginary part: $\bar{z} = a - jb$.

## Polar form

The same point can be described by its distance from the origin and its angle:

$$
|z| = \sqrt{a^2 + b^2},
\qquad
\angle z = \operatorname{atan2}(b, a)
$$

![A complex number as a point with magnitude and angle, and its conjugate](../assets/figures/complex_polar.svg#only-light)
![A complex number as a point with magnitude and angle, and its conjugate](../assets/figures/complex_polar_dark.svg#only-dark)

In the figure, $a$ and $b$ are the point's coordinates, $|z|$ is its distance from the
origin, and the angle is measured from the real axis. The conjugate is the mirror image
across the real axis.

## Euler's formula

$$
e^{j\theta} = \cos\theta + j\sin\theta
$$

So any complex number can be written $z = |z|\,e^{j\angle z}$. Multiplying two complex
numbers then multiplies their magnitudes and adds their angles.

## Complex exponentials in time

Let $s = \sigma + j\omega$. Then

$$
e^{st} = e^{\sigma t}\, e^{j\omega t}
$$

is a point rotating around the origin at $\omega$ rad/s, with a radius $e^{\sigma t}$ that
shrinks or grows. Adding a conjugate pair cancels the imaginary parts and leaves a real
signal:

$$
e^{st} + e^{\bar{s}t} = 2e^{\sigma t}\cos\omega t
$$

That's a cosine whose amplitude follows $e^{\sigma t}$. The dotted envelope is a plain
first-order exponential decay, and the oscillation stays inside it:

![A decaying sinusoid inside its exponential envelope](../assets/figures/decaying_sinusoid.svg#only-light)
![A decaying sinusoid inside its exponential envelope](../assets/figures/decaying_sinusoid_dark.svg#only-dark)

The figure below shows the signal produced by an $s$ in each part of the plane. The faint
dots below the axis are the conjugate partners of the ones above.

![Root positions in the complex plane and the signal each produces](../assets/figures/s_plane_map.svg#only-light)
![Root positions in the complex plane and the signal each produces](../assets/figures/s_plane_map_dark.svg#only-dark)

The real part of $s$ decides decay or growth, and the imaginary part decides oscillation.
This picture comes back throughout the course.

In C++, `std::complex<double>` provides all of this, including `std::abs`, `std::arg`,
and `std::exp`.
