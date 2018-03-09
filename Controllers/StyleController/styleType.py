from . import *

# Style type json file
@style.route('/styleInfluencers/<string:styles_type>/influencers/JSON')
@login_required
def stylesInfluencersJSON(styles_type):
	style = session.query(Type).filter_by(type=styles_type).one()
	influencers = session.query(Influencers).filter_by(styles=styles).all()
	return jsonify(influencers=[i.serialize for i in influencers])
