import json

# Define the raw data as a multi-line string (in practice, this would come from a file)
raw_data = """
Wed Feb  10 14:23:19 2021 +01:00
LENGTH : '329'
ACTION :[102] 'INSERT INTO users (user_id, username, email)
              VALUES (123, 'testuser', 'test@example.com')'
DATABASE USER:[4] 'jdoe'
PRIVILEGE :[6] 'SYSDBA'
CLIENT USER:[0] 'john'
CLIENT TERMINAL:[7] 'UNKNOWN'
STATUS:[1] '0'
DBID:[10] '2943533768'
SESSIONID:[10] '3444967295'
USERHOST:[3] 'PC1'
CLIENT ADDRESS:[0] ''
ACTION NUMBER:[1] '3'
"""

# Parsing the raw data
def parse_raw_data(data):
    lines = data.strip().splitlines()
    parsed_data = {}
    
    # Handle timestamp separately
    parsed_data["timestamp"] = lines[0].strip()
    
    # Process the remaining lines
    for line in lines[1:]:
        if ':' in line:
            key_value = line.split(":", 1)  # Split only at the first colon
            key = key_value[0].strip().replace(' ', '_').lower()  # Convert key to a more JSON-friendly format
            value = key_value[1].strip().strip("'")  # Strip extra spaces and quotes from value
            parsed_data[key] = value
    
    return parsed_data

# Parse the raw data into a dictionary
parsed_data = parse_raw_data(raw_data)

# Convert the dictionary to a JSON string
json_string = json.dumps(parsed_data, indent=4)

# Output the JSON string
print(json_string)
