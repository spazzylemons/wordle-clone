from flask import Flask, request

app = Flask(__name__)

with open('src/index.html') as file:
    homepage = file.read()

@app.route('/')
def index():
    return homepage

@app.route('/send_recording', methods=['POST'])
def send_recording():
    with open('received.webm', 'wb') as file:
        file.write(request.data)
    return 'audio received and saved'

if __name__ == '__main__':
    app.run()
