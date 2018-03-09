from . import *

# Display all styles
@style.route('/styles', methods=['GET', 'POST'])
def showStyles(type):
	allStyles = session.query(Styles).order_by(asc(Styles.type)).all()
    oneStyle = session.query(Styles).filter_by(asc(allStyles_type)).one()
    print (style, influencers)
	creator = getUserID(type.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicStyles.html',
								oneStyle=style.type,
								allStyles=styles,
								influencers=influencers
								)
	else:
		user = getUserInfo(login_session['user_id'])
		return render_template('styles.html',
								allStyles=styles,
								oneStyle=style.type,
								influencers=influencers)
