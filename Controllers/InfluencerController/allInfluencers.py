from . import *

# Display all influencers
@app.route('/influencers', methods=['GET', 'POST'])
def showInfluencers(blogName):
    influencers = session.query(Influencers).order_by(asc(Influencers.blogName)).all()
    influencer = session.query(Influencers).filter_by(asc(influencers_blogName)).one()
    print(influencers)
    creator = getUserID(type.user_id)
    if 'username' not in login_session or creator.id != login_session['user.id']:
        return render_template('publicInfluencers.html'
                                influencer=influencer.blogName,
                                influencers=influencers)
    else:
        return render_template('influencers.html',
                                influencer=influencer.blogName,
                                influencers=influencers)
