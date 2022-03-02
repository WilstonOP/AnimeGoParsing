import bs4
import requests
from fake_useragent import UserAgent
from selenium import webdriver

global LAST_SER
LAST_SER = 0
global SITES
SITES = list()
ua = UserAgent()
headers = {"User-Agent": ua}
#rec = requests.get("https://animego.org/anime/reyting-korolya-m1883")
#s_soup = bs4.BeautifulSoup(rec.text, 'lxml')


def check_anime(nickname):
    request = requests.get('https://animego.org/user/' + nickname + '/mylist/anime/watching').text
    soup = bs4.BeautifulSoup(request, 'lxml')
    temp = soup.find_all('td', class_='text-left table-100')
    for i in temp:
        SITES.append(f'https://animego.org{(i.find("a").get("href"))}')
    for site in SITES:
        rec = requests.get(site)
        s_soup = bs4.BeautifulSoup(rec.text, 'lxml')
        result = list()
        result.append(f"{s_soup.title.text.rstrip('смотреть онлайн — Аниме')}")

        # for i in s_soup.find_all("div", class_='row m-0')[1:]:
        # print(i.text)
        try:
            result.append(f"На данный момент доступно {s_soup.find_all('dd', class_='col-6 col-sm-8 mb-1')[1].text} серий\n")
        except IndexError:
            print('Ой')
        if result:
            yield '\n'.join(result)
        else:
            yield 'Не могу найти данного пользователя'


def list_anime(nickname):
    res = requests.get('https://animego.org/user/' + nickname + '/mylist/anime/completed').text
    soup = bs4.BeautifulSoup(res, 'lxml')
    anime_list = list()
    anime = soup.find_all('td')
    i = 1
    while i < len(anime) - 4:
        anime_list.append({'name': '|'.join((anime[i].text.strip().split('\n            '))), 'rate': anime[i + 1].text.strip(),
                           'series': anime[i + 2].text.strip(), 'type': anime[i + 3].text.strip()})
        i += 5

    if anime_list:
        return anime_list
    else:
        return'Не могу найти данного пользователя'


def best_anime():
    res = requests.get('https://animego.org/anime?sort=r.rating&direction=desc').text
    soup = bs4.BeautifulSoup(res, 'lxml')
    temp = soup.find_all('div', class_='h5 font-weight-normal mb-1')
    anime_list = list()
    for a in temp:
        elem = f"{a.text}, {a.find('a').get('href')}\n"
        anime_list.append(elem)
    print(len(anime_list))
    return ' '.join(anime_list)


def random_anime():
    res = requests.get('https://animego.org/anime/random').text
    soup = bs4.BeautifulSoup(res, 'lxml')
    anime_list = list()
    anime_list.append(soup.find('div', class_='anime-title').find('h1').text)
    anime_list.append(f"Жанры: {''.join(soup.find('dd', class_='col-6 col-sm-8 mb-1 overflow-h').text.split())}")
    if (soup.find('div', class_='pr-2').text.split()[0]) == 'Нет':
        anime_list.append('Нет оценок')
    else:
        anime_list.append((soup.find('div', class_='pr-2').text[:6]))

    return '\n'.join(anime_list)


def loop_new_check():
    global LAST_SER
    result = list()
    rec = requests.get("https://animego.org/anime/reyting-korolya-m1883")
    s_soup = bs4.BeautifulSoup(rec.text, 'lxml')
    for i in s_soup.find('span', class_="d-none d-sm-inline"):
        current = (''.join([i for i in i.text if i.isdigit()]))
    if int(current) == '':
        result.append('Аниме закончилось(')
    elif int(current) == int(LAST_SER):
        result.append(f"Серия {int(LAST_SER)-1} вышла!, Ждем теперь {int(LAST_SER)}")
        result.extend(new_check())
        LAST_SER = int(LAST_SER) + 1
    elif int(current) > int(LAST_SER):
        LAST_SER = current
        result.append(f"Я неусмотрела за последней серией. Теперь последняя доступная серия - {int(current)-1}")
    elif int(current) < int(LAST_SER):
        current = current
        result.append(f"{current} к сожалению еще не вышла. Ждем!")
        result.extend(new_check())
        print(result)
    return '\n'.join(result)


