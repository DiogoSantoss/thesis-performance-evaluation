import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

# List of file names to process
file_names = ["data/threshold_timestamps.json", "data/multisig_timestamps.json"]

# Determine the grid size for subplots
num_files = len(file_names)
cols = 2  # Adjust the number of columns as needed
rows = (num_files + cols - 1) // cols  # Calculate the number of rows needed

fig = plt.figure(figsize=(12 * cols, 10 * rows))
gs = gridspec.GridSpec(rows, cols, figure=fig, wspace=0.4, hspace=0.6)

for idx, file_name in enumerate(file_names):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)

    # Convert nanoseconds to milliseconds
    for event in data:
        event['T'] = event['T'] / 1e6

    # Convert timestamps to relative nanoseconds
    start_time = min(event['T'] for event in data)
    for event in data:
        event['T'] = event['T'] - start_time

    # Extract all unique event types
    unique_labels = set(label.split('_', 1)[1] for label in (event['S'] for event in data))

    # Calculate durations and sort by start time
    durations = []
    for label in unique_labels:
        start_events = [event for event in data if event['S'] == f'START_{label}']
        finish_events = [event for event in data if event['S'] == f'FINISH_{label}']
        
        if len(start_events) != len(finish_events):
            print(f"Warning: Mismatched START and FINISH counts for {label} in file {file_name}")
            continue
        
        for start_event, finish_event in zip(start_events, finish_events):
            start = start_event['T']
            finish = finish_event['T']
            duration = finish - start
            durations.append((label, start, finish, duration))

    # Sort by start time and then by duration
    durations.sort(key=lambda x: (x[1], -x[3]))

    # Select the appropriate subplot
    ax = fig.add_subplot(gs[idx])

    # Plot each event as a bar with duration text
    y_labels = []
    for idx, (label, start, finish, duration) in enumerate(durations):
        y_position = idx
        y_label = f'{label}'
        y_labels.append(y_label)
        ax.broken_barh([(start, duration)], (y_position - 0.4, 0.8), facecolors='lightblue', edgecolor='blue')
        ax.text(start + duration / 2, y_position, f'{duration:.3f} ms', va='center', ha='center')

    # Formatting the plot
    ax.set_yticks(range(len(durations)))
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Time (ms)')
    ax.set_title(f'Execution Timeline for {file_name.split("/")[-1].split("_")[0]}')
    ax.grid(True)

# Adjust layout to make room for the y-axis labels and center the plots
plt.tight_layout(pad=3.0)
fig.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.1, wspace=0.4, hspace=0.6)

plt.show()
