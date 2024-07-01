import json
import numpy as np
import matplotlib.pyplot as plt

# Function to read a JSON file
def read_json_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Function to calculate the average values for each key
def calculate_averages(data):
    averages = {}
    for key, values in data.items():
        averages[key] = np.mean(values)
    return averages

# Main function to plot the data
def plot_data(file_paths):
    averages_list = []
    file_names = []

    for file_path in file_paths:
        data = read_json_file(file_path)
        averages = calculate_averages(data)
        averages_list.append(averages)
        file_names.append(file_path.split('/')[-1])

    keys = sorted(averages_list[0].keys())
    x = np.arange(len(keys))

    bar_width = 0.35
    fig, ax = plt.subplots()
    for i, averages in enumerate(averages_list):
        values = [averages[key] for key in keys]
        ax.bar(x + i * bar_width, values, bar_width, label=file_names[i].split('.')[0].split('_')[-1])

    ax.set_xlabel('Cluster Size')
    ax.set_ylabel('Latency (ms)')
    ax.set_title('Latency with increasing cluster size')
    ax.set_xticks(x + bar_width / 2)
    # Keys are 'f' but we want to display 'n', so we should compute n = 3f+1
    keys = [str(3 * int(key) + 1) for key in keys]
    ax.set_xticklabels(keys)
    ax.legend()

    plt.show()

file_paths = [
    'data/cluster_size_qbft2.json',
    'data/cluster_size_alea2.json',
]

# Run the script
plot_data(file_paths)
