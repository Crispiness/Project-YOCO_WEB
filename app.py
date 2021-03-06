import os
from flask import Flask, render_template, redirect, request
from flask_dropzone import Dropzone
#from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_mail import Mail, Message


app = Flask(__name__)
dropzone = Dropzone(app)
mail = Mail()
filename = None

dir_path = os.path.dirname(os.path.realpath(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'paint'

# Dropzone settings
#app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
#app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
#app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
#app.config['DROPZONE_REDIRECT_VIEW'] = 'paint'
#app.config['DROPZONE_MAX_FILES'] = 1
# Uploads settings
#app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
#photos = UploadSet('photos', IMAGES)
#configure_uploads(app, photos)
#patch_request_class(app)  # set maximum file size, default is 16MB

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@gmail.com'
app.config["MAIL_PASSWORD"] = '*********'

mail.init_app(app)

@app.route('/')
@app.route('/main' , methods=['POST', 'GET'])
def main():
    global filename
    file = None
    if request.method == 'POST':
        f = request.files.get('file')
        file = f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        filename = f.filename
    return render_template('main.html')


@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/github')
def github():
    return redirect('https://github.com/7-B/yoco')

@app.route('/contactus')
def contactus():
    return redirect('https://github.com/7-B/yoco')

@app.route('/makeMeme', methods=['POST', 'GET'])
def makeMeme():
    global filename
    return render_template("makeMeme.html", file_name = filename)

@app.route('/color')
def color():
    return render_template('colorbook.html')

@app.route('/painting')
def paint():
    global filename
    return render_template('painting.html', file_name = filename)

@app.route("/email", methods=['post', 'get'])
def email_test():

    if request.method == 'POST':
        senders = request.form['email_sender']
        receiver = request.form['email_receiver']
        content = request.form['email_content']
        receiver = receiver.split(',')

        for i in range(len(receiver)):
            receiver[i] = receiver[i].strip()

        print(receiver)

        result = send_email(senders, receiver, content)

        if not result:
            return render_template('email.html', content="Email is sent")
        else:
            return render_template('email.html', content="Email is not sent")

    else:
        return render_template('email.html')

def send_email(senders, receiver, content):
    try:
        mail = Mail(app)
        msg = Message('Title', sender = senders, recipients = receiver)
        msg.body = content
        mail.send(msg)
    except Exception:
        pass
    finally:
        pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
