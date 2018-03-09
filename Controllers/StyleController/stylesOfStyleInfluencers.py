from . import *

# Styles json file
@style.route('/styleInfluencers/styles/JSON')
@login_required
def stylesJSON():
	styles = session.query(Styles).all()
	styles_dict = [s.serialize for s in styles]
	for s in range(len(styles_dict)):
		type = [i.serialize for i in session.query(Type).filter_by(styles_id=styles_dict[s]["id"]).all()]
		if type: 
			type_dict[c]["type"] = type
	return jsonify(Styles=styles_dict)
