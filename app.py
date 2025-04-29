# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from urllib.parse import quote_plus

# app = Flask(__name__)
# CORS(app)

# # MongoDB connection string with password safely encoded
# username = "Nani"
# password = quote_plus("Nani7075@")
# mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.tlqfeke.mongodb.net/"

# # Connect to MongoDB
# client = MongoClient(mongo_uri)
# db = client["your_database_name"]           # replace with your DB name
# collection = db["your_collection_name"]     # replace with your collection name



# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

# MongoDB connection
username = "Nani"
password = quote_plus("Nani7075@")  # Escape special characters
uri = f"mongodb+srv://{username}:{password}@cluster0.tlqfeke.mongodb.net/"
client = MongoClient(uri)

db = client["complaints_db"]
collection = db["complaints"]



@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})




@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    # Check if user already exists
    if collection.find_one({"email": email}):
        return jsonify({"message": "Email already registered!", "status": "error"}), 400

    # Save user
    collection.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "phone": phone
    })

    return jsonify({"message": "Registration successful!", "status": "success"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = collection.find_one({"email": email, "password": password})
    if user:
        return jsonify({"message": "Login successful!", "status": "success"}), 200
    else:
        return jsonify({"message": "Invalid credentials", "status": "error"}), 401
    



@app.route("/submit", methods=["POST"])
def submit_complaint():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Complaint submitted successfully"})

@app.route("/track/<complaint_id>", methods=["GET"])
def track_complaint(complaint_id):
    complaint = collection.find_one({"id": complaint_id}, {"_id": 0})
    if complaint:
        return jsonify({"status": complaint["status"]})
    else:
        return jsonify({"error": "Complaint not found"}), 404
    


feedback_collection = db["feedbacks"]  # Add this where you define other collections
   
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = {
        "name": data.get("name"),
        "message": data.get("message"),
        "rating": data.get("rating"),
    }
    feedback_collection.insert_one(feedback)
    return jsonify({"message": "Feedback submitted successfully!", "status": "success"})

@app.route("/admin/summary")
def admin_summary():
    complaints = list(db.complaints.find())
    users = list(db.users.find())

    total = len(complaints)
    pending = len([c for c in complaints if c.get("status") == "In Progress"])
    resolved = len([c for c in complaints if c.get("status") == "Resolved"])
    registered_users = len(users)

    return jsonify({
        "total_complaints": total,
        "pending_complaints": pending,
        "resolved_complaints": resolved,
        "users_registered": registered_users
    })

# @app.route('/admin/complaints', methods=['GET'])
# def get_complaints():
#     return jsonify(complaints_data)

# Add route to resolve a complaint


@app.route('/update-settings', methods=['POST'])
def update_settings():
    data = request.get_json()

    fullname = data.get('fullname')
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # TODO: Replace with real user ID and database logic
    print(f"User settings update requested for: {fullname} ({email})")

    if current_password and new_password:
        # Simulate checking and updating the password
        print("Password change detected.")

    # Simulate updating user info in database
    print("Saving updated info...")

    return jsonify({'message': 'Your settings have been successfully updated!'})


@app.route("/admin/complaints", methods=["GET"])
def get_complaints():
    return jsonify(complaints)

@app.route("/admin/complaints/<int:complaint_id>/resolve", methods=["POST"])
def resolve_complaint(complaint_id):
    for c in complaints:
        if c["id"] == complaint_id:
            c["status"] = "Resolved"
            return jsonify({"message": "Complaint resolved"}), 200
    return jsonify({"error": "Complaint not found"}), 404

@app.route("/admin/complaints/<int:complaint_id>", methods=["DELETE"])
def delete_complaint(complaint_id):
    global complaints
    complaints = [c for c in complaints if c["id"] != complaint_id]
    return jsonify({"message": "Complaint deleted"}), 200

handler = app

if __name__ == "__main__":
    app.run(debug=True)
  
