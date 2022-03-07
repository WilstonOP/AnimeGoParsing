import bs4
import requests
from fake_useragent import UserAgent

ua = UserAgent()
header = {"User-Agent": ua.chrome}


def update_anime():
    result = list()
    req = requests.get('https://animego.org/', headers=header).text
    soup = bs4.BeautifulSoup(req, 'lxml')
    temp = soup.find('div', role='tabpanel')
    for i in temp:
        result.append({'Название': i.find('span').text, 'Серия': i.find('div', class_='ml-3 text-right').text,
                       'Ссылка': 'https://animego.org' + i.get('onclick').strip("'location.href='")})
    return packing(result)


def check_anime(nickname):
    request = requests.get('https://animego.org/user/' + nickname + '/mylist/anime/watching', headers=header).text
    soup = bs4.BeautifulSoup(request, 'lxml')
    temp = soup.find_all('tr')
    result = list()
    for i in temp[1:]:
        name = i.find(class_='text-left table-100').find('a').text
        series, anime_type = [i.find_all('td', class_='text-left text-md-center table-100')[1].text,
                              i.find_all('td', class_='text-left text-md-center table-100')[2].text]
        result.append({'Название': name.strip(), 'Серии': series.strip(), 'Тип': anime_type.strip()})
    return packing(result)


def season_anime():
    result = list()
    req = requests.get('https://animego.org/', headers=header).text
    soup = bs4.BeautifulSoup(req, 'lxml')
    temp = soup.find_all('div', class_='position-relative')
    temp2 = soup.find_all('div', class_='h5 font-weight-normal mb-2 card-title carousel-item-title text-truncate')
    temp3 = soup.find('a', class_='text-dark text__underline__link').text
    for i, j in zip(temp, temp2):
        result.append({'Название': j.text, 'Ссылка': i.find('a').get('href')})
    return temp3 + '\n\n' + packing(result)


def list_anime(nickname):
    anime_list = list()
    for page in range(1, 2):
        link = f'https://animego.org/user/{nickname}/mylist/anime/completed?type=mylist&page='
        link += str(page)
        resp = requests.get(link, headers=header)
        if resp.status_code == 200:
            res = resp.text
            soup = bs4.BeautifulSoup(res, 'lxml')
            anime = soup.find_all('td')
            i = 1
            while i < len(anime) - 4:
                anime_list.append(
                    {'name': '|'.join((anime[i].text.strip().split('\n            '))),
                     'rate': anime[i + 1].text.strip(),
                     'series': anime[i + 2].text.strip(), 'type': anime[i + 3].text.strip()})
                i += 5
        else:
            break
    if anime_list:
        return anime_list
    else:
        return 'Не могу найти данного пользователя'


def best_anime():
    res = requests.get('https://animego.org/anime?sort=r.rating&direction=desc', headers=header).text
    soup = bs4.BeautifulSoup(res, 'lxml')
    temp = soup.find_all('div', class_='h5 font-weight-normal mb-1')
    anime_list = list()
    for a in temp:
        elem = f"{a.text}, {a.find('a').get('href')}\n"
        anime_list.append(elem)
    return ' '.join(anime_list)


def popular_anime(n=3):
    anime_list = list()
    for i in range(1, n):
        link = "https://animego.org/anime?sort=r.rating&direction=desc&type=animes&page=" + str(i)
        res = requests.get(link, headers=header).text
        soup = bs4.BeautifulSoup(res, 'lxml')
        temp = soup.find_all('div', class_='h5 font-weight-normal mb-1')
        for a in temp:
            name, link2 = a.text, a.find('a').get('href')
            res1 = requests.get(link2).text
            soup1 = bs4.BeautifulSoup(res1, 'lxml')
            genres = soup1.find_all('dd', class_='col-6 col-sm-8 mb-1 overflow-h')
            for elem in range(0, len(genres) - 1, 2):
                genre = ', '.join(genres[elem].text.split(',                             '))
                studio = genres[elem + 1].text
            temp2 = soup1.find('div', class_='pr-2')
            if temp2 is not None:
                rate, votes = temp2.text.split('/10')
                anime_list.append({'Название': name, 'Ссылка': link2, 'Рейтинг': rate, 'Голоса': votes,
                                   'Жанр': genre, 'Студия': studio})
    sorted_salaries = sorted(anime_list, key=lambda d: int(d['Голоса']), reverse=True)
    return packing(sorted_salaries[0:13])


def random_anime():
    res = requests.get('https://animego.org/anime/random', headers=header).text
    soup = bs4.BeautifulSoup(res, 'lxml')
    anime_list = list()
    anime_list.append(f"Название: {soup.find('div', class_='anime-title').find('h1').text}")
    anime_list.append(f"Жанры: {' '.join(soup.find('dd', class_='col-6 col-sm-8 mb-1 overflow-h').text.split())}")
    if (soup.find('div', class_='pr-2').text.split()[0]) == 'Нет':
        anime_list.append('Нет оценок')
    else:
        anime_list.append(f"Оценка: {soup.find('div', class_='pr-2').text[:6]}")
    return '\n'.join(anime_list)


def packing(result):
    if result:
        final = ''
        for i in result:
            for key, value in i.items():
                final += f'{str(key)}: {str(value)}\n'
            final += '\n'
        return final
    else:
        return 'Ошибка. Пустой ответ'
