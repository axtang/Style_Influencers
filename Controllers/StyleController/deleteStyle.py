from . import *

# Delete a style type
@app.route('/styles/<string:styles_type>/delete', method=['GET', 'POST'])
@login_required
def deleteStyle(styles_id, styles_type):
	styles = session.query(Styles).filter_by(id=styles_id).one()
	deletingStyle = session.query(Styles).filter_by(type=styles_type).one()
	creator = getUserInfo(deletingStyle.user_id)
	user = getUserInfo(login_session['user_id'])
	if creator.id != login_session['user_id']:
		flash("You cannot delete this style. This Style belongs to a different user.")
		return redirect(url_for('index.html'))
	if request.method == 'POST':
		session.delete(deletingStyle)
		session.commit()
		flash("You have successfully deleted %s!" % deletingStyle_type)
		return redirect(url_for('index.html',
								styles_type=styles.type))
	else:
		return render_template('deleteStyle.html',
								style=deletingStyle)
