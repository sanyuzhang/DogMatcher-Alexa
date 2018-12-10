from bs4 import BeautifulSoup
import re
import os
import sys
import sqlite3
import requests
import threading


LINE_SEPARATOR = '\n'
BAR_SEPARATOR = '-'
COMMA_SEPARATOR = ','

BASE_URL = 'https://www.akc.org/dog-breeds/'

TEMERAMENT_HTML_CLASS = 'attribute-list__description attribute-list__text attribute-list__text--lg mb4 bpm-mb5 pb0 d-block'
DESC_HTML_CLASS = 'breed-hero__footer'
DETAILS_HTML_CLASS = 'attribute-list__description attribute-list__text '
IMAGE_HTML_CLASS = 'media-wrap__image'

DOGS_URLS_FILE = 'dogs2urls.txt'
ERROR_LOG = 'error_dogs.txt'

def write_error_dogs(url, dog_name):
    """ Write error logs to file

    Args:
        url: current url requested
        dog_name: name of the current dog 
    """
    ERROR_LOG_HANDLER = open(ERROR_LOG, 'a+')
    ERROR_LOG_HANDLER.write(url + LINE_SEPARATOR)
    ERROR_LOG_HANDLER.write(dog_name + LINE_SEPARATOR * 2)
    ERROR_LOG_HANDLER.close()


def get_dog_url_lst(fname):
    """ Load query data from input file, then return an array of dicts.

    Args:
        fname: the absolute path of the input file.

    Returns:
        The return value. An array of dicts:
        [
            {
                'dog': 'Shetland Sheepdog',
                'url': 'https://www.akc.org/dog-breeds/shetland-sheepdog/'
            },
            ...
        ]
    """
    raw = open(fname, 'r').read()
    dogs_urls = raw.split(LINE_SEPARATOR * 2)
    dog_url_lst = [{'dog': pair.split(LINE_SEPARATOR)[1], 'url': pair.split(LINE_SEPARATOR)[0]} for pair in dogs_urls if len(pair) > 1]
    return dog_url_lst


def get_html(url):
    """ Get html content via http request

    Args:
        url: to be visited by http request

    Returns:
        The return value. Content of html:
        <!DOCTYPE html>
        <html>
        <body>
        </body>
        </html>
    """
    try:
        page = requests.get(url)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print('Exception Timeout:', url)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print('Exception TooManyRedirects:', url)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print('Exception RequestException', url)
        print(e)

    if page.status_code == 200:
        return page.text
    else:
        return None


