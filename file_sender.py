from flask import Flask
from flask import send_from_directory

UPLOAD_FOLDER = '/home/namj/Desktop/tc/qrcodes/'

app = Flask(__name__)
app.config


@app.route('/qrcodes/<filename>', methods=['GET', 'POST'])
def send_qrcode(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run()