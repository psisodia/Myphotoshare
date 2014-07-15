import os
from flask import Flask, render_template, redirect, request, url_for, flash, session, g
import model
import jinja2
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/Users/psisodia/Python/myphotoshare/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print app.config['UPLOAD_FOLDER']

@app.before_request
def load_user_id():
    g.username = session.get('username')

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
        session['username'] = user_object.username
        flash("user successfully registered")
        return redirect("/upload_album")    

@app.route("/login")
def login():
    return render_template("login.html")

# @app.route("/upload_album")
# def album():
#     return render_template("upload_album.html")

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get('username')
    password = request.form.get('password')

    row = model.dbsession.query(model.User).filter_by(username=username).all()
    passrow = model.dbsession.query(model.User).filter_by(password=password).all()

    if row and passrow:
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

@app.route("/upload_album", methods=["GET"])
def list_albums():
    userid = session["userid"]
    album_list = model.dbsession.query(model.Album).filter_by(user_id=userid).all()
    return render_template("upload_album.html",album_list=album_list)

@app.route("/upload_album", methods=["POST"])
def upload_pic():
    username = session.get("username")
    albumname = request.form.get('albumname')
    if request.method == 'POST':
        imagefile = request.files['imagefile']
        my_file= imagefile.filename
        if my_file and allowed_file(my_file):
            filename = secure_filename(my_file)
            image_path = username + '_' + albumname + '_' + my_file
            my_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagefile.save(my_file_path)
            album_id = save_album(albumname)
            image_id = save_image(my_file,image_path,album_id)
    
    return redirect(url_for("list_albums"))

def save_album(albumname):
    print albumname
    username = session.get('username')
    dbalbumname = model.dbsession.query(model.Album).filter_by(name=albumname).filter(model.User.username==username).filter(model.Album.user_id==model.User.id).first()

    print dbalbumname
    if dbalbumname is not None:
        album_id = dbalbumname.id
        print album_id
        return album_id
    
    album_object = model.Album(name=albumname,
                             user_id=session.get("userid"))
    album_object.add_album()
    album_id = album_object.id
    return album_id



def save_image(my_file,image_path,album_id):
    image_object = model.Image(name=my_file,
                                  img_path=image_path,
                                  user_id=session.get("userid"),
                                  album_id=album_id)
    image_object.add_picture()
    image_id = image_object.id
    return image_id

@app.route("/create_album", methods=["POST"])
def create_album():
    new_album = request.form.get('new_album')
    desc = request.form.get('desc')
    blogpost = request.form.get('blogpost')
    userid = session['userid']
    username= session['username']
    new_album = model.Album(name=new_album,
                            desc=desc,
                            user_id=userid)
    dbalbumname = model.dbsession.query(model.Album).filter_by(name=new_album).filter(model.User.username==username).filter(model.Album.user_id==model.User.id).first()
    if dbalbumname:
        flash("albumname already exist, please try different albumname")
    else:
        new_album.add_album()
        flash("Album successfully created")
        return redirect("/upload_album") 
    newalbum_id = new_album.id 
    blog_object = model.Blog(blogpost=blogpost,
                             user_id=userid,
                             album_id=newalbum_id)
    blog_object.add_blog()
    return redirect("/upload_album")

@app.route("/album_detail")
def album_load():
    userid = session['userid']
    album_id_clicked = request.form.get['album_id']



@app.route("/logout")
def logout():
    del session['userid']
    return redirect(url_for("login"))

       
if __name__ == "__main__":
    app.run(debug = True)