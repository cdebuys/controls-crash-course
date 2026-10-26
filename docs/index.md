# Controls Crash Course

A course on control theory and robot control, from a mass-spring-damper to a walking
humanoid.

## Scope

This is a crash course. Each chapter covers the minimum needed to understand its topic
and leaves out detail you'd need to master it. Every chapter has whole textbooks behind
it; we skip most of that material to keep the course manageable.

## Audience

The course is written for computer science students and graduates, but anyone can use
it. It assumes algebra and trigonometry. Calculus helps, and Chapter 0 covers the math
the course uses. The labs assume some familiarity with programming, but feel free to ask
your favorite LLM to assist you with the examples.

## Outcome

The course ends with whole-body control of a walking humanoid. Before that, Chapter 7
builds the control loop for a simulated 7-DOF arm, using MuJoCo for physics, Pinocchio
for the robot model, and TSID for torques.

## How to use it

- Read the chapters in order.
- Chapter 0 is optional. If it's too much, skip it; later chapters link back to the
  parts they use.
- Use the widgets to try out the ideas in each chapter.
- Labs will be added once the lab environment is ready.

Chapters 2–8 are in progress.

## Chapters

- **0.** [Math Toolkit](math/complex_numbers.md): complex numbers, linear algebra, and
  differential equations, kept to what the course uses. Later chapters link back
  here with short refreshers.
- **1.** Time Domain: [dynamic systems](time_domain.md) and [state space, stability, and
  linearization](state_space.md).
- **2.** Frequency Domain *(coming soon)*: the Laplace transform, transfer functions, poles and
  zeros, and Bode plots.
- **3.** Feedback and Joint Control *(coming soon)*: PID control, root locus, and stability
  margins.
- **4.** Kinematics *(coming soon)*: rotations and transforms, forward kinematics, the
  Jacobian, singularities, inverse kinematics, and redundancy.
- **5.** Rigid-Body Dynamics *(coming soon)*: the manipulator equations, Pinocchio's
  algorithms, and computed-torque control.
- **6.** Task-Space Control *(coming soon)*: operational-space control, null-space
  projection, and impedance control.
- **7.** Task-Space Inverse Dynamics *(coming soon)*: multiple tasks and hard limits
  as a quadratic program, on a 7-DOF arm.
- **8.** Whole-Body Control *(coming soon)*: floating bases, contacts, and balance,
  on a walking humanoid.
