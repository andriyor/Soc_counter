from bs4 import BeautifulSoup


def youtube(page):
    soup = BeautifulSoup(page, 'html.parser')
    about_stat = soup.find_all("span", {"class": "about-stat"})
    ys, bl, jl, = map(lambda x: x.text, about_stat)
    ys = ys.split()[0]
    return ys


def twitter(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'}) \
        .find('span', {'class': 'ProfileNav-value'}).text
    return followers


def instagram(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find("meta", property="og:description")["content"]
    followers = followers.split()[0]
    return followers


def facebook(page):
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