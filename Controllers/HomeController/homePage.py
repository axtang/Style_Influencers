from . import *

# Home page
@home.route('/')
@home.route('/home')
def Home():
	styles = session.query(Styles).order_by(asc(Styles.type))
	influencers = session.query(Influencers).order_by(asc(Influencers.name))
	return render_template('index.html', styles=Styles, influencers=Influencers)