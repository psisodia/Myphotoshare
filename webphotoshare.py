import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
import model
import jinja2
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/Users/psisodia/Python/myphotoshare/data/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print app.config['UPLOAD_FOLDER']



@app.route("/sign_up")
def sign_up():
    return render_template("Sign_up.html")

@app.route("/sign_up", methods=["POST"])
def process_signup():
    username = request.form.get('username')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    email = request.form.get('email')
    user_object = model.User(username=username,
                            password=password,
                            age=age, 
                            zipcode=zipcode,
                            email=email)
    dbusername = model.dbsession.query(model.User).filter_by(username=username).all()
    if dbusername:
        flash("Username already exist, please try different username")
        return render_template("/Sign_up.html")
    else:
        user_object.add_user()
        session['userid'] = user_object.id
        flash("user successfully registered")
        return redirect("/upload_album")    

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/upload_album")
def album():
    return render_template("upload_album.html")

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get('username')
    row = model.dbsession.query(model.User).filter_by(username=username).all()
    if row:
        flash("Log in successful")
        session['userid'] = row[0].id
        session['username'] = row[0].username
        return redirect("upload_album")
    else:
        flash("Sorry we could not find your record")
        return render_template("login.html")

def allowed_file(filename):
    file_ext = filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
    return file_ext     

@app.route("/upload_album", methods=["POST"])
def upload_pic():
    username = session.get("username")
    print username
    albumname = request.form.get('albumname')
    print albumname
    if request.method == 'POST':
        imagefile = request.files['imagefile']
        print imagefile.filename
        if imagefile and allowed_file(imagefile.filename):
            filename = secure_filename(imagefile.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print image_path
            imagefile.save(image_path)
            album_id = save_album(albumname)
            image_id = save_image(imagefile,image_path,album_id)
            return redirect(url_for("album", filename=filename))

def save_album(albumname):
    album_object = model.Album(name=albumname,
                                 user_id=session.get("userid"))
    album_object.add_album()
    my_album = model.dbsession.query(model.Album).filter_by(name=albumname).all()
    album_id = my_album[0].id
    return album_id

def save_image(imagefile,image_path,album_id):
    image_object = model.Image(name=imagefile,
                                  img_path=image_path,
                                  user_id=session.get("userid"),
                                  album_id=album_id)
    image_object.add_picture()
    image = model.dbsession.query(model.Image).filter_by(name=imagefile).all()
    image_id = image.id
    return image_id






#def update_album_id(album_id):



    
   
if __name__ == "__main__":
    app.run(debug = True)