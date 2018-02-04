from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'unifeed'
app.config['MONGO_URI'] = 'mongodb://donaldev:password@ds113098.mlab.com:13098/unifeed'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/signIn')
def signIn():
    if 'username' in session:
        return 'You are logged in as ' + session['username'] + '<br> You are a teacher!'
    elif 's_no' in session:
        return 'You are logged in as ' + session['s_no'] + '<br> You are a student!'
    return render_template('user_auth/login.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST' :
        users = mongo.db.users
        username_var = request.form['username']
        login_teacher = users.find_one({'username' : username_var})
        login_student = users.find_one({'s_no' : username_var})
        if login_teacher :
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_teacher['password']) ==  login_teacher['password']:
                session['username'] = username_var  
                return redirect(url_for('registertwo'))
        if login_student :
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_student['password']) ==  login_student['password']:
                session['s_no'] = username_var
                return redirect(url_for('registertwo'))
        else:
            return redirect(url_for('login'))
    return render_template('user_auth/login.html')


# @app.route('/registertwo', methods=['POST','GET'])
# def registertwo():
#     if request.method == 'POST'

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST' :
       users = mongo.db.users
    #    user1 = mongo.db.users.name
       username_var = request.form['username'] 
       existing_user = users.find_one({'username' : username_var})

       if existing_user is None:
           user_type = 'teacher'
           hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
           users.insert({'username' : username_var, 'password' : hashpass, 'user_type' : user_type})
           session['username'] = username_var
           return redirect(url_for('registertwo'))
       return 'That username already exists' 
       
           

    return render_template('user_auth/register.html')


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
def get_modules(modules):
    modules_true = []
    modules_false = []
    for module in modules :
            current_module = modulesDB.find_one({"mod_code" : module})
            if  current_module :
                modules_true.append(module)
            else:
                if module:
                    modules_false.append(module)
    return modules_true,modules_false

# @app.route('/registertwo', methods=['POST','GET'])
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
        check_modules(modules)
        modules_true = []
        modules_false = []
        
                
        
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
            current_student = users.find_one({'s_no':session['s_no']})['s_no']
            users.update_one({'s_no' : session['s_no']}, {'$set':{'modules': modules, 'registered' : 'true'}})
            return render_template('user_auth/registertwo.html', modules_true=modules_true, modules_false=modules_false)

        # if ''

        # return render_template('user_auth/registertwo.html',name=current_student)
    return render_template('user_auth/registertwo.html')



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)