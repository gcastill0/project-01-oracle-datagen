import re
import json

# Define a function to parse a single record
def parse_record(record_lines):
    record_dict = {}
    for line in record_lines:
        if ':' in line:
            key_value = line.split(":", 1)  # Split only at the first colon
            key = key_value[0].strip().replace(' ', '_').lower()  # Normalize key
            value = key_value[1].strip().strip("'\"")  # Strip extra spaces and quotes from value
            record_dict[key] = value
    return record_dict

# Define a function to load the file and parse the records
def parse_audit_log(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Regex to identify timestamp as a delimiter for each record
    timestamp_pattern = re.compile(r'^TIMESTAMP: ".*"')
    
    records = []
    current_record_lines = []
    
    for line in lines:
        if timestamp_pattern.match(line):
            if current_record_lines:  # If we have collected lines for a record, parse it
                record = parse_record(current_record_lines)
                records.append(record)
                current_record_lines = []
        
        current_record_lines.append(line.strip())
    
    # Don't forget the last record in the file
    if current_record_lines:
        record = parse_record(current_record_lines)
        records.append(record)

    return records

# Function to convert records to JSON
def records_to_json(records, output_file):
    with open(output_file, 'w') as f:
        json.dump(records, f, indent=4)

# Path to the audit log file
file_path = "audit_log.txt"
output_json_file = "audit_records.json"

# Parse the audit log file and convert it to JSON

parsed_records = parse_audit_log(file_path)
print(parsed_records)

records_to_json(parsed_records, output_json_file)

# print(f"Parsed {len(parsed_records)} records and saved to {output_json_file}.")
