def replace_root_with_line_number(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        with open(output_file, 'w') as outfile:
            for i, line in enumerate(lines, start=1):
                new_line = line.replace("root", f"root{str(i).zfill(8)}")
                outfile.write(new_line)

        print(f"Successfully processed the file. Check {output_file} for results.")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


input_file = 'bracket_notation_trees.txt'
output_file = 'numbered_500k_trees.txt'
replace_root_with_line_number(input_file, output_file)
