from . import *

# Edit a style
@style.route('/styles/<string:styles_type>/edit', method=['GET', 'POST'])
@login_required
def editStyle(styles_type):
	editStyle = session.query(Styles).filter_by(type=styles_type).one()
	creator = getUserInfo(editStyle.user_id)
	user = getUserInfo(login_session['user_id'])

	# if the style was not associated with the user
	if creator.id != login_session['user_id']:
		flash("Sorry, you cannot edit this style.")
		return redirect(url_for('index.html'))
	else:
		# edit the style
		if request.method == 'POST':
			if request.form['type']:
				editStyle.type = request.form['type']
			session.add(editStyle)
			session.commit()
			flash('You have successfully edited a style!')
			return redirect(url_for('index.html'))
		else:
			return render_template('editStyle.html',
									styles=editStyle,
									style=style)
