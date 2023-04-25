import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics import recall_score
import os

app = Flask(__name__)

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the prediction_check.csv file in the data folder
check_data_path = os.path.join(current_directory, 'data', 'prediction_check.csv')

# Load your prediction_check.csv file
check_data = pd.read_csv(check_data_path)


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

    if score<=0.4:
        return jsonify(f'Thank for your submission! Your score is {score}. I feel you can do better!'), 200
    elif score>0.4 and score <=0.6:
        return jsonify(f'Thank for your submission! Your score is {score}. Good try! give it another go!'), 200    
    elif score>0.6 and score<0.83:
        return jsonify(f'Thank for your submission! Your score is {score}. Very good job at this stage you probably beaten me!'), 200   
    elif score>0.83:
        return jsonify(f'Thank for your submission! Your score is {score}. Did you cheat? :-)'), 200       

if __name__ == '__main__':
    app.run(debug=True)
