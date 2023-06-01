from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user # import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/')
def direct_to_register():
    return redirect('/user/login')

@app.route('/user/register', methods=['POST' , 'GET'])
def user_register():
    if request.method == 'GET':
        return render_template('register.html',  user_input = session.get('user_registration_input', ''))

    #post method if valid registration
    if  user.User.create_user(request.form):
        return redirect('/user/profile')
    #if invalid registration store their form and send them back to registration with their previous form data
    session['user_registration_input'] = request.form
    return redirect('/user/register')


# Read Users Controller
@app.route('/user/profile')
def show_user_profile():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('profile.html')

@app.route('/user/login' , methods=['POST' , 'GET'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    if user.User.login_user(request.form):
        return redirect('/user/profile')
    session['user_login_email'] = request.form['email']
    return redirect('/user/login')

@app.route('/user/logout')
def user_logout():
    session.clear()
    return redirect('/')

# Update Users Controller



# Delete Users Controller


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.