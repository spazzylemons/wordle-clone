from flask import Flask

app = Flask(__name__)

with open('src/index.html') as file:
    homepage = file.read()

@app.route('/')
def index():
    return homepage

if __name__ == '__main__':
    app.run()
