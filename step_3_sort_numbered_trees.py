def cluster_lines_by_z(input_file, output_file):
    from collections import defaultdict

    # Read lines from the input file and cluster them
    clusters = defaultdict(list)
    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:  # Avoid empty lines
                z_count = line.count('z')
                clusters[z_count].append(line)

    # Sort clusters by size in descending order
    sorted_clusters = sorted(clusters.values(), key=len, reverse=True)

    # Write the sorted clusters to the output file
    with open(output_file, 'w') as outfile:
        for i, cluster in enumerate(sorted_clusters):
            #outfile.write(f"Cluster size: {len(cluster)}\n")
            for line in cluster:
                outfile.write(line + '\n')
            #if i < len(sorted_clusters) - 1:
            #    outfile.write('\n')  # Add a newline between clusters except after the last one

# Example usage
input_file = 'numbered_500k_trees.txt'
output_file = 'numbered_sorted_500k_trees.txt'
cluster_lines_by_z(input_file, output_file)
