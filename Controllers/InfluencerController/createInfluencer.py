from . import *

# Add a new influencer
@app.route('/influencers/new', methods=['GET', 'POST'])
@login_required
def newInfluencer(influencer_id):
    if request.method == ['POST']:
        newInfluencer= Influencer(
            name = request.form['name'],
            country = request.form['country'],
            blogName = request.form['blogName'],
            description = request.form['description'],
            picture = requet.form['picture'])
        print (newInfluencer)
        session.add(newInfluencer)
        flash('You have sucessfully added %s as a new influencer!' % newInfluencer.name)
        session.commit()
        return redirect(url_for('index.html'))
    else:
        return render_template('newInfluencer.html')
