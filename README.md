# Lotka-Volterra Equations: Rabbits and Wolves Example

## Overview
The Lotka-Volterra equations, also known as the predator-prey equations, are a pair of first-order, nonlinear differential equations frequently used to describe the dynamics of biological systems in which two species interact: one as a predator and the other as prey. In this summary, we use the example of rabbits as the prey and wolves as the predators.

## Equations
The Lotka-Volterra equations are given by:

1. **Prey (Rabbits) population growth equation:**
   \[
   \frac{dR}{dt} = \alpha R - \beta RW
   \]
   - \( R \) is the number of rabbits (prey).
   - \( \alpha \) is the natural growth rate of rabbits in the absence of predation.
   - \( \beta \) is the rate at which rabbits are captured by wolves.

2. **Predator (Wolves) population growth equation:**
   \[
   \frac{dW}{dt} = \delta RW - \gamma W
   \]
   - \( W \) is the number of wolves (predators).
   - \( \delta \) is the growth rate of wolves per rabbit eaten.
   - \( \gamma \) is the natural death rate of wolves in the absence of food (rabbits).

## Dynamics
The Lotka-Volterra equations describe the cyclical nature of predator-prey interactions:
- When the rabbit population increases, food for wolves becomes more abundant, leading to an increase in the wolf population.
- As the wolf population grows, they consume more rabbits, leading to a decline in the rabbit population.
- With fewer rabbits to eat, the wolf population begins to decline due to starvation.
- With fewer wolves, the rabbit population begins to recover, and the cycle repeats.


## Simulation 

In this project the Lotka-Volterra emerges from the Rabbit-Wolves (aka prey-predator) system. You can run it and play with it. 
```python
python LotkaVolterra.py
```


### Simulation Results
A simulation of these equations would typically show oscillating populations of rabbits and wolves over time. Key features include:
- **Peaks and Troughs:** Rabbit populations peak before wolf populations, followed by a decline in rabbits as wolves become more abundant.
- **Phase Shift:** The cycles of rabbits and wolves are out of phase, with changes in the rabbit population leading changes in the wolf population.

### Real-World Applications
The Lotka-Volterra model, while simplified, provides a foundation for understanding predator-prey dynamics in ecological studies. It highlights the importance of interaction rates and natural growth/death rates in shaping population dynamics.

### Limitations
The basic Lotka-Volterra model makes several assumptions:
- Unlimited resources for prey (rabbits), except for predation pressure.
- A constant interaction rate between predators and prey.
- No time delays in the response of predator and prey populations.

In real ecosystems, factors such as environmental changes, availability of resources, and more complex interactions can significantly influence population dynamics.

## Conclusion
The Lotka-Volterra equations offer a fundamental framework for studying the interactions between predators and prey, using rabbits and wolves as an illustrative example. By understanding these dynamics, ecologists can better predict and manage wildlife populations and their interactions within ecosystems.


