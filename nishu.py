from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random

app = Flask(__name__)

# Function to generate a random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Home page with a form to submit URLs
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_code = generate_short_code()

    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
    conn.commit()
    conn.close()

    shortened_url = request.host_url + short_code
    return render_template('index.html', shortened_url=shortened_url)

# Endpoint to redirect to the original URL
@app.route('/<short_code>')
def redirect_to_original(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)