from flask import Flask, render_template, request, redirect, flash, jsonify
from time_track.utils import get_current_time_range,get_time_block


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Sample data (replace with database integration for persistence)
events = []

# Function to generate unique event ID (replace with a more robust ID generation mechanism)
def generate_event_id():
    # Implement a logic to generate unique IDs (e.g., using UUID or incrementing counter)
    return f'event-{len(events) + 1}'

@app.route('/')
def index():
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    # Convert time_block to appropriate format
    interval = request.args.get('interval', 'hourly')
    time_block = get_time_block(interval)
    current_time = get_current_time_range(time_block)  
    
    if request.method == 'POST':
        event_name = request.form['event_name']
        time_block = request.form['time_block']
        type = request.form['type']
        grid = request.form['grid']
        date = request.form['date']

        # Validate input
        if not event_name or not time_block or not type or not grid or not date:
            flash('Please fill in all required fields.', 'error')
            return render_template('add.html')

        try:
            # Create event dictionary
            event = {
                'name': event_name,
                'time_block': time_block,
                'type': type,
                'grid': grid,
                'date': date,
                'id': generate_event_id()  # Function to generate unique ID
            }

            # Add event to list (replace with database operation)
            events.append(event)

            flash('Event added successfully!', 'success')
            if 'add_another' in request.form:
                # Render the add.html template again
                return render_template('add.html', time_blocks=time_block, current_time=current_time, interval=interval)
            else:
                # Redirect to index page or any other page
                return redirect('/')
        except ValueError:
            flash('Invalid date or time format.', 'error')
            return render_template('add.html', time_blocks=time_block, current_time=current_time, interval=interval)

    return render_template('add.html', time_blocks=time_block, current_time=current_time, interval=interval)

@app.route('/update_time_blocks', methods=['GET'])
def update_time_blocks():
    interval = request.args.get('interval', 'hourly')
    time_blocks = get_time_block(interval)
    options = ''.join([f'<option value="{time_block}">{time_block}</option>' for time_block in time_blocks])
    return jsonify(options)

if __name__ == '__main__':
    app.run(debug=True)
