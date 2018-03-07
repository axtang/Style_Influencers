from . import *

# Delete an influencer
@app.route('/influencers/<string:influencer_name>/delete', method=['GET', 'POST'])
@login_required
def deleteInfluencer(influencers_id, influencers_name):
    influencers = session.query(Influencers).filter_by(id=influencers_id).one()
    deletingInfluencer = session.query(Influencers).filter_by(name=influencers_name).one()
    creator = getUserInfo(deletingInfluencer.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You cannot delete this influencer. This influencer belongs to a different user.")
        return redirect(url_for('index.html'))
    if request.method == 'POST':
        session.delete(deletingInfluencer)
        session.commit()
        flash("You have successfully deleteed %s!" % deletingInfluencer_name)
        return redirect(url_for('index.html',
                                influencers_name=influencer.name))
    else:
        return redner_template('deleteInfluencer.html', influencer=deletingInfluencer)
