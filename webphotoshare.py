import os
from os import mkdir
from flask import Flask, render_template, redirect, request, url_for, flash, session, g
import model
import jinja2
from werkzeug.utils import secure_filename
import json
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

    # Password is required
    if password == "":
        flash("Please enter a password")
        return sign_up()

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

def create_user_session(user_object):
    session['userid'] = user_object.id
    session['username'] = user_object.username
    return session

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get('username')
    password = request.form.get('password')

    row = model.dbsession.query(model.User).filter_by(username=username).first()
    passrow = model.dbsession.query(model.User).filter_by(password=password).first()

    if row and passrow:
        flash("Log in successful")
        create_user_session(row)
        return redirect("upload_album")
    else:
        flash("Sorry we could not find your record")
        return render_template("login.html")

def allowed_file(filename):
    file_ext = filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
    return file_ext     

@app.route("/upload_album", methods=["GET"])
def list_albums():
    print "GET"
    userid = session['userid']
    print userid
    album_list = model.dbsession.query(model.Album).filter_by(user_id=userid).all()
    print album_list
    if not album_list:
        flash("You dont have any albums created yet")
    return render_template("upload_album.html",album_list=album_list)
    


@app.route("/upload_album", methods=["POST"])
def upload_pic():
    print "POST"
    username = session.get("username")
    user_id = session.get('userid')
    albumname = request.form.get('albumname')
    if request.method == 'POST':
        imagefile = request.files['imagefile']
        my_file= imagefile.filename
        my_file_type = my_file.split(".") # extract file extension from my_file
        file_type = my_file_type.pop()

    if my_file and allowed_file(my_file):
        filename = secure_filename(my_file)
        my_file_path = os.path.join(app.config['UPLOAD_FOLDER'])
        album_id = save_album(albumname)
        image_id = save_image(file_type,album_id,user_id)
        my_dir = "%s/%d/%d/" % ( my_file_path, user_id, album_id )
        image_path = "/%s/%d.%s" % (my_dir, image_id, file_type)
        if not os.path.exists(my_dir):
            os.makedirs(my_dir, 0o777)   
        imagefile.save(image_path)    
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



def save_image(file_type,album_id,user_id):
    image_object = model.Image(extention=file_type,
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
    new_album1 = model.Album(name=new_album,
                            desc=desc,
                            user_id=userid)
    dbalbumname = model.dbsession.query(model.Album).filter_by(name=new_album).filter(model.User.username==username).filter(model.Album.user_id==model.User.id).first()
    if dbalbumname:
        flash("albumname already exist, please try different albumname")
    else:
        new_album1.add_album()
        flash("Album successfully created")
        newalbum_id = new_album1.id 
        print newalbum_id
        blog_object = model.Blogpost(BlogText=blogpost,
                             user_id=userid,
                             album_id=newalbum_id)
        print "this is blog object %s" % blog_object
        blog_object.add_blog()
        print "blog added"
    return redirect("/upload_album")

@app.route("/album_detail/<int:id>")
def album_load(id):
    userid = session['userid']
    image_list = model.dbsession.query(model.Image).filter_by(album_id=id).all()
    print "This is my image list" ,image_list
    return render_template("album_detail.html", image_list=image_list)

@app.route("/process_facebook_login", methods=['POST'])
def create_fb_user():
    # Get the facebook data
    fbdata = request.form.get("fbdata")
    user_prof = json.loads(fbdata)
    print user_prof['id']

    # Get the Facebook ID from the data
    fbid = user_prof['id']
    email = user_prof['email']

    # Check if a user exists already with a matching fbid
    user = model.dbsession.query(model.User).filter_by(fbid=fbid).first()

    if not user:
        # No user with the fbid exists, check if user with this 
        #    email address exists
        row = model.dbsession.query(model.User).filter_by(username=email).first()

        if row:
            print "here"
            flash("Username already exist, please login with your existing account and password")
            return "ok"

        # This is the first time we've seen this user, create
        #   the User object and save in the database
        user = model.User(username=email,
                          fbid=fbid,
                            age="", 
                            zipcode="",
                            email=email)

        user.add_user()

    # Now "user" is our database user object, create a session 
    #   for this user
    create_user_session(user)
    flash("user successfully logged in")
    return redirect("/upload_album")    

@app.route("/logout")
def logout(): 
        del session['userid']
        return redirect(url_for("login"))

       
if __name__ == "__main__":
    app.run(debug = True)