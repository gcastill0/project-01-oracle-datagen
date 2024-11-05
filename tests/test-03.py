import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Sample JSON string
json_string = '''
{
    "timestamp": "Wed Feb  10 14:23:19 2021 +01:00",
    "length": "329",
    "action": "INSERT INTO users (user_id, username, email) VALUES (123, 'testuser', 'test@example.com')",
    "database_user": "jdoe",
    "privilege": "SYSDBA",
    "client_user": "john",
    "client_terminal": "UNKNOWN",
    "status": "0",
    "dbid": "2943533768",
    "sessionid": "3444967295",
    "userhost": "PC1",
    "client_address": "",
    "action_number": "3"
}
'''

# Function to convert snake_case to camelCase
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

# Function to convert JSON to XML
def json_to_xml(json_data):
    root = ET.Element("AuditRecord")
    
    for key, value in json_data.items():
        # Convert the JSON key to camelCase
        camel_case_key = to_camel_case(key)
        # Create an XML element using the camelCase key
        element = ET.SubElement(root, camel_case_key)
        # Set the text for the XML element
        element.text = str(value)
    
    return root

# Function to pretty print the XML
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Load the JSON data
json_data = json.loads(json_string)

# Convert JSON to XML
xml_root = json_to_xml(json_data)

# Output the pretty-printed XML
pretty_xml = prettify_xml(xml_root)
print(pretty_xml)
