from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, session

from agents.db.users import Users
from agents.mailing.mails import Mail
from config import MASTER_EMAIL, PASSWORD


app = Flask(__name__)
app.secret_key = "........"
app.permanent_session_lifetime = timedelta(minutes=9999) # how long youn want your session to be stored

# project's classes and objects
usr = Users()
mail = Mail(MASTER_EMAIL, PASSWORD)


"""--------------------------------------------------INDEX PAGE------------------------------------------------------------------------------"""
# POST method for form submission
@app.route('/', methods=['GET', 'POST'])
def index():
	# checks if you already registered, if yes then sends you to results page
	if 'email' in session:
		return redirect(url_for('results'))
	

	# if not registered then the following code executes
	else:
		# this if statement means if user pressed on the submit button
		if request.method=='POST':
			session.permanent = True
			
			# getting data from the register form
			name_ = request.form['name']
			max_temp = request.form['maxt']
			min_temp = request.form['mint']
			email = request.form['email']

			longitude = request.form['ln']
			latitude = request.form['lat']

			# storing session data to make retrieval of user data fast instead of requesting the 
			# database everytime user refreshes the page
			session['email'] = email
			session['max_temp'] = max_temp
			session['min_temp'] = min_temp
			session['name'] = name_
			session['lat'] = latitude
			session['long'] = longitude
			#print(name_, max_temp, min_temp, email, latitude, longitude)

			# passing data to database module to store the user info
			usr.data_entry(name_, max_temp, min_temp, latitude, longitude, email)
			return redirect(url_for('results'))
		
		else:
			return render_template('index.html')
"""--------------------------------------------------------------------------------------------------------------------------------------"""



"""------------------------------------------------------RESULTS PAGE---------------------------------------------------------------------"""
@app.route('/results', methods = ['GET', 'POST'])
def results():
	# this url shows your basic info and has the button to cancel subscription
	if 'email' in session:
		if request.method == 'POST':
			return redirect(url_for('clear')) # more on this function later
		
		else:
			# getting session data instead of querying database again as mentioned earlier
			email = session['email']
			name_ = session['name']
			max_temp = session['max_temp']
			min_temp = session['min_temp']
			latitude = session['long']
			longitude = session['lat']

			# sending registration confirmation mail
			mail.send(email, "You've been succesfully registered! You will get a noitification from mails in this manner if temperature goes out of your desired range!")

			# passing session data to results page
			return render_template('results.html', name=name_, mt=max_temp, mnt=min_temp, em=email, lat=latitude, ln=longitude)
	else:
		return redirect(url_for('index'))
	
"""--------------------------------------------------------------------------------------------------------------------------------------"""



"""-------------------------------------------------------LOGOUT PAGE-----------------------------------------------------------------------"""
@app.route('/e')
def clear():
	# this function clears data of the current user data and stop mailing
	try:
		email__ = session['email']
		usr.delete(email__)
		session.pop('email')
		session.pop('max_temp')
		session.pop('min_temp')
		session.pop('name')
		session.pop('lat')
		session.pop('long')

	except Exception as e:
		print(e)
	return redirect(url_for('index'))

"""--------------------------------------------------------------------------------------------------------------------------------------"""
		
