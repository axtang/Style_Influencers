from . import *

# Styles and influencers json file
@style.route('/styleInfluencers/JSON')
@login_required
def allStyleInfluencersJSON():
	styles = session.query(Styles).all()
	styles_dict = [s.serializes for s in styles]
	for s in range(len(styles_dict)):
		categories = [c.serialize for c in session.query(Type).filter_by(styles_id=styles_dict[c]["id"]).all()]
		if categories:
			styles_dict[c]["type"] = categories
