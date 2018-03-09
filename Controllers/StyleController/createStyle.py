from . import *

# Add a style
@style.route('/styles/new', methods=['GET', 'POST'])
@login_required
def newStyle():
	if request.method == 'POST':
		newStyle = Styles(
			type = request.form['type'],
			user_id = login_session['user_id'])
		print(newStyle)
		session.add(newStyle)
		flash('You have successfully added %s as a new style!' % newStyle.type)
        session.commit()
		return redirect(url_for('index.html'))
	else:
		return render_template('newStyle.html')
