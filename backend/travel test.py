print("Hello! Python is working!")

from flask import Flask
print("Flask imported successfully!")

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running!"

print("Starting server on http://localhost:5000")
print("Press Ctrl+C to stop")

if __name__ == '__main__':
    app.run(debug=True, port=5000)