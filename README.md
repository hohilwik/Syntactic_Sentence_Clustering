# Syntactic_Sentence_Clustering
Syntactic Clustering of Sentences in a dataset using tree edit distance

## Pre-processing Steps
- convert JSON format to bracket format
- replace all word labels with "z"
- replace "root" with "root<index_number>" to help identify sentences easily after clustering
- Output histogram data of number of nodes(in this case, occurences of "z") in each tree
- Sort the lines of the data by number of nodes, (preferably according to frequency in histogram table)

## Clustering

- take the first sentence, run tree-edit-distance between this tree and all other trees
- take every sentence whose distance to first tree is within the max_distance parameter, and relieve parameter strictness if cluster_size is below min_size
- Remove the first sentence and every sentence which was filtered and add them to a new cluster
- Repeat until the tree list is empty
