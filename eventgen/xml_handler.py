import re, json, random
import xml.etree.ElementTree as ET
from xml.dom import minidom
import xml.sax.saxutils as saxutils
from datetime import datetime
import pytz

def get_current_timestamp():
    # Get the current time with timezone info
    tz = pytz.timezone('America/New_York')  # You can use your local timezone (e.g., 'Europe/Paris', 'America/New_York')
    now = datetime.now(tz)

    # Format the timestamp in the desired format: YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM
    formatted_timestamp = now.isoformat()

    return formatted_timestamp

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

# Function to convert a single JSON record to an XML element
def json_record_to_xml(record):
    root = ET.Element("AuditRecord")
    
    for key, value in record.items():
        # Convert the JSON key to Camel_Hump_Case
        camel_hump_key = to_camel_hump_case(key)
        # Create an XML element using the Camel_Hump_Case key
        element = ET.SubElement(root, camel_hump_key)
        # Set the sanitized value for the XML element
        element.text = sanitize_value(str(value))
    
    # Convert the ElementTree to a string
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    return reparsed.toprettyxml(indent="  ")

# Function to convert records to JSON
def records_to_json(records, output_file):
    with open(output_file, 'w') as f:
        json.dump(records, f, indent=4)

# Function to sanitize XML element names
def sanitize_key(key):
    # Replace invalid characters like $, and any character that's not alphanumeric or underscore, with an underscore
    return re.sub(r'[^a-zA-Z0-9_]', '_', key)

# Function to sanitize values for XML
def sanitize_value(value):
    # Escape common XML special characters
    return saxutils.escape(value).replace("'", "&apos;").replace('"', "&quot;")

# Function to convert snake_case to Camel_Hump_Case
def to_camel_hump_case(snake_str):
    components = snake_str.split('_')
    return '_'.join(x.capitalize() for x in components)

# Function to convert JSON to XML
def json_to_xml(json_record):
    root = ET.Element("AuditRecord")
    
    for key, value in json_record.items():
        # Sanitize the key to ensure it's a valid XML element name
        sanitized_key = sanitize_key(key)
        # Convert the sanitized key to Camel_Hump_Case
        camel_hump_key = to_camel_hump_case(sanitized_key)
        # Create an XML element using the Camel_Hump_Case key
        element = ET.SubElement(root, camel_hump_key)
        # Set the sanitized value for the XML element
        element.text = sanitize_value(str(value))

    return root

# Function to pretty print the XML
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')

    # Print the rough string to inspect for issues
    # print(f"Rough XML string:\n{rough_string}\n\n")
    
    # Attempt to parse the rough string
    try:
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {e}\n\n{rough_string}")

    return pretty_xml

def process_json_input(json_data):
    # If json_data is a string, parse it into a dictionary
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)  # Parse JSON string into a dictionary
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")
    
    return json_data
