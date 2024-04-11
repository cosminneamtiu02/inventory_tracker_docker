from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)
dbname = os.environ.get('POSTGRES_DB')
dbuser = os.environ.get('POSTGRES_USER')
dbpassword = os.environ.get('POSTGRES_PASSWORD')
dbhost = "postgres"

# Connect to PostgreSQL database
try:
  conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword, host=dbhost)
  cursor = conn.cursor()
except Exception as e:
  print("Database connection error:", e)
  print(dbpassword)
  exit(1)

# Create table if not exists (modify as needed)
cursor.execute('''CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT, quantity INTEGER)''')
conn.commit()

# Routes (CRUD operations)
@app.route('/items', methods=['GET'])
def get_items():
  try:
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    return jsonify(items)
  except Exception as e:
    print("Error fetching items:", e)
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/items', methods=['POST'])
def add_item():
  data = request.get_json()
  name = data.get('name')
  quantity = data.get('quantity')
  if not name or not quantity:
    return jsonify({'error': 'Please provide name and quantity'}), 400
  try:
    cursor.execute('INSERT INTO items (name, quantity) VALUES (%s, %s)', (name, quantity))
    conn.commit()
    return jsonify({'message': 'Item added successfully'}), 201
  except Exception as e:
    print("Error adding item:", e)
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
  try:
    cursor.execute('SELECT * FROM items WHERE id = %s', (item_id,))
    item = cursor.fetchone()
    if not item:
      return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)
  except Exception as e:
    print("Error fetching item:", e)
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
  data = request.get_json()
  name = data.get('name')
  quantity = data.get('quantity')
  if not name or not quantity:
    return jsonify({'error': 'Please provide name and quantity'}), 400
  try:
    cursor.execute('UPDATE items SET name = %s, quantity = %s WHERE id = %s', (name, quantity, item_id))
    conn.commit()
    return jsonify({'message': 'Item updated successfully'})
  except Exception as e:
    print("Error updating item:", e)
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
  try:
    cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
    conn.commit()
    return jsonify({'message': 'Item deleted successfully'})
  except Exception as e:
    print("Error deleting item:", e)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)