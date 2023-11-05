import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Parameters
NUM_PEOPLE = 100
SIMULATION_ROUNDS = 50
DECISION_IMPACT = 0.3
EMOTIONAL_CONTAGION_FACTOR = 0.1
RANDOM_EVENT_PROBABILITY = 0.05
RIPPLE_EFFECT_DECAY = 0.1

# Create a society with a Watts-Strogatz small-world network
society_graph = nx.watts_strogatz_graph(n=NUM_PEOPLE, k=6, p=0.1)
happiness = np.random.uniform(0.5, 1.0, NUM_PEOPLE)


def simulate_trolley_problem():
    global happiness
    # Trolley problem decision
    group_saved = np.random.choice(NUM_PEOPLE, size=3, replace=False)
    individual_sacrificed = np.random.choice(NUM_PEOPLE)

    # Update happiness levels
    happiness[group_saved] += DECISION_IMPACT
    happiness[individual_sacrificed] -= DECISION_IMPACT * 3

    # Ripple effect simulation
    for _ in range(SIMULATION_ROUNDS):
        for i in range(NUM_PEOPLE):
            neighbors = list(society_graph.neighbors(i))
            happiness[i] += np.sum((happiness[neighbors] - happiness[i]) * EMOTIONAL_CONTAGION_FACTOR)
            if np.random.rand() < RANDOM_EVENT_PROBABILITY:
                happiness[i] += np.random.uniform(-RIPPLE_EFFECT_DECAY, RIPPLE_EFFECT_DECAY)
            happiness[i] = np.clip(happiness[i], 0, 1)

    return happiness


# Prepare initial state for comparison
initial_happiness = happiness.copy()


# GUI functions
def update_plots():
    # Simulate the trolley problem to update happiness values
    final_happiness = simulate_trolley_problem()

    # Calculate net change in happiness
    net_change = np.sum(final_happiness) - np.sum(initial_happiness)

    # Update the bar chart
    bar_chart_ax.clear()
    bar_chart_ax.bar(['Initial', 'Final'], [np.sum(initial_happiness), np.sum(final_happiness)],
                     color=['blue', 'green'])
    bar_chart_ax.set_ylabel('Total Happiness')
    bar_chart_ax.set_title('Net Change in Happiness: {:.2f}'.format(net_change))
    bar_chart_ax.text(1, np.sum(final_happiness), f'{net_change:.2f}', ha='center', va='bottom')

    # Update the network plot
    network_ax.clear()
    pos = nx.spring_layout(society_graph)
    nx.draw(society_graph, pos, ax=network_ax, node_size=50, node_color=happiness, cmap=plt.cm.viridis,
            edge_color='gray')
    network_ax.set_title('Society Network Happiness Levels')

    # Redraw the canvas
    canvas.draw_idle()


# Create the main window
root = tk.Tk()
root.title('Trolley Problem Simulation')

# Create the matplotlib figure and subplots
fig = Figure(figsize=(12, 6))
bar_chart_ax = fig.add_subplot(121)
network_ax = fig.add_subplot(122)

# Create the canvas and place it on the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add a button to update the plots
update_button = tk.Button(root, text="Simulate Trolley Problem", command=update_plots)
update_button.pack(side=tk.BOTTOM)

# Initial plots
update_plots()

# Display the GUI
root.mainloop()