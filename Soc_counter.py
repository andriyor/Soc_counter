import time
from flask import Flask, render_template
import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientSession

app = Flask(__name__)

handle = 'rozetked'


def get_youtube_subscriber(page):
    soup = BeautifulSoup(page, 'html.parser')
    about_stat = soup.find_all("span", {"class": "about-stat"})
    ys, bl, jl, = map(lambda x: x.text, about_stat)
    ys = ys.split()[0]
    return ys


def get_twitter_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'}) \
        .find('span', {'class': 'ProfileNav-value'}).text
    return followers


def get_instagram_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find("meta", property="og:description")["content"]
    followers = followers.split()[0]
    return followers


def get_facebook_followers(page):
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


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run():
    tasks = []
    async with ClientSession() as session:
        link_list = ["https://www.youtube.com/user/{}/about?hl=en".format(handle),
                     "https://twitter.com/{}".format(handle),
                     "https://www.instagram.com/{}".format(handle),
                     "https://www.facebook.com/{}".format(handle)]

        for link in link_list:
            task = asyncio.ensure_future(fetch(link, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


@app.route('/')
def hello_world():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    y, t, i, f = loop.run_until_complete(future)
    ys = get_youtube_subscriber(y)
    tf = get_twitter_followers(t)
    instagram_followers = get_instagram_followers(i)
    ff = get_facebook_followers(f)
    print("--- %s get ---" % (time.time() - start_time))
    return render_template("index.html", ys=ys, tf=tf, instagram_followers=instagram_followers, ff=ff)


if __name__ == '__main__':
    app.run(debug=True)
