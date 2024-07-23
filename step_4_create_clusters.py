import os
import subprocess
import numpy as np


def find_nth(sorted_array, n):
    if n < len(sorted_array):
        return sorted_array[n]
    else:
        return sorted_array[-1]

def percentile_to_index(percentile, size):
    if not (0 <= percentile <= 100):
        raise ValueError("Percentile must be between 0 and 100")
    index = int(round((percentile / 100) * (size - 1)))
    return index

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return sum(1 for line in file)
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return 0
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")
        return 0


def find_nth_percentile(N, val):
    # Open and read the first line of items_list.txt
    with open('items_list.txt', 'r') as f:
        first_line = f.readline().strip()
        lines = f.readlines()

    # Check if the file is empty
    if not lines:
        return None
    else:
        # Create temp_compare.txt with the first line from items_list.txt repeated
        with open('temp_compare.txt', 'w') as temp_compare:
            for line in lines:
                temp_compare.write(first_line + '\n')
            # Write the last line again if the last character is not '\n'
            if not lines[-1].endswith('\n'):
                temp_compare.write(first_line + '\n')
            temp_compare.write(first_line)
    # Run the binary executable
    subprocess.run(['./ted', 'apted', 'linewise', 'items_list.txt', 'temp_compare.txt', 'temp_results.txt'])

    # Read and sort the results from temp_results.txt
    with open('temp_results.txt', 'r') as results_file:
        results = [float(line.strip()) for line in results_file.readlines()]

    results.sort()

    res_med = np.median(results)
    res_mean = np.mean(results)
    print(f"Median distance: {res_med}, Average distance: {res_mean}")
    # Find the Nth percentile

    #percentile_value = np.percentile(results, N)
    percentile_value = find_nth(results, val)

    return percentile_value

def create_cluster(threshold, file_num):
    # Read lines from items_list.txt and results.txt
    with open('items_list.txt', 'r') as items_file:
        items_lines = items_file.readlines()

    with open('temp_results.txt', 'r') as results_file:
        results_lines = results_file.readlines()

    # Ensure corresponding lines
    assert len(items_lines) == len(results_lines), "Mismatch in number of lines between items_list.txt and results.txt"

    # Create the cluster file name
    cluster_file_name = f'cluster_{file_num:03d}.txt'

    # Prepare lists for keeping track of lines to keep in items_list.txt
    remaining_items = []
    cluster_size = 0

    with open(cluster_file_name, 'w') as cluster_file:
        for item_line, result_line in zip(items_lines, results_lines):
            result_value = float(result_line.strip())
            if result_value <= threshold:
                cluster_file.write(item_line)
                cluster_size = cluster_size+1
            else:
                remaining_items.append(item_line)

    # Write remaining lines back to items_list.txt
    with open('items_list.txt', 'w') as items_file:
        items_file.writelines(remaining_items)

    return cluster_size

def init_clusters(N):
    file_num = 1
    numlines = count_lines_in_file('items_list.txt')
    min_size = round(numlines/100)
    val = percentile_to_index(N, numlines)
    while os.path.getsize('items_list.txt') > 0:
        percentile_value = find_nth_percentile(N, val)
        if percentile_value is None:
            break
        if(percentile_value<10):
            percentile_value=10
        if(percentile_value>14):
            percentile_value=14

        subprocess.run(['cp', 'items_list.txt', 'temp_items.txt'])
        cluster_size = create_cluster(percentile_value, file_num)
        while(cluster_size<min_size):
            percentile_value = percentile_value+1
            subprocess.run(['cp', 'temp_items.txt', 'items_list.txt'])
            cluster_size = create_cluster(percentile_value, file_num)

        remainder = count_lines_in_file('items_list.txt')

        if(remainder<min_size):
            min_size = remainder
        # print cluster number and size of cluster
        print(f"Cluster: {file_num}, Threshold: {percentile_value}, Size: {cluster_size}, Remaining: {remainder}")
        # this is so much easier than string manip
        file_num += 1

# main
# 5th percentile would be 50k sentences per million
N = 2

init_clusters(N)
