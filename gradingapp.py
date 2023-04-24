import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics import recall_score

app = Flask(__name__)

# Load your prediction_check.csv file
check_data = pd.read_csv('prediction_check.csv')

# Function to compare the submitted predictions with the check data
def grade_predictions(user_data):
    # Check if all submitted IDs are in the check data
    if not set(user_data['id']).issubset(set(check_data['id'])):
        return None, "Invalid IDs"

    # Merge the user_data and check_data DataFrames based on the 'id' column
    merged_data = user_data.merge(check_data, on='id')

    # Calculate recall score using the 'predictions' and 'check' columns
    score = recall_score(merged_data['predictions'],merged_data['real'])

    return score, None

@app.route('/submit', methods=['POST'])
def submit_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    user_data = pd.read_csv(file)

    if 'id' not in user_data.columns or 'predictions' not in user_data.columns:
        return jsonify({"error": "Invalid file format"}), 400

    score, error = grade_predictions(user_data)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"score": score}), 200

if __name__ == '__main__':
    app.run(debug=True)
