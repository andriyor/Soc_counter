import time
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

handle = 'rozetked'


def get_youtube_subscriber():
    url = "https://www.youtube.com/user/{}/about?hl=en".format(handle)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    about_stat = soup.find_all("span", {"class": "about-stat"})
    ys, bl, jl, = map(lambda x: x.text, about_stat)
    ys = ys.split()[0]
    return ys


def get_twitter_followers():

    url = "https://twitter.com/{}".format(handle)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    followers = soup.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'}) \
        .find('span', {'class': 'ProfileNav-value'}).text
    return followers


def get_instagram_followers():
    url = "https://www.instagram.com/{}".format(handle)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    followers = soup.find("meta", property="og:description")["content"]
    followers = followers.split()[0]
    return followers


def get_facebook_followers():
    url = "https://www.facebook.com/{}".format(handle)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
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
def hello_world():
    start_time = time.time()
    ys = get_youtube_subscriber()
    print("--- %s get_youtube_subscriber ---" % (time.time() - start_time))

    start_time = time.time()
    tf = get_twitter_followers()
    print("--- %s get_twitter_followers ---" % (time.time() - start_time))

    start_time = time.time()
    instagram_followers = get_instagram_followers()
    print("--- %s get_instagram_followers ---" % (time.time() - start_time))

    start_time = time.time()
    ff = get_facebook_followers()
    print("--- %s get_facebook_followers ---" % (time.time() - start_time))

    return render_template("index.html", ys=ys, tf=tf, instagram_followers=instagram_followers, ff=ff)


if __name__ == '__main__':
    app.run(debug=True)