def parse_2_store(dog_name, html, url):
    """ Parse html content and then store to database

    Args:
        dog_name: the name of current dog
        html: html contents
        url: requested url
    """
    print("STORING DOG -", dog_name, url)
    try:
        dog_insert_cols = "name, desc, height_min, height_max, weight_min, weight_max, life_expectancy_min, life_expectancy_max, image, dog_group, activity_level, barking_level, coat_type, shedding, size, trainability, popularity, url"
        dog_group_id, activity_level_id, barking_level_id, coat_type_id, shedding_id, trainability_id, size_id = -1, -1, -1, -1, -1, -1, -1
        popularity, height_min, height_max, weight_min, weight_max, life_expectancy_min, life_expectancy_max = -1, sys.maxsize, -1, sys.maxsize, -1, sys.maxsize, -1
        characteristic_ids, temperament_ids = [], []
        image = ''

        soup = BeautifulSoup(html, 'html.parser')

        desc_htmls = soup.find_all('div', class_ = DESC_HTML_CLASS)
        desc = desc_htmls[0].get_text()

        detail_htmls = soup.find_all('span', class_ = DETAILS_HTML_CLASS)
        for i in range(len(detail_htmls)):
            detail = detail_htmls[i].get_text()
            if 'Rank' in detail:
                popularity = detail
            elif 'inch' in detail:
                heights =  re.findall('\d+',detail)
                for h in heights:
                    h = float(h)
                    height_min = h if h < height_min else height_min
                    height_max = h if h > height_max else height_max
            elif 'pound' in detail:
                weights = re.findall('\d+',detail)
                for w in weights:
                    w = float(w)
                    weight_min = w if w < weight_min else weight_min
                    weight_max = w if w > weight_max else weight_max
            elif 'year' in detail:
                life_expectancy = re.findall('\d+',detail)
                for l in life_expectancy:
                    l = float(l)
                    life_expectancy_min = l if l < life_expectancy_min else life_expectancy_min
                    life_expectancy_max = l if l > life_expectancy_max else life_expectancy_max
            elif i == len(detail_htmls) - 1:
                dog_group = detail.strip().lower()
                dog_group_id = db_select('dog_groups', 'desc', dog_group)[0]
        
        image_htmls = soup.find_all('img', class_ = IMAGE_HTML_CLASS)
        if len(image_htmls) > 0:
            image = image_htmls[1].get('src')
        
        character_detail = (re.findall(r"googletag\.pubads\(\)\.setTargeting\('characteristic'.*", html)[0]).split("[")[1].split("]")[0]
        character_details = character_detail[1 : -1].replace(BAR_SEPARATOR, ' ').split('","')
        for detail in character_details:
            if 'activity level ' in detail:
                activity_level = detail.split('activity level ')[1]
                activity_level_id = db_select('activity_levels', 'desc', activity_level)[0]
            elif 'barking level' in detail:
                barking_level = detail.split('barking level ')[1]
                barking_level_id = db_select('barking_levels', 'desc', barking_level)[0]
            elif 'characteristic' in detail:
                characteristic = detail.split('characteristic ')[1]
                characteristic_ids.append(db_select('characteristics', 'desc', characteristic)[0])
            elif 'coat type' in detail:
                coat_type = detail.split('coat type ')[1]
                coat_type_id = db_select('coat_types', 'desc', coat_type)[0]
            elif 'shedding' in detail:
                shedding = detail.split('shedding ')[1]
                shedding_id = db_select('sheddings', 'desc', shedding)[0]
            elif 'trainability' in detail:
                trainability = detail.split('trainability ')[1]
                trainability_id = db_select('trainabilities', 'desc', trainability)[0]
            elif 'temperament' in detail:
                temperament = detail.split('temperament ')[1]
                result = db_select('temperaments', 'desc', temperament)
                if result:
                    temperament_ids.append(result[0])
                else:
                    temperament_ids.append(db_insert_single('temperaments', 'desc', (temperament,)))
        size_htmls = re.findall(r"googletag\.pubads\(\)\.setTargeting\('size'.*", html)
        if len(size_htmls) > 0:
            size = (size_htmls[0]).split(',')[1].split('"')[1]
            size_id = db_select('sizes', 'desc', size)[0]

        dog_insert_data = (
        dog_name, desc, height_min, height_max, weight_min, weight_max, life_expectancy_min, life_expectancy_max, 
            image, dog_group_id, activity_level_id, barking_level_id, shedding_id, coat_type_id, size_id, trainability_id, popularity, url
        )
        dog_id = db_insert_single('dogs', dog_insert_cols, dog_insert_data)

        characteristic_insert_data = []
        for cid in characteristic_ids:
            characteristic_insert_data.append((dog_id, cid))
        db_insert_many('dogs_characteristics', 'dog_id, characteristic_id', characteristic_insert_data)

        temperament_insert_data = []
        for tid in temperament_ids:
            temperament_insert_data.append((dog_id, tid))
        db_insert_many('dogs_temperaments', 'dog_id, temperament_id', temperament_insert_data)
    
    except Exception as e:
        print('STORING FAILED DOG -', dog_name, url)
        write_error_dogs(url, dog_name)


def db_select(table, col, value):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM %s WHERE %s = '%s'" % (table, col, value))
    return cursor.fetchone()


def db_insert_single(table, cols, value):
    cursor = conn.cursor()
    num_of_cols = len(cols.split(COMMA_SEPARATOR))
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, ('?,' * num_of_cols)[:-1])
    cursor.execute(sql, value)
    last_id = cursor.lastrowid
    return last_id


def db_insert_many(table, cols, values):
    cursor = conn.cursor()
    num_of_cols = len(cols.split(COMMA_SEPARATOR))
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, ('?,' * num_of_cols)[:-1])
    cursor.executemany(sql, values)


if __name__ == '__main__':
    
    HANDLING_ERROR = False
    if HANDLING_ERROR:
        dog_url_lst = get_dog_url_lst(ERROR_LOG)
    else:
        dog_url_lst = get_dog_url_lst(DOGS_URLS_FILE)

    conn = sqlite3.connect('../dogs.db3', isolation_level=None, check_same_thread=False)
    for pair in dog_url_lst:
        dog = pair['dog']
        url = pair['url']
        html = get_html(url)
        if html:
            threading.Thread(target=parse_2_store, args=(dog, html, url)).start()

    # conn.close()
