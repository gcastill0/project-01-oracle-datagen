from datetime import datetime
import pytz

def get_current_timestamp():
    # Get the current time with timezone info
    tz = pytz.timezone('America/New_York')  # You can use your local timezone (e.g., 'Europe/Paris', 'America/New_York')
    now = datetime.now(tz)

    # Format the timestamp in the desired format: YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM
    formatted_timestamp = now.isoformat()

    return formatted_timestamp

# Example usage
current_timestamp = get_current_timestamp()
print(f"Current timestamp: {current_timestamp}")
