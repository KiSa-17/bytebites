from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import time
from threading import Timer

app = Flask(_name_)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'password'  
app.config['MYSQL_DB'] = 'medication_db'


mysql = MySQL(app)


medication_data = []

# Route to add medication schedule
@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    medication_name = data['medication_name']
    dosage = data['dosage']
    time = data['time']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO medication_schedule (medication_name, dosage, time) VALUES (%s, %s, %s)", 
                (medication_name, dosage, time))
    mysql.connection.commit()
    return jsonify({"message": "Schedule added successfully!"}), 200

# Route to get medication schedule
@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medication_schedule")
    data = cur.fetchall()
    
    return jsonify({"medication_schedules": data}), 200

# Function to simulate sending a reminder and checking for confirmation
def send_reminder(medication):
    print(f"Reminder: Time to take your medication: {medication}")
    # Here, you would send the reminder to the user via SMS or chat
    # Call your external service (Twilio, WhatsApp, etc.) to notify the user.
    
    # For demo, we just print it out.
    
    # Check if no confirmation received after 10 seconds, escalate the alert
    Timer(10.0, send_escalation_alert, [medication]).start()

def send_escalation_alert(medication):
    print(f"Escalation Alert: No confirmation received for {medication}. Alert sent to family.")
    # Send escalation alert logic (family member notification) goes here.

# Start reminder system
def start_reminder_system():
    # This simulates checking the medication schedule every minute
    while True:
        # Here you would check the database for upcoming medication times and send reminders
        current_time = time.strftime('%H:%M')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM medication_schedule WHERE time = %s", (current_time,))
        medications = cur.fetchall()
        
        for medication in medications:
            send_reminder(medication[1])  # medication[1] is the medication name
        time.sleep(60)

if _name_ == '_main_':
    app.run(debug=True)
