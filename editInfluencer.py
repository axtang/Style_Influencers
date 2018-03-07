from . import *

# Edit an influencer
@app.route('/influencers/<string:influencers_name>/edit', method=['GET'], ['POST'])
@login_required
def editInfluencers(influencers_name):
    editInfluencer = session.query(Influencers).filter_by(name=influencer_name).one()
    creator = getUserinfo(editInfluencer.user_id)
    user = getUserInfo(login_session['user_id'])

    # if the influencer was not associated with the user
    if creator.id != login_session['user_id']:
        flash("Sorry, you cannot eit this influencer.")
        return redirect(url_for('index.html'))
    else:
        # edit the influencer
        if request.method == 'POST':
            if request.form['name']:
                editInfluencer.name = request.form['name']
            session.add(editInfluencer)
            session.commit()
            flash('You have successfully edited an influencer!')
            return redirect(url_for('index.html'))
        else:
            return render_template('editInfluencer.html',
                                    influencers=editInfluecers,
                                    influencer=influencer)
