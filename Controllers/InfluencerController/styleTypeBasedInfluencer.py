from . import *

# Influencer based on style type json file
@influencer.route('/styleInfluencers/<string:styles_type>/<string:influencer_name>/JSON')
@login_required
def influencerStylesJSON():
	styles = session.query(Styles).filter_by(type=styles_type).one()
	influencer = session.query(Influencers).filter_by(blog_name=influencer_blogName, type=styles_type).one()
	return jsonify(influencers=[influencers.serialize])
