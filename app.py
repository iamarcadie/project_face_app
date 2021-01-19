from flask import Flask, render_template, request, Response
from forms import SubmitDataForm
from Train import *
from Recognize import *
from face_detect import *



app = Flask(__name__)

app.config['SECRET_KEY'] = 'thecodex'

face_cascade = './Haar_Cascades/haarcascade_frontalface_default.xml'
right_eye_cascade = './Haar_Cascades/haarcascade_righteye_2splits.xml'
left_eye_cascade = './Haar_Cascades/haarcascade_lefteye_2splits.xml'
samples = 50
dataset_name = 'dataset/'
file_name = 'train.yaml'
# variables for LBPH algorithm
radius = 1
neighbour = 8
grid_x = 8
grid_y = 8
var = list([radius,neighbour,grid_x,grid_y])

skin_detect = Skin_Detect()
size1 = (30,30)
size2 = (80,110)
scale_factor = 3
Face_Detect = Face_Detector(skin_detect)
file_name = 'train.yaml'

video = cv2.VideoCapture(-1)
model = Train_Model(face_cascade,right_eye_cascade,left_eye_cascade,var)
model_rec = Recognizer(face_cascade,file_name,var)

def gen_frames_recognition():
    while True:
        ret, img = video.read()
        predicted = model_rec.predict(img,Face_Detect,size1,size2)
        ret, buffer = cv2.imencode('.jpg', predicted)
        frame = buffer.tobytes()   
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/forms_name', methods = ['GET','POST'])
def forms_name():
    form = SubmitDataForm()
    if form.is_submitted():
        result = request.form
        nume = result['nume']
        # data_name(result)
        return render_template('create_dataset.html',nume = nume)
    return render_template('form.html', form = form)

@app.route('/train')
def train():
    model.train(dataset_name,file_name)
    return render_template("home.html")

@app.route('/video_dataset_feed')
def video_dataset_feed():
    return Response(model.create_dataset(samples,video,dataset_name), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/face_recognition')
def face_recognition():
    return render_template('face_recognition.html')


# @app.route('/create_dataset')
# def create_dataset():
#     return render_template('create_dataset.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0',debug=False, use_reloader = False)

