import time

import grequests
from flask import render_template, Blueprint
from flask_login import login_required, current_user

from forms import LinksForm
from models import Links
from parsers import youtube, twitter, instagram, facebook

main = Blueprint('main', __name__, template_folder='templates')


@main.app_errorhandler(404)
def page_not_found():
    return render_template('404.html')


@main.app_errorhandler(500)
def internal_server_error():
    return render_template('500.html')


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = LinksForm()
    if form.validate_on_submit():
        links = Links(form.youtube.data, form.twitter.data,
                      form.instagram.data, form.facebook.data)
        current_user.links = links
        current_user.save()
    return render_template('user_profile.html', form=form)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    start_time = time.time()

    link_list = [current_user.links.youtube,
                 current_user.links.twitter,
                 current_user.links.instagram,
                 current_user.links.facebook]

    rs = (grequests.get(u) for u in link_list)
    y, t, i, f = list(map(lambda r: r.text, grequests.map(rs)))
    ys = youtube(y)
    tf = twitter(t)
    insta = instagram(i)
    ff = facebook(f)
    print("--- %s get ---" % (time.time() - start_time))
    return render_template("index.html", ys=ys, tf=tf, instagram=insta, ff=ff)
