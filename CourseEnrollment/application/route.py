from application import app, db,api 
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegistrationForm, CourseAddForm
from application.course_list import course_list
from flask import render_template, request, Response, json, jsonify,redirect, flash, session, url_for
from flask_restx import Resource


courseData=[{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

############################################APIs###############################################################
@api.route('/api','/api/')
class GetandPOst(Resource):

    def get(self):
        return jsonify(User.objects.all())
    def post(self):
        data=api.payload
        
        user=User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()

        return jsonify(User.objects(user_id=data['user_id']))
@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))
    
    
    def put(self, idx):
        data=api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))
    
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("user is deleted.")


############################################APIs###############################################################


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True) #flask searches for index.html in the template dir





@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=None):
    if term==None:
        term="spring 2022"
    classes=Course.objects.order_by("-courseID")
    return render_template("courses.html", courseData=classes, courses=True, term=term) #flask searches for courses.html in the template dir

@app.route("/addcourse", methods=['GET', 'POST'])
def addcourse():
    form=CourseAddForm()
    if form.validate_on_submit():
        courseID=Course.objects.count()+1
        title=form.title.data
        description=form.description.data
        credit=form.credit.data
        term=form.term.data
        Course(courseID=courseID, title=title, description=description, credit=credit, term=term).save()
        flash("You are successfully registered", "success")
        return redirect(url_for("courses"))
    return render_template("addcourse.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if session.get('user_id'):
        return redirect("/index")
    
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        user_id=User.objects.count()
        user_id +=1

        user=User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered", "success")
        return redirect("/index")
    return render_template("register.html",form=form,  register=True) #flask searches for index.html in the template dir

@app.route("/login", methods=['GET', 'POST'])
def login():
    form=LoginForm()

    if session.get('user_id'):
        return redirect("/index")
    if form.validate_on_submit():
        email=form.email.data #accessing the value of email field in the form
        password=form.password.data #accessing the value of password field in the form
        user=User.objects(email=email).first()# find the first user in data model with the same email
        if user and user.check_password(password):
         
          session['user_name']=user.first_name
          session['user_id']=user.user_id
          
          flash(f"{user.first_name} You are successfully logged in!", "success") 
          return redirect("/index")         
        else:
            flash("sorry, something went wrong!","danger")
    return render_template("login.html", title="login", form=form, login=True) #flask searches for index.html in the template dir


@app.route("/logout")
def logout():
    session['user_id']=None
    session.pop('user_name',None)
    return redirect(url_for("login"))
""" a version with get method: 

@app.route("/enrollment") 
def enrollment():
    id=request.args.get('id')
    title=request.args.get('title')
    term=request.args.get('term')
    return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term}) #flask searches for index.html in the template dir
"""

#a version with post method:


@app.route("/enrollment", methods=["GET", "POST"]) 
def enrollment():
    if not session.get('user_id'):
        return redirect(url_for("login"))
    courseID=request.form.get('id')
    courseTitle=request.form.get('title')
    term=request.form.get('term')
    user_id=session.get('user_id')
    if courseID:
         if Enrollment.objects(user_id=user_id, course_id=courseID):
             flash(f"Oops! you are already registerd for this course {courseTitle}","danger")
             return redirect("courses")
         else:
             enroll=Enrollment(user_id=int(user_id), course_id=courseID).save()
             flash(f"you are enrolled in {courseTitle}", "success")
    classes=course_list()
    return render_template("enrollment.html",
                            title="enrollment",
                            enrollment=True,
                            classes=classes)


# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if idx==None:
#         jdata=courseData
#     else:
#         jdata=courseData[int(idx)]
#     return Response(json.dumps(jdata), mimetype="application/json")


    
    

@app.route("/user")
def user():
    # user=User(user_id=1, first_name="Chris", last_name="clarks", email="aaa@bbb.com", password="12134").save()
    # user=User(user_id=2, first_name="Andi", last_name="daves", email="aaa2@bbb.com", password="12134").save()
    # user=User(user_id=3, first_name="Mary", last_name="happies", email="aaa3@bbb.com", password="12134").save()
    # user=User(user_id=15, first_name="Ana1", last_name="goods", email="aaa15@bbb.com", password="123456789").save()

    users=User.objects.all()
    return render_template("user.html", users=users)

    