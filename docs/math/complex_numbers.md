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

| | $\omega = 0$ | $\omega \neq 0$ |
|---|---|---|
| $\sigma < 0$ | decays | decaying oscillation |
| $\sigma = 0$ | constant | steady oscillation |
| $\sigma > 0$ | grows | growing oscillation |

This table comes back throughout the course: the real part of $s$ decides decay or
growth, and the imaginary part decides oscillation.

In C++, `std::complex<double>` provides all of this, including `std::abs`, `std::arg`,
and `std::exp`.
