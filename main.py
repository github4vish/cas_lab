from flask import Flask, request, jsonify
import os
import pymysql

app = Flask(__name__)

@app.route('/generate_even_numbers/<int:n>', methods=['GET'])
def generate_even_numbers(n):
         even_numbers = [i * 2 for i in range(n)]
         return jsonify({'even_numbers': even_numbers})


def matrix_multiply(matrix_a, matrix_b):
    result = [[0] * len(matrix_b[0]) for _ in range(len(matrix_a))]
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            for k in range(len(matrix_b)):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return result

@app.route('/multiply', methods=['POST'])
def multiply_matrices():
    data = request.get_json()
    matrix_a = data['matrix_a']
    matrix_b = data['matrix_b']
    
    result = matrix_multiply(matrix_a, matrix_b)
    
    return jsonify({'result': result})

@app.route('/')
def display_nth_largest():
    numbers = [int(x) for x in request.args.get('numbers').split(',')]
    n = int(request.args.get('n'))
    nth_largest = sorted(numbers, reverse=True)[n-1]
    return f'The {n}th largest number is: {nth_largest}'


db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('SQL_USERNAME'),
    'database': os.environ.get('SQL_DATABASE_NAME','users'),
}



cnx = pymysql.connect(**db_config)

cursor = cnx.cursor()

# User registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Both username and password are required'}), 400

    # Check if username already exists
    cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'error': 'Username already exists'}), 400

    # Insert new user into the database
    cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password))
    cnx.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Both username and password are required'}), 400

    # Retrieve user from the database
    cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    elif user and user[1] == password:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})




if __name__ == '__main__':
    app.run(debug=True)





