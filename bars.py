import matplotlib.pyplot as plt
import json
import numpy as np
import os

# List of JSON files to be loaded
file_list = [
    'data/qbft_throughput.json',
    'data/alea_throughput.json',
    # Add more file paths here as needed
]

# Function to extract the label from the filename
def extract_label(file_path):
    return os.path.basename(file_path).replace('_throughput.json', '').replace('_', ' ').capitalize()

# Dictionary to hold data from each file
data_dict = {}

# Load data from each JSON file
for file_path in file_list:
    with open(file_path, 'r') as file:
        data_dict[extract_label(file_path)] = json.load(file)

# Extract payload sizes (assumes all files have the same keys)
payload_sizes = sorted(map(int, next(iter(data_dict.values())).keys()))

# Calculate average throughput values for each dataset
average_throughput = {}
for label, data in data_dict.items():
    average_throughput[label] = [sum(data[str(size)]) / len(data[str(size)]) for size in payload_sizes]

# Bar width
bar_width = 0.25

# Positions of the bars on the x-axis
r = np.arange(len(payload_sizes))
positions = [r + i * bar_width for i in range(len(file_list))]

# Plotting the data
plt.figure(figsize=(12, 6))

# Plot bars for each dataset
for pos, (label, averages) in zip(positions, average_throughput.items()):
    plt.bar(pos, averages, width=bar_width, edgecolor='grey', label=label)

# Adding titles and labels
plt.title('Throughput with increasing payload size')
plt.xlabel('Payload Size (bytes)')
plt.ylabel('Throughput (duties/s)')
plt.xticks([r + bar_width * (len(file_list) - 1) / 2 for r in range(len(payload_sizes))], payload_sizes)
plt.legend()

# Displaying the plot
plt.grid(True)
plt.show()
