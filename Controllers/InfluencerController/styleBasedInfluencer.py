from . import *

# Display a specfic influencer based on a specific style
@app.route('/<string:styles_type>/<string:influencers_name>', methods=['GET', 'POST'])
def showStyleInfluencer(styles_type, influencers_name):
	styles = session.query(Styles).order_by(asc(Styles.type))
	style = session.query(Styles).filter_by(styles_type).one()
	influencer = session.query(Influencers).filter_by(Style=style).order_by(asc(name=influencers_name)).one()
    print(style, influencer)

	creator = getUserInfo(influencer.user_id)
	if 'username' not in login_session or creator.id != login_sessin['user_id']:
		return render_template('publicInfluencers.html',
								styles=styles.type,
								influencer=influencers.name)
	else:
		return render_template('influencers.html',
								styles=styles.type,
								influencer=influencers.name)
