from datetime import datetime, timedelta


# Function to get the start time ranges for the entire day
def get_time_block(interval):
    current_time = datetime.now()
    time_block = datetime(current_time.year, current_time.month, current_time.day, 0, 0)  # Start of the day
    end_time = time_block + timedelta(days=1)  # End of the day
    time_blocks = []

    if interval == 'hourly':
        step = timedelta(hours=1)
    elif interval == 'half-hourly':
        step = timedelta(minutes=30)
    elif interval == 'quarter-hourly':
        step = timedelta(minutes=15)
    else:
        raise ValueError("Invalid time interval")

    while time_block < end_time:
        time_str = time_block.strftime('%H:%M') + " - " + (time_block + step).strftime('%H:%M')
        time_blocks.append(time_str)
        time_block += step

    return time_blocks

# Function to get the current time range
def get_current_time_range(time_blocks):
    current_hour = datetime.now().hour
    current_time_range = None
    
    for time_range in time_blocks:
        start_hour = int(time_range.split(' - ')[0].split(':')[0])
        end_hour = int(time_range.split(' - ')[1].split(':')[0])
        if start_hour <= current_hour < end_hour:
            current_time_range = time_range
            break
    
    return current_time_range
