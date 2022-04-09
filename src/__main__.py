import asyncio
from flask import Flask, request
from google.cloud import speech
from threading import Thread

import websockets

app = Flask(__name__)

with open('src/index.html') as file:
    homepage = file.read()

@app.route('/')
def index():
    return homepage

async def receive_recording(websocket):
    content = await websocket.recv()
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        audio_channel_count=2,
        language_code='en-US',
    )
    response = client.recognize(config=config, audio=audio)
    alternatives = response.results[0].alternatives
    for alternative in alternatives:
        letters = alternative.transcript.split(' ')
        print(letters)
        if len(letters) == 5 and all(len(i) == 1 for i in letters):
            return ''.join(letters).lower()
    await websocket.send(content)

async def process_recordings():
    print('i am here 1')
    await websockets.serve(receive_recording, 'localhost', 5001)

def run_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.new_event_loop()
t = Thread(target=run_event_loop, args=(loop,), daemon=True)
t.start()
task = asyncio.run_coroutine_threadsafe(process_recordings(), loop)

if __name__ == '__main__':
    app.run(debug=True)
