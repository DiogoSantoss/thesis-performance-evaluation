import os
import json
import re

def read_json_files(directory):
    # Initialize an empty dictionary to store the results
    data_map = {}
    
    # Define the regex pattern to match filenames in the format temp_throughSIZE.json
    pattern = re.compile(r'temp_throughput(\d+)\.json')
    
    # Iterate through files in the specified directory
    for filename in os.listdir(directory):
        print("here1")
        # Check if the filename matches the expected pattern
        match = pattern.match(filename)
        if match:
            print("here")
            # Extract the SIZE part from the filename
            size = match.group(1)
            
            # Construct the full file path
            filepath = os.path.join(directory, filename)
            
            # Open and read the JSON file
            with open(filepath, 'r') as file:
                contents = json.load(file)
                print(contents)
                # Add the contents to the dictionary with SIZE as the key
                data_map[size] = contents
    
    return data_map

# Example usage:
if __name__ == "__main__":
    # Specify the directory containing the JSON files
    directory = '/home/diogo/dev/ist/thesis/graphs/data/'
    
    # Read the JSON files and create the map
    result = read_json_files(directory)
    
    # Write the resulting map to a new JSON file
    with open('data/temp_create_map.json', 'w') as file:
        json.dump(result, file)
