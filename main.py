from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_restful import Resource, Api
from flask_restful import reqparse
import bcrypt 
import json
import datetime

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'unifeed'
app.config['MONGO_URI'] = 'mongodb://donaldev:password@ds113098.mlab.com:13098/unifeed'

mongo = PyMongo(app)
parser = reqparse.RequestParser()


@app.route('/')
def index():
    #go to index.html
    return render_template('index.html')  


@app.route('/signIn')

def signIn():
    #if it's a teacher logged in
    if 'username' in session: 
        return redirect(url_for('home'))
    

        
    #if it's a student logged in    
    elif 's_no' in session:
        # grab modules,name etc and pass in
        return redirect(url_for('home'))
    #if nobody logged in send them back to the login
    return render_template('user_auth/login.html')





@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST' :
        #initialise user DB
        users = mongo.db.users
        username_var = request.form['username']
        #Next two lines check if it's a teacher or a student logging in
        login_teacher = users.find_one({'username' : username_var})
        login_student = users.find_one({'s_no' : username_var})
        if login_teacher : #if a teacher is logged in
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_teacher['password']) ==  login_teacher['password']:
                session['username'] = username_var  #store their username in a session
                return redirect(url_for('home'))
        if login_student : #if a student is logged in
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_student['password']) ==  login_student['password']:
                session['s_no'] = username_var  #store their student number in a session
                return redirect(url_for('home'))

    return render_template('user_auth/login.html')

######################## LECTURER REGISTRATION ######################
@app.route('/register', methods=['POST','GET'])
def register():
    
    if request.method == 'POST' :
        users = mongo.db.users #initialise user DB
        modules = mongo.db.modules #initialise modules DB
        user_type = 'teacher' 
        username_var = request.form['username'] 
        enrollment_key = request.form['enrollment_key']
        office_loc = request.form['office_loc']
        link = request.form['link']
        img_link = request.form['img_link']
        existing_user = users.find_one({'username' : username_var})
        existing_mod_owner = modules.find_one({'owner':username_var})
        my_modules = []
        
        #if user hasn't registered already
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt()) ##encrypts password
            #check the modules DB to grab all module codes who have the 'owner' of the teachers username
            if existing_mod_owner :


                for module in modules.find({}) :
                    # print(module['owner'])
                    if module['owner'] == username_var :
                        my_modules.append(module['mod_code'])
                # my_modules = modules.find_one({'owner':username_var})['mod_code'] #########THIS IS TO BE CHANGED TO LOOP ALL OF THEM
                enroll_key_check = modules.find_one({'owner':username_var})['enrollment_key'] #checks if enrollment key is valid for owners modules
                if enrollment_key == enroll_key_check :
                    valid_key = 'valid'
                    
                else :
                    valid_key = 'invalid'
                
                if valid_key == 'valid' :#if enrollment key is G, insert data to DB and log the teacher in
                    users.insert({
                        'username' : username_var,
                        'password' : hashpass,
                        'user_type' : user_type,
                        'enrollment_key' : enrollment_key,
                        'modules' : my_modules,
                        'office_loc' : office_loc,
                        'link' : link,
                        'img_link' : img_link})
                    session['username'] = username_var
                    return redirect(url_for('home'))
                else: #otherwise redirect them to same page plus pass in error msg
                    error_msg = 'Invalid enrollment key, please try again'
                    
                    return render_template('user_auth/register.html', errormsg=error_msg)
            else :
                error_msg = 'Not a valid username'
                return render_template('user_auth/register.html', errormsg=error_msg)

        #this is the else for the check to see if user is registered
        error_msg = 'This username already exists, please sign in or contact administrator for help'
        
        return render_template('user_auth/register.html', errormsg=error_msg)
       

    return render_template('user_auth/register.html')


@app.route('/checkModules',methods=['POST'])
def checkModules():
    modulesDB = mongo.db.modules
    module_1 = request.form['module1'] 
 
    correctMods = []
    incorrectMods = []
    allModules = [
        {"correct": correctMods,
         "incorrect" : incorrectMods   
        }
    ]
    # for module in selectedModules :
    if modulesDB.find_one({"mod_code" : module_1}) :
        correctMods.append(module_1)
    else :
        incorrectMods.append(module_1)

    return jsonify({'allModules' : allModules})


