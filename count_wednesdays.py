from datetime import datetime

# Define input and output file paths
input_file = "/data/dates.txt"
output_file = "/data/dates-wednesdays.txt"

# Initialize Wednesday count
wednesday_count = 0

# Read and process the dates
with open(input_file, "r") as file:
    for line in file:
        date_str = line.strip()
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Adjust format if needed
            if date_obj.weekday() == 2:  # 2 represents Wednesday
                wednesday_count += 1
        except ValueError:
            print(f"Skipping invalid date format: {date_str}")

# Write the count to the output file
with open(output_file, "w") as file:
    file.write(str(wednesday_count))

print(f"Number of Wednesdays: {wednesday_count}")
