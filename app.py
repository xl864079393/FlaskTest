from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to store the data
chart_data = {
    "StepCount": [120, 132, 101, 134, 90, 230, 210, 0, 0,0],
    "HeartRate": [120, 132, 101, 134, 90, 230, 210, 0, 0,0],
    "SPO2": [120, 132, 101, 134, 90, 230, 210, 0, 0,0],

}

# Function to simulate incoming data from your monitoring device
@app.route('/device_data', methods=['POST'])
def simulate_device_data():
    while True:
        # Simulating the device sending data every second
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        # Update chart data
        for key in chart_data:
            chart_data[key].pop(0)  # Remove the oldest data point
            chart_data[key].append(data[key])  # Add the new data point

        # Emit the updated data to the frontend
        socketio.emit('new_data', chart_data)

# Start the data simulation in a background thread
threading.Thread(target=simulate_device_data, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Send the initial data to the frontend when connected
    emit('new_data', chart_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
