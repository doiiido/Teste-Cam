from flask import Flask

app = Flask(__name__)
app.secret_key = "Teste-CAM"
app.config['UPLOAD_FOLDER'] = "static"
