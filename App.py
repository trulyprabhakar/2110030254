from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

WINDOW_SIZE = 10
numbers_store = []

def fetch_numbers(number_id):
    try:
        response = requests.get(f"https://example.com/numbers/{number_id}", timeout=0.5)
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except (requests.RequestException, ValueError):
        return []
    return []

def calculate_average(numbers):
    return round(sum(numbers) / len(numbers), 2) if numbers else 0.00

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    global numbers_store

    # Store previous state of the window
    window_prev_state = numbers_store.copy()

    # Fetch new numbers from the third-party API
    new_numbers = fetch_numbers(number_id)
    
    # Filter out duplicates and add new numbers to the store
    unique_new_numbers = [num for num in new_numbers if num not in numbers_store]

    # Update the store with a maximum size limit
    for num in unique_new_numbers:
        if len(numbers_store) < WINDOW_SIZE:
            numbers_store.append(num)
        else:
            numbers_store.pop(0)
            numbers_store.append(num)

    # Calculate the average of the current window
    average = calculate_average(numbers_store)

    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": numbers_store,
        "numbers": new_numbers,
        "avg": average
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
