import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],
                  index=['cobra', 'viper', 'sidewinder'],
                  columns=['max_speed', 'shield'])

# Example data
import matplotlib.pyplot as plt
import numpy as np

# Sample data for two gameweeks
import matplotlib.pyplot as plt
import numpy as np

# Sample data for two gameweeks
gw1_data = [10, 20, 15, 25]  # Data for gameweek 1
gw2_data = [15, 25, 20, 30]  # Data for gameweek 2
labels = ['Player 1', 'Player 2', 'Player 3', 'Player 4']  # X-labels

# Set the width of the bars
bar_width = 0.35

# Set the positions for the bars
x = np.arange(len(labels))

# Plot the bars for gameweek 1
plt.bar(x, gw1_data, bar_width, label='Gameweek 1', color='blue')

# Plot the bars for gameweek 2, stacked on top of gameweek 1
plt.bar(x, gw2_data, bar_width, label='Gameweek 2', color='orange', bottom=gw1_data)

# Add labels, title, and legend
plt.xlabel('Players')
plt.ylabel('Points')
plt.title('Points Comparison Between Two Gameweeks')
plt.xticks(x, labels)  # Set x-labels
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