@app.route('/registerS', methods=['POST','GET'])
def registerS():
    
    if request.method == 'POST' :
        # parser.add_argument('modules', action='append') 
        # args = parser.parse_args()
        users = mongo.db.users
        username_var = request.form['username']
        existing_user = users.find_one({'s_no' : username_var})
        modules = request.form['modules']
        modules = modules.split(",")
        # print(modules)



        if existing_user is None:
           user_type = 'student'
           hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
           users.insert({'s_no' : username_var, 'password' : hashpass, 'user_type' : user_type, 'modules' : modules})
           session['s_no'] = username_var
           return redirect(url_for('home'))
        else:
           error_msg = 'Username already exists - please log in'
           return render_template('user_auth/registerS.html', errormsg=error_msg)
       
    return render_template('user_auth/registerS.html')

@app.route('/home',methods=['POST','GET'])
def home() :

    if request.method == 'GET' :

        if 'username' in session: 
            users = mongo.db.users #initialise user DB

            #### Retrieve all of the current lecturers personal details AND educational details ie modulesDB
            
            modules_var = []
            user = users.find_one({"username" : session['username']})
            
            username = session['username']
            location = users.find_one({"username" : session['username']})['office_loc']
            img_loc = users.find_one({"username" : session['username']})['img_link']


            # print(user['modules'])
            for module in user['modules'] :
                modules_var.append(module)
            # print(modules_var)
            current_teacher_modules = retrieve_user_modules(modules_var,'reg')
            return render_template('home/homepage.html', current_teacher_modules = current_teacher_modules,username = username, location=location, img_loc=img_loc)

        elif 's_no' in session :
            users = mongo.db.users #initialise user DB

            #### Retrieve all of the current lecturers personal details AND educational details ie modulesDB
            
            modules_var = []
            user = users.find_one({"s_no" : session['s_no']})
            
            username = session['s_no']
            # location = users.find_one({"username" : session['username']})['office_loc']
            # img_loc = users.find_one({"username" : session['username']})['img_link']


            # print(user['modules'])
            for module in user['modules'] :
                modules_var.append(module)
            # print(modules_var)
           
            current_student_modules = retrieve_user_modules(modules_var,'reg')
            # print(current_student_modules)
            return render_template('home/homepage.html', current_student_modules = current_student_modules,username = username)
        else :
            return redirect(url_for('signIn'))    
        
    return redirect(url_for('signIn'))


#write post for module
@app.route('/mod_post',methods=['POST'])
def mod_post():
    modulesDB = mongo.db.modules
    
    module = request.form['mod_opt']
    post = request.form['post']
    date = datetime.datetime.now()
    time = date.strftime(" %d-%m-%Y %H:%M")

    post_ready = {
        'content' : post,
        'date' : time,
        'author' : session['username'],
        'mod_code': module
    }
    modulesDB.update_one({'mod_code': module}, {'$push':{'posts':post_ready}})
    #  users.update_one({'email':session['email']}, {'$set': {'name': name, 'surname': surname}})
    return redirect(url_for('myfeed'))






#write post for module
@app.route('/feedback_post',methods=['POST'])
def feedback_post():
    modulesDB = mongo.db.modules
    
    module_code = request.form['mod_opt']
    form_name = request.form['form_name']
    #only necessary if I'm adding a timeout to the feedback forms
    # date = datetime.datetime.now()
    # time = date.strftime(" %d-%m-%Y %H:%M")

    form_ready = {
        'title' : form_name,
        'type' : "weekly",
        'q1' : [],
        'q2' : [],
        'q3' : [],
        'q4' : [],
        'q5' : []
    }
    # print(form_ready)
    modulesDB.update({'mod_code': module_code}, {'$push':
                                                            { 
                                                                'feedback': {
                                                                            '$each':[form_ready],
                                                                            '$position': 0
                                                                        }
                                                            }
                                                    }
                                            )
    modulesDB.update_one({'mod_code' : module_code}, {'$set':{'active' : True}})
    #  users.update_one({'email':session['email']}, {'$set': {'name': name, 'surname': surname}})
    return redirect(url_for('home'))


@app.route('/feedback_submit', methods=['POST'])
def feedback_submit():

    modulesDB = mongo.db.modules




@app.route('/close_feedback', methods=['POST'])
def close_feedback():

    modulesDB = mongo.db.modules

 
    module_code = request.form['mod_opt']
    modulesDB.update_one({'mod_code' : module_code}, {'$set':{'active' : False}})
    return redirect(url_for('home'))


@app.route('/myfeed', methods=['GET'])
def myfeed():

    # modulesDB = mongo.db.modules
    users = mongo.db.users


    if request.method == 'GET' :

        if 'username' in session: 
            users = mongo.db.users #initialise user DB

            #### Retrieve all of the current lecturers personal details AND educational details ie modulesDB
            
            modules_var = []
            user = users.find_one({"username" : session['username']})
            
            username = session['username']



            # print(user['modules'])
            for module in user['modules'] :
                modules_var.append(module)
            # print(modules_var)
            current_teacher_modules = retrieve_user_modules(modules_var,'reg')
            current_posts = retrieve_user_modules(modules_var,'post')
            # current_feedback = retrieve_user_modules(modules_var,'feedback')
            # print(current_feedback)
            # print(current_posts)

            return render_template('home/feed.html', current_teacher_modules = current_teacher_modules,username = username, current_teacher_posts=current_posts)

        elif 's_no' in session :
            users = mongo.db.users #initialise user DB

            #### Retrieve all of the current lecturers personal details AND educational details ie modulesDB
            
            modules_var = []
            user = users.find_one({"s_no" : session['s_no']})
            
            username = session['s_no']
            # location = users.find_one({"username" : session['username']})['office_loc']
            # img_loc = users.find_one({"username" : session['username']})['img_link']


            # print(user['modules'])
            for module in user['modules'] :
                modules_var.append(module)
            # print(modules_var)
           
            current_student_modules = retrieve_user_modules(modules_var,'reg')
            current_posts = retrieve_user_modules(modules_var,'post')

           
            return render_template('home/feed.html', current_student_modules = current_student_modules,username = username, current_student_posts = current_posts)
        else :
            return redirect(url_for('signIn'))    
        
    return redirect(url_for('signIn'))





#Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('s_no', None)
    return render_template('index.html')



########################     HELPER FUNCTIONS     #################

def retrieve_user_modules(modules,functype) :
    modulesDB = mongo.db.modules
    # print ("Length is : {}".format(len(modules)))

    ##### RETRIEVE ALL RELEVANT INFO FOR User-Specific Modules #####



    if len(modules[0]) == 1 :
        
        mod_code = modules
        mod_title = modulesDB.find_one({"mod_code" : mod_code})['mod_title']
        owner = modulesDB.find_one({"mod_code" : mod_code})['owner'] 
        active = modulesDB.find_one({"mod_code" : mod_code})['active']


        ###### DATE INPUTTED WRONG

        posts = []
        for post in modulesDB.find_one({"mod_code" : modules}).sort("date",-1) :
            posts.append(post)
        
        posts.append(modulesDB.find_one({"mod_code" : modulesDB})['posts']) 
        module1 = {
            'mod_code' : mod_code,
            'mod_title' : mod_title,
            'mod_posts' : posts,
            'owner' : owner,
            'active' : active
        }
        # print (module1)
        return module1
    else :
        my_modules = []
        all_posts = []

        
        for module in modules :
            # print(module)
            mod_code = module

            mod_title = modulesDB.find_one({"mod_code" : module})['mod_title']
            owner = modulesDB.find_one({"mod_code" : module})['owner'] 
            active = modulesDB.find_one({"mod_code" : module})['active']
           
            # active_feed = modulesDB.find({"$and" : [{"mod_code" : module},
            #                                         {"status" : "active"}]})
            





            posts = []
            for post in modulesDB.find_one({"mod_code" : module})['posts'] :
                posts.append(post)
                all_posts.append(post)
            posts = sorted(posts, key=lambda k: k['date'], reverse=True)
           
            # posts = modulesDB.find_one({"mod_code" : module})['posts']
            modules_ready = {
                'mod_code' : mod_code,
                'mod_title' : mod_title,
                'mod_posts' : posts,
                'owner' : owner,
                'active' : active
            }
            my_modules.append(modules_ready)
        if(functype == 'reg') :
            return my_modules
        elif(functype == 'post') :
            
            all_posts = sorted(all_posts, key=lambda k: k['date'], reverse=True)
            return all_posts
        
        # elif(functype == 'feedback')

    

           

    


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)