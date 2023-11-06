# The problem of utilitarian calculation in random scale-free networks

This project is an interactive simulation of the classic ethical dilemma known as the [trolley problem](https://en.wikipedia.org/wiki/Trolley_problem), placed within the framework of an interconnected scale-free societal network. The original problem poses a scenario where a decision must be made whether to take an action that will lead to the death of one person but save several others. This simulation extrapolates that scenario to a networked society, analyzing the broader impact on collective happiness. It is a technical exploration of the implications of utilitarian ethics applied to complex social structures.

## The Problem

The trolley problem is usually prefaced by the assumption that to the person faced with the decision, the people tied to the tracks are of equal 'value'. That is to say that nothing is known about their personal lives, including their tendencies or connections within society. The implications of making a utilitarian decision under this pretence are rather simple, but consider a complex network where each node is an individual with a quantifiable level of happiness. A utilitarian decision is made: the happiness of a certain individual is sacrificed for the greater happiness of others. The questions are:
  - How does this decision affect the overall happiness of the society when considering the interconnectedness of its members?
  - Is this impact reliably predictable? 

## Constructing a simulation 

The challenge is to model the society as a graph of nodes with weighted edges representing relationships. The utilitarian action alters the happiness of certain nodes, and this change propagates through the network. The propagation is subject to the strength of relationships (edge weights) and random life events that may affect the happiness levels of individuals independently of the utilitarian decision. Given the pretence that the person making the decision should have no insight into the connections of the people on the tracks, we need to construct connections in the network to be random and unpredictable.

To achieve this, we define the propagation of happiness as a diffusion process over the network, which is mathematically modeled using principles from graph theory and stochastic processes. The decision's impact is then quantified by comparing the net happiness before and after the action, providing a measure of its utilitarian value.

## Implementation

The technical solution involves creating a dynamic graph model (in this case a [Barabási–Albert model](https://en.wikipedia.org/wiki/Barabási–Albert_model)) and implementing a simulation that factors in both the immediate and secondary effects of the utilitarian decision. This requires crafting algorithms that can handle complex interactions within the graph and evolve the system state in a realistic manner. The core of this is demonstrated in the following pseudocode:

```python
# Pseudocode for the happiness propagation algorithm
initialize graph G with nodes and edges
for each utilitarian action in G:
    apply immediate happiness changes to affected nodes
    for each node in G:
        propagate happiness change through edges
        apply random life events
    calculate net happiness change
```

The simulation is implemented in Python, using libraries such as NetworkX for graph manipulation, Matplotlib for visualization, and NumPy for numerical operations.

## Visual Demonstrations of a single run of the simulation

- **Net change in happiness bar chart**

  ![Screenshot 2023-11-05 192306](https://github.com/olegware/trolley-sim/assets/129217985/766e82fa-8270-46ab-9fad-c61529e2dcea)

- **Post-decision society graph**

  ![Screenshot 2023-11-05 192426](https://github.com/olegware/trolley-sim/assets/129217985/e23c16bf-dd06-4900-bd95-b7dc054364be)

## Findings

- **Results upon running the simulation 1000 times**

  ![Screenshot 2023-11-05 194034](https://github.com/olegware/trolley-sim/assets/129217985/a53e1870-f4e2-4a38-bb27-dfa0ce221832)

The above findings suggest that even in a small society of only 100 people, through the unpredictable nature of connections and the emotional contagion that propagates through them, the true utility of a seemingly obvious utilitarian decision can be significantly undermined. Here lies the problem of utilitarian calculation in complex networks: we cannot reliably foresee the true utility of an action past a pure surface level.
 

## Implications

The crux of this simulation is to illustrate the potential shortcomings of a purely utilitarian approach, especially in complex systems such as human societies where interdependencies can lead to unforeseen consequences. The term **"net happiness"** becomes a nuanced concept when one observes how a positive change for the majority can still lead to a significant negative impact due to the connected nature of individuals.

This simulation provides a platform for deeper analysis and discussion in ethical philosophy, social dynamics, and network theory. It allows us to question whether "the greatest happiness for the greatest number" can sometimes be an oversimplified principle when dealing with the intricate web of social relationships and individual experiences. As for the implications of this on wider society, this idea could contribute to the suggestion that an axiomatic moral framework is more beneficial for society than individual case-by-case utilitarian calculation. 

