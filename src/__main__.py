from flask import Flask, request
from google.cloud import speech

app = Flask(__name__)

with open('src/index.html') as file:
    homepage = file.read()

@app.route('/')
def index():
    return homepage

@app.route('/send_recording', methods=['POST'])
def send_recording():
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=request.data)
    config = speech.RecognitionConfig(
        audio_channel_count=2,
        language_code='en-US',
    )
    response = client.recognize(config=config, audio=audio)
    print(response)
    data = []
    for result in response.results:
        data.append('"{}"'.format(result.alternatives[0].transcript))
    return ' '.join(data)

if __name__ == '__main__':
    app.run(debug=True)
