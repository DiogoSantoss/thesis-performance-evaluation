import json
import numpy as np
import matplotlib.pyplot as plt

# Function to read a JSON file
def read_json_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Function to calculate the average values and standard deviations for each key
def calculate_stats(data):
    stats = {}
    for key, values in data.items():
        stats[key] = {
            'mean': np.mean(values),
            'std_dev': np.std(values)
        }
    return stats

# Main function to plot the data
def plot_data(file_paths):
    stats_list = []
    file_names = []

    for file_path in file_paths:
        data = read_json_file(file_path)
        stats = calculate_stats(data)
        stats_list.append(stats)
        file_names.append(file_path.split('/')[-1])

    keys = sorted(stats_list[0].keys())
    x = np.arange(len(keys))

    fig, ax = plt.subplots()

    for i, stats in enumerate(stats_list):
        means = [stats[key]['mean'] for key in keys]
        std_devs = [stats[key]['std_dev'] for key in keys]
        ax.errorbar(x, means, yerr=std_devs, fmt='o', linestyle=':', label=file_names[i].split('.')[0].split('_')[-1], capsize=5)

    ax.set_xlabel('Cluster Size')
    ax.set_ylabel('Latency (ms)')
    ax.set_title('Latency with increasing cluster size')
    ax.set_xticks(x)
    # Keys are 'f' but we want to display 'n', so we should compute n = 3f+1
    keys = [str(3 * int(key) + 1) for key in keys]
    ax.set_xticklabels(keys)
    ax.legend(loc='upper left')

    plt.show()

file_paths = [
    'data/cluster_size_qbft2.json',
    'data/cluster_size_alea2.json',
    'data/cluster_size_alea-f-1.json'
]

# Run the script
plot_data(file_paths)
