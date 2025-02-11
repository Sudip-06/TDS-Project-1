import json

# Define input and output file paths
input_file = "/data/contacts.json"
output_file = "/data/contacts-sorted.json"

# Read the JSON data
with open(input_file, "r") as file:
    contacts = json.load(file)  # Expecting a list of dictionaries

# Sort the contacts by last_name, then first_name
sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

# Write the sorted list back to the output file
with open(output_file, "w") as file:
    json.dump(sorted_contacts, file, indent=4)

print("Contacts sorted successfully!")
