import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

# Parameters
NUM_PEOPLE = 100
SIMULATION_ROUNDS = 50
DECISION_IMPACT = 0.5
EMOTIONAL_CONTAGION_FACTOR = 0.1
RANDOM_EVENT_PROBABILITY = 0.05
RIPPLE_EFFECT_DECAY = 0.1
NUM_SIMULATIONS = 1000

# Initialize society graph
society_graph = nx.barabasi_albert_graph(n=NUM_PEOPLE, m=3)


# Simulate trolley problem and update happiness and graph weights
def simulate_trolley_problem(happiness, society_graph):
    for _ in range(SIMULATION_ROUNDS):
        new_happiness = happiness.copy()
        for i in range(NUM_PEOPLE):
            neighbors = list(society_graph.neighbors(i))
            happiness_diff_sum = sum(society_graph[i][n]['weight'] * (happiness[n] - happiness[i]) for n in neighbors)
            new_happiness[i] += EMOTIONAL_CONTAGION_FACTOR * happiness_diff_sum
            if np.random.rand() < RANDOM_EVENT_PROBABILITY:
                new_happiness[i] += np.random.uniform(-RIPPLE_EFFECT_DECAY, RIPPLE_EFFECT_DECAY)
            new_happiness[i] = np.clip(new_happiness[i], 0, 1)  # Ensure happiness is within bounds
        happiness = new_happiness

        # Update graph weights for next round
        for i, j in society_graph.edges():
            society_graph[i][j]['weight'] = np.clip(np.mean([happiness[i], happiness[j]]), 0, 1)

    return happiness


# Store results
total_happiness_changes = []

# Run the simulation 1000 times with a progress bar
for _ in tqdm(range(NUM_SIMULATIONS), desc="Simulating", unit="sim"):
    initial_happiness = np.random.uniform(0.5, 1.0, NUM_PEOPLE)

    # Set edge weights based on initial happiness
    for i, j in society_graph.edges():
        society_graph[i][j]['weight'] = np.mean([initial_happiness[i], initial_happiness[j]])

    final_happiness = simulate_trolley_problem(initial_happiness, society_graph)
    total_happiness_change = final_happiness.sum() - initial_happiness.sum()
    total_happiness_changes.append(total_happiness_change)

# Plot the results
plt.figure(figsize=(10, 6))
plt.hist(total_happiness_changes, bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Net Happiness Change Over 1000 Simulations')
plt.xlabel('Net Change in Happiness')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.axvline(x=np.mean(total_happiness_changes), color='red', linestyle='dashed', linewidth=2)
plt.text(np.mean(total_happiness_changes) + np.mean(total_happiness_changes) / 10,
         max(plt.hist(total_happiness_changes, bins=30)[0]) / 2, f'Mean: {np.mean(total_happiness_changes):.2f}',
         color='red')
plt.show()

# Output a summary of the results
average_change = np.mean(total_happiness_changes)
median_change = np.median(total_happiness_changes)
std_dev_change = np.std(total_happiness_changes)

description = (
    f"Over {NUM_SIMULATIONS} simulations:\n"
    f"- The average net change in happiness was {average_change:.2f}.\n"
    f"- The median net change in happiness was {median_change:.2f}.\n"
    f"- The standard deviation of the net change in happiness was {std_dev_change:.2f}.\n"
)

print(description)