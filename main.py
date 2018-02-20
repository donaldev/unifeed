from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'unifeed'
app.config['MONGO_URI'] = 'mongodb://donaldev:password@ds113098.mlab.com:13098/unifeed'

mongo = PyMongo(app)


@app.route('/')
def index():
    #go to index.html
    return render_template('index.html')  


@app.route('/signIn')

def signIn():
    #if it's a teacher logged in
    if 'username' in session: 

        # # grab modules,name etc and pass in
        return redirect(url_for('home'))
    

        
    #if it's a student logged in    
    elif 's_no' in session:
        # grab modules,name etc and pass in
        return 'You are logged in as ' + session['s_no'] + '<br> You are a student!'
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
                return redirect(url_for('signIn'))
        if login_student : #if a student is logged in
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_student['password']) ==  login_student['password']:
                session['s_no'] = username_var  #store their student number in a session
                return redirect(url_for('signIn'))

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
                    print(module['owner'])
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
                    return redirect(url_for('signIn'))
                else: #otherwise redirect them to same page plus pass in error msg
                    error_msg = 'Invalid enrollment key, please try again'
                    print(error_msg)
                    return render_template('user_auth/register.html', errormsg=error_msg)
            else :
                error_msg = 'Not a valid username'
                return render_template('user_auth/register.html', errormsg=error_msg)

        #this is the else for the check to see if user is registered
        error_msg = 'This username already exists, please sign in or contact administrator for help'
        print(error_msg) 
        return render_template('user_auth/register.html', errormsg=error_msg)
       

    return render_template('user_auth/register.html')
    
@app.route('/checkModules',methods=['POST'])
def checkModules():
    modulesDB = mongo.db.modules

    module_1 = request.form['module1'] 
    module_2 = request.form['module2']
    module_3 = request.form['module3']
    module_4 = request.form['module4']
    module_5 = request.form['module5']
    module_6 = request.form['module6']

    selectedModules = [module_1,module_2,module_3,module_4,module_5,module_6]
    
    correctMods = []
    incorrectMods = []
    allModules = [
        {"correct": correctMods,
         "incorrect" : incorrectMods   
        }
    ]
    for module in selectedModules :
        if modulesDB.find_one({"mod_code" : module}) :
           correctMods.append(module)
        else :
            incorrectMods.append(module)
    return jsonify({'allModules' : allModules})


@app.route('/registerS', methods=['POST','GET'])
def registerS():
    if request.method == 'POST' :
       users = mongo.db.users 
       username_var = request.form['username']
       existing_user = users.find_one({'name' : username_var})

       if existing_user is None:
           user_type = 'student'
           hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
           users.insert({'s_no' : username_var, 'password' : hashpass, 'user_type' : user_type})
           session['s_no'] = username_var
           return redirect(url_for('registertwo'))
       return 'That username already exists' 
       
    return render_template('user_auth/registerS.html')

   




@app.route('/registertwo', methods=['POST','GET'])
# def submit():
#     if request.method == 'POST' :
#         #add modules to student 
#         #add student number to each module

def registertwo():
    if request.method == 'POST' :
        users = mongo.db.users
        modulesDB = mongo.db.modules
        module_1 = request.form['module1'] 

        module_2 = request.form['module2']

        module_3 = request.form['module3']

        module_4 = request.form['module4']

        module_5 = request.form['module5']

        module_6 = request.form['module6']

        modules = [module_1,module_2,module_3,module_4,module_5,module_6]
        modules_true = []
        modules_false = []
        for module in modules :
            current_module = modulesDB.find_one({"mod_code" : module})
            if  current_module :
                modules_true.append(module)
            else:
                if module:
                    modules_false.append(module)
        
                
        
        print (modules_true)
        print (modules_false)
       

        if 'username' in session : 

            #set selected modules to modules field in user table in following format -> modules = [module0,module1] with module* be a module code FN356
            #to show users modules we check module one to start with - if module[0] in db.users.modules = one instance of find_one(module[0] in modules.code is in db.modules 
                                                                      # set variable to be that module + its information(to show on page)
            

            # current_teacher_modules = users.find_one({'username':session['username']})['modules']
            # users.update_one({'username' : session['username']}, {'$set':{'modules': modules, 'registered' : 'true'}})
            # modules = modulesDB
            # for module in modules.mod_codes.find()
            
            #     existing_module = modulesDB.find({'') 
            #     if existing_module is None :
            #        module = "<h2 class='danger'> Not a correct Module Code, please try again</h2>"
            #     module = module 


            return render_template('user_auth/registertwo.html')
        
        if 's_no' in session : 
            users.update_one({'s_no' : session['s_no']}, {'$set':{'modules': modules, 'registered' : 'true'}})
            return render_template('user_auth/registertwo.html', modules_true=modules_true, modules_false=modules_false)

        # if ''

        # return render_template('user_auth/registertwo.html',name=current_student)
    return render_template('user_auth/registertwo.html')

@app.route('/home',methods=['POST','GET'])
def home() :

    if request.method == 'POST' :
         return render_template('home/homepage.html')
    
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
        current_teacher_modules = retrieve_user_modules(modules_var)
    return render_template('home/homepage.html', current_teacher_modules = current_teacher_modules,username = username, location=location, img_loc=img_loc)
#Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('s_no', None)
    return render_template('index.html')



########################     HELPER FUNCTIONS     #################

def retrieve_user_modules(modules) :
    modulesDB = mongo.db.modules
    print ("Length is : {}".format(len(modules)))

    ##### RETRIEVE ALL RELEVANT INFO FOR User-Specific Modules #####



    if len(modules[0]) == 1 :
        
        mod_code = modules
        mod_title = modulesDB.find_one({"mod_code" : modules})['mod_title']
        owner = modulesDB.find_one({"mod_code" : modules})['owner'] 


        ###### DATE INPUTTED WRONG

        # posts = []
        # # for post in modulesDB.find_one({"mod_code" : modules}).sort("date",-1) :
        # #     posts.append(post)
        
        # posts.append(modulesDB.find_one({"mod_code" : modulesDB})['posts']) 
        module1 = {
            'mod_code' : mod_code,
            'mod_title' : mod_title,
            # 'mod_posts' : posts,
            'owner' : owner
        }
        print (module1)
        return module1
    else :
        my_modules = []
        for module in modules :
            print(module)
            mod_code = module
            mod_title = modulesDB.find_one({"mod_code" : module})['mod_title']
            owner = modulesDB.find_one({"mod_code" : module})['owner'] 


            ################### NEED TO FORMAT POSTS CORRECTLY MAYBE TO DO WITH DATE
            # posts = []
            # for post in modulesDB.find_one({"mod_code" : module}).sort("date",-1) :
            #     posts.append(post)
            # posts = modulesDB.find_one({"mod_code" : module})['posts']
            modules_ready = {
                'mod_code' : mod_code,
                'mod_title' : mod_title,
                # 'mod_posts' : posts,
                'owner' : owner
            }
            my_modules.append(modules_ready)
            
        return my_modules


    

           

    


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)