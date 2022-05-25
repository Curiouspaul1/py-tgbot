from flask import Flask
from main import main
from multiprocessing import Process

app = Flask(__name__)

@app.route('/bot')
def start_bot():
    process = Process(target=main)
    process.start()
    # process.join()
    return "started bot successfully"

if __name__ == "__main__":
    app.run(debug=True)

# https://t.me/botfather    