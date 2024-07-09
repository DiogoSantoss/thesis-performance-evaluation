import json
import matplotlib.pyplot as plt
import numpy as np

# List of file names
file_names = [  
    'data/qbft.json',
    'data/alea_base.json', 
    'data/alea_async_coin.json', 
    'data/alea_fast_aba.json', 
    'data/alea_delay_aba.json',
    'data/alea_complete_view.json',
    'data/alea_delay_verification.json',
    'data/alea_multisig.json',
    'data/alea_delay_aba-f+1.json'
]  # Add more file names as needed

# Initialize lists to store data
latency_avg = []
latency_std_devs = []

# Load data from each file
for file_name in file_names:
    with open(file_name, 'r') as json_file:
        loaded_data = json.load(json_file)
    
    latency = np.array(list(loaded_data.values()))

    # Compute average and standard deviation for each point
    latency_avg.append(np.mean(latency, axis=1))
    latency_std_devs.append(np.std(latency, axis=1))

# Ensure all data arrays have the same number of elements
data_lengths = [len(data) for data in latency_avg]
if len(set(data_lengths)) != 1:
    raise ValueError("All data arrays must have the same length")

# Find the load values
load = np.array(list(loaded_data.keys()), dtype=int)

# Sort the data based on load
sort_index = np.argsort(load)
load = load[sort_index]
latency_avg = np.array(latency_avg)[:, sort_index]
latency_std_devs = np.array(latency_std_devs)[:, sort_index]

# Plotting
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
for i in range(len(file_names)):
    plt.errorbar(load, latency_avg[i], yerr=latency_std_devs[i], label=file_names[i].split('/')[1].split('.')[0], fmt='-o', capsize=5)

# Adding labels and legend
plt.xlabel('Number of duties')
plt.ylabel('Latency (ms)')
plt.title('Latency with increasing system load')
plt.legend()

# Display the plot
plt.grid(True)
plt.show()

