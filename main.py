import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Parameters
NUM_PEOPLE = 100
SIMULATION_ROUNDS = 50
DECISION_IMPACT = 0.3
EMOTIONAL_CONTAGION_FACTOR = 0.1
RANDOM_EVENT_PROBABILITY = 0.05
RIPPLE_EFFECT_DECAY = 0.1

# Initialize society graph and happiness
society_graph = nx.barabasi_albert_graph(n=NUM_PEOPLE, m=3)
happiness = np.random.uniform(0.5, 1.0, NUM_PEOPLE)

# Set edge weights based on initial happiness
for i, j in society_graph.edges():
    society_graph[i][j]['weight'] = np.mean([happiness[i], happiness[j]])

# Simulate trolley problem and update happiness and graph weights
def simulate_trolley_problem():
    global happiness
    # Trolley problem decision
    group_saved = np.random.choice(NUM_PEOPLE, size=int(NUM_PEOPLE * 0.05), replace=False)
    individual_sacrificed = np.random.choice(NUM_PEOPLE)
    # Update happiness
    happiness[group_saved] += 1
    happiness[individual_sacrificed] -= DECISION_IMPACT * len(group_saved)
    # Contagion and random events
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
    # Update weights based on new happiness
    for i, j in society_graph.edges():
        society_graph[i][j]['weight'] = np.clip(np.mean([happiness[i], happiness[j]]), 0, 1)

# GUI setup
root = tk.Tk()
root.title('Trolley Problem Simulation')
fig, (bar_chart_ax, network_ax) = plt.subplots(1, 2, figsize=(12, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

initial_happiness = happiness.copy()

# Plot update function
def update_plots():
    global initial_happiness
    simulate_trolley_problem()
    final_happiness = happiness.copy()
    net_change = final_happiness.sum() - initial_happiness.sum()
    bar_chart_ax.clear()
    bar_chart_ax.bar(['Initial', 'Final'], [initial_happiness.sum(), final_happiness.sum()], color=['blue', 'green'])
    bar_chart_ax.set_ylabel('Total Happiness')
    bar_chart_ax.set_title(f'Net Change in Happiness: {net_change:.2f}')
    network_ax.clear()
    pos = nx.spring_layout(society_graph, weight='weight')
    nx.draw(society_graph, pos, ax=network_ax, node_size=50, node_color=happiness, cmap=plt.cm.viridis,
            edge_color='gray', alpha=0.7)
    network_ax.set_title('Society Network Happiness Levels')
    canvas.draw_idle()
    initial_happiness = final_happiness

# GUI buttons and initial plot
update_button = tk.Button(root, text="Simulate Trolley Problem", command=update_plots)
update_button.pack(side=tk.BOTTOM)
update_plots()

# Start GUI event loop
root.mainloop()
