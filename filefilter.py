# Open the input file for reading
with open('user-agent_filteredSM.txt', 'r') as input_file:
  # Open the output file for writing
  with open('user-agent_filteredmain.txt', 'w') as output_file:
    # Iterate over each line in the input file
    for line in input_file:
      # If the line has a length between 10 and 20 characters (inclusive), write it to the output file
      if 55 <= len(line) <= 65 and 'SM-' in line or 'ONEPLUS' in line or 'Pixel' in line and 'Google' not in line or 'Nexus' in line or 'ZTE' in line:
        output_file.write(line)
