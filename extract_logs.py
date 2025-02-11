import os
import glob

# Define directory and output file
log_dir = "/data/logs/"
output_file = "/data/logs-recent.txt"

# Get a list of all .log files, sorted by modification time (most recent first)
log_files = sorted(glob.glob(os.path.join(log_dir, "*.log")), key=os.path.getmtime, reverse=True)

# Take the 10 most recent files
recent_logs = log_files[:10]

# Extract the first line of each file
first_lines = []
for log_file in recent_logs:
    with open(log_file, "r") as file:
        first_line = file.readline().strip()
        first_lines.append(first_line)

# Write the first lines to the output file
with open(output_file, "w") as file:
    file.write("\n".join(first_lines) + "\n")

print("Successfully extracted first lines of the 10 most recent log files!")

