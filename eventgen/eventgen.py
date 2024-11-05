import json
import os
import requests
import random
import time
import xml.etree.ElementTree as ET
from datetime import datetime as dt, timezone
import xml_handler

# Load configuration from config.json
def load_config(file_path='config.json'):
    """
    Load the configuration from a JSON file.
    
    Args:
        file_path (str): Path to the JSON config file.
        
    Returns:
        dict: Configuration settings.
    """
    with open(file_path, 'r') as file:
        config = json.load(file)

    # Assume auth_token is an environment variable. Load it and 
    # then add it to the config. The token should not be written
    # in a file at any time.
    auth_token  = os.getenv('AUTH_TOKEN')
    config.update({"auth_token": auth_token})

    return config

def generate_event(sample, config):
    event = sample.copy()

    # Real-time UTC date
    date = dt.now(timezone.utc)
    unix_time = date.timestamp()

    # Refactor data properties from event sample
    event["timestamp"] = xml_handler.get_current_timestamp()
    
    # Convert the dictionary to a JSON string
    final_event = json.dumps(event)

    return final_event

def dispatch_event(event, config):
    # Define the webhook URL where the data will be sent
    webhook_url = config["webhook_url"]
    
    # Determine the payload format (JSON or XML)
    if isinstance(event, dict):
        # The event is in JSON format (dictionary)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config["auth_token"]}'
        }
        # Convert the event to a JSON string
        event_data = json.dumps(event)
    elif isinstance(event, ET.Element):
        # The event is in XML format (ElementTree element)
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {config["auth_token"]}'
        }
        # Convert the XML event to a string
        event_data = ET.tostring(event, encoding='utf-8', method='xml').decode('utf-8')
    elif isinstance(event, str):
        # The event is a pre-serialized string (assume it's either JSON or XML)
        if event.strip().startswith("<"):
            # It's likely XML
            headers = {
                'Content-Type': 'application/xml',
                'Authorization': f'Bearer {config["auth_token"]}'
            }
        else:
            # It's likely JSON
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {config["auth_token"]}'
            }
        # Use the string as-is for the request
        event_data = event
    else:
        raise ValueError("Unsupported event format. Must be a dict (JSON), ElementTree.Element (XML), or string.")

    # Send the data to the webhook URL using an HTTP POST request
    response = requests.post(webhook_url, headers=headers, data=event_data)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to send data. Status code: {response.status_code}")
    else:
        print(f"Data successfully sent. Status code: {response.status_code}")

def parse_size(size_str):
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "PB": 1024**4}
    size, unit = size_str[:-2], size_str[-2:]
    return int(size) * units[unit]

def parse_time_range(time_range):
    time_units = {'m': 60, 'h': 3600, 'd': 86400}
    
    # Extract the numeric part and the unit
    number = int(time_range[:-1])
    unit = time_range[-1]
    
    if unit not in time_units:
        raise ValueError("Invalid time unit. Use 'm' for minutes, 'h' for hours, or 'd' for days.")
    
    return number * time_units[unit]

def calculate_average_event_size(events):
    total_size = 0

    for event in events:
        # Handle JSON events
        if isinstance(event, dict):
            # Convert event to JSON string and calculate its size in bytes
            event_str = json.dumps(event)
            event_size = len(event_str.encode('utf-8'))
        # Handle XML events (assuming event is an ElementTree element)
        elif isinstance(event, ET.Element):
            # Convert event to XML string and calculate its size in bytes
            event_str = ET.tostring(event, encoding='utf-8')
            event_size = len(event_str)
        # If event is already a string (XML or JSON)
        elif isinstance(event, str):
            event_size = len(event.encode('utf-8'))
        else:
            raise TypeError(f"Unsupported event type: {type(event)}")
        
        total_size += event_size

    average_size = total_size / len(events) if events else 0
    return average_size

def generate_events(config):
    # Use the sample events to rehydrate new events in the future

    if (config["format"] == "json"):
      events = xml_handler.parse_audit_log(config["samples"])
    elif (config["format"] == "xml"):
      events = xml_handler.parse_audit_log(config["samples"])

    byte_limit = parse_size(config['output_size'])
    total_time_seconds = parse_time_range(config["time_range"])

    average_event_size = calculate_average_event_size(events)
    estimated_events = byte_limit // average_event_size
    delay_per_event = total_time_seconds / estimated_events if estimated_events > 0 else 0

    # Timing measurement
    start_time = time.time()
    last_print_time = start_time
    elapsed_minutes = 0

    # Number of events
    event_count = 0

    # Loop control
    total_bytes = 0

    while total_bytes < byte_limit:
      sample = random.choice(events)
      event = generate_event(sample, config)
      total_bytes += len(event.encode())
      
      if (config["format"] == "xml"):
        event = xml_handler.json_to_xml(xml_handler.process_json_input(event))

      event_count += 1
      current_time = time.time()

      dispatch_event(event, config)
      time.sleep(delay_per_event)

      if current_time - last_print_time >= 60:
        elapsed_time = current_time - start_time
        elapsed_minutes = elapsed_time // 60
        last_print_time = current_time
    
      print(f"Sent {event_count} events, {total_bytes} bytes in {int(elapsed_minutes)} minute(s).")


def main():
    config = load_config()
    generate_events(config)

if __name__=="__main__":
    main()
