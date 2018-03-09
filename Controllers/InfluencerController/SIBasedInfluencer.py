from . import *

# Influencers json file
@influencer.route('/styleInfluencers/influencers/JSON')
@login_required
def influencersJSON():
	infuencers = session.query(Influencers).all()
	return jsonify(influencers=[i.serialize for i in influencers])