#19090136_Sri mulia ningsih_6D
#19090060_Nirla Wahidatus salam_6D

# import library
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import datetime, os


# Inisialisasi
database_file = 'sqlite:///database/users_pic.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'jpeg', 'png', 'gif']
db = SQLAlchemy(app)


# DATABASE
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    timeStamp = db.Column(db.DateTime)

db.create_all()

def validate_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']

# http://127.0.0.1:5000/upImage
@app.route('/upImage', methods=["POST"])
def upImage():
    img = request.files['image']
    time = datetime.datetime.utcnow()
    if img and validate_img(img.filename):
        filename = secure_filename(img.filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gambar = Image(name=img.filename, timeStamp=time)
        db.session.add(gambar)
        db.session.commit()
        return jsonify({"msg": "Upload Image Successful !", "name":filename, "time":time})
    return jsonify({"msg": "Upload Image Failed !"})

if __name__ == '__main__':
   app.run(debug = True, port=4000)