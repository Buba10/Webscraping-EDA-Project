from flask import Flask, request, jsonify
import pandas as pd
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize default data
default_data = [
    {
        'name': 'Sample Laptop 1',
        'rating': 9.0,
        'processor': 'Intel i5',
        'ram': '8GB',
        'os': 'Windows 10',
        'ssd': '256GB',
        'display': '15.6 inches',
        'warranty': '1 year',
        'price': 800.00
    },
    {
        'name': 'Sample Laptop 2',
        'rating': 8.5,
        'processor': 'Intel i7',
        'ram': '16GB',
        'os': 'Windows 10',
        'ssd': '512GB',
        'display': '15.6 inches',
        'warranty': '2 years',
        'price': 1200.00
    }
]

# Load data with error handling
def load_data():
    if not os.path.isfile('laptop_data.csv'):
        initialize_data()  # Initialize if the file doesn't exist
    try:
        df = pd.read_csv('laptop_data.csv')
        if df.empty:
            initialize_data()  # Initialize if the file is empty
            df = pd.read_csv('laptop_data.csv')  # Reload the data after initialization
        return df
    except FileNotFoundError:
        logging.error("File not found. Returning empty DataFrame.")
        return pd.DataFrame(columns=['name', 'rating', 'processor', 'ram', 'os', 'ssd', 'display', 'warranty', 'price'])

# Initialize the CSV file with default data
def initialize_data():
    df = pd.DataFrame(default_data)
    save_data(df)
    logging.info("Initialized CSV file with default data.")

# Save data to CSV
def save_data(df):
    df.to_csv('laptop_data.csv', index=False)
    logging.info("Data saved to laptop_data.csv")

# Read Items
@app.route('/items', methods=['GET'])
def read_items():
    df = load_data()
    return jsonify(df.to_dict(orient='records'))

# Create Item
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    df = load_data()
    
    # Validate incoming data
    required_fields = ['name', 'rating', 'processor', 'ram', 'os', 'ssd', 'display', 'warranty', 'price']
    missing_fields = [field for field in required_fields if field not in new_item]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Additional validation for types and ranges
    try:
        new_item['rating'] = float(new_item['rating'])
        new_item['price'] = float(new_item['price'])
        if not (0 <= new_item['rating'] <= 10):
            return jsonify({'error': 'Rating must be between 0 and 10'}), 400
    except ValueError:
        return jsonify({'error': 'Rating and price must be numeric'}), 400

    new_item_df = pd.DataFrame([new_item])
    df = pd.concat([df, new_item_df], ignore_index=True)
    
    save_data(df)
    logging.info(f"New item added: {new_item}")
    return jsonify(new_item), 201

# Update Item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.json
    df = load_data()
    
    if 0 <= item_id < len(df):
        # Validate updated data
        for field in ['rating', 'price']:
            if field in updated_item:
                try:
                    updated_item[field] = float(updated_item[field])
                    if field == 'rating' and not (0 <= updated_item[field] <= 10):
                        return jsonify({'error': 'Rating must be between 0 and 10'}), 400
                except ValueError:
                    return jsonify({'error': f'{field.capitalize()} must be numeric'}), 400

        df.loc[item_id] = updated_item
        save_data(df)
        logging.info(f"Item updated: {updated_item}")
        return jsonify(updated_item), 200
    
    return jsonify({'error': 'Item not found'}), 404

# Delete Item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    df = load_data()
    
    if 0 <= item_id < len(df):
        deleted_item = df.iloc[item_id]  # Get the item to be deleted
        df = df.drop(item_id).reset_index(drop=True)
        save_data(df)
        logging.info(f"Item deleted: {deleted_item.to_dict()}")
        return jsonify({'message': 'Item deleted', 'item': deleted_item.to_dict()}), 200

    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)