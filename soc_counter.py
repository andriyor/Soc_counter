import time
import grequests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

handle = 'rozetked'

link_list = ["https://www.youtube.com/user/{}/about?hl=en".format(handle),
             "https://twitter.com/{}".format(handle),
             "https://www.instagram.com/{}".format(handle),
             "https://www.facebook.com/{}".format(handle)]


def fetch_youtube_subscriber(page):
    soup = BeautifulSoup(page, 'html.parser')
    about_stat = soup.find_all("span", {"class": "about-stat"})
    ys, bl, jl, = map(lambda x: x.text, about_stat)
    ys = ys.split()[0]
    return ys


def fetch_twitter_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'}) \
        .find('span', {'class': 'ProfileNav-value'}).text
    return followers


def fetch_instagram_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find("meta", property="og:description")["content"]
    followers = followers.split()[0]
    return followers


def fetch_facebook_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    desc = soup.find(attrs={"name": "description"})["content"]
    descl = desc.split()

    for i in descl:
        if i.isdigit():
            first_int = i
            break

    followers = ''
    for j in descl[descl.index(first_int):]:
        if j.isdigit():
            followers += j
        else:
            break
    return followers


@app.route('/')
def index():
    start_time = time.time()
    rs = (grequests.get(u) for u in link_list)
    y, t, i, f = list(map(lambda x: x.text, grequests.map(rs)))
    ys = fetch_youtube_subscriber(y)
    tf = fetch_twitter_followers(t)
    instagram_followers = fetch_instagram_followers(i)
    ff = fetch_facebook_followers(f)
    print("--- %s get ---" % (time.time() - start_time))
    return render_template("index.html", ys=ys, tf=tf, instagram_followers=instagram_followers, ff=ff)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
