import requests
import os
import sqlite3
from random import choice, randint
from time import sleep
from selenium import webdriver


def get_driver(proxy):
    options = webdriver.ChromeOptions()
    #options.binary_location = '/usr/bin/chromedriver' # '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_argument('--window-size=800x841')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--proxy-server=%s' % proxy)
    return webdriver.Chrome(chrome_options=options)


def get_proxy():
    api = 'http://pubproxy.com/api/proxy?limit=5&level=elite&speed=10&last_check=5&https=true'
    proxies = requests.get(api).json()
    list_of_endpoints = []
    for proxy in proxies['data']:
        list_of_endpoints.append(proxy['ipPort'])
    return list_of_endpoints


def time_gen(type='large'):
    if type == "small":
        return randint(15, 60)
    else:
        return randint(2100, 3900)


def message_generator(guide_firstname, username, country):
    msg0 = 'Hello %s my name is %s, I was wondering if you are listed on Tourzan.com? I am looking for someone to show me around when I visit but i am '\
           'wanting to experience more of the local scene. I like the social first aspect of tourzan and its easier to '\
           'talk to locals on their site and organize trips. The payment process is a bit nicer too as it is cashless, wich I prefer. '\
           'I was curious about what things you could show me in %s and if you would '\
           'be willing to chat with me over there.' % (guide_firstname, username, country)

    msg1 = 'Hello %s my name is %s, I was wondering if you have a profile on Tourzan.com? I a have found it is easier for me to ' \
           'communicate and get to know my guide through their chat room and social profiles than on viator. ' \
           'Their booking solution is pretty awesome too and their fees are less. ' \
           'I was curious about what things you could show me in %s and if you would ' \
           'be willing to chat with me over there.' % (guide_firstname, username, country)

    msg2 = 'Hello %s my name is %s, are you on Tourzan.com? I was hoping we could chat about what local experiences you offer over there. ' \
           'I like their instant messaging solution better than Viators emailer and I would prefer a cashless booking ' \
           'process as i like to have all my trips planned and paid in advance.' % (guide_firstname, username)

    msg3 = 'Hello %s my name is %s I am planning a round the world trip and wanted to see if you are interested in ' \
           'showing me the local hot spots. Because of the complexities of coordinating experiences with so many guides ' \
           'I was hoping we could chat on Tourzan.com? Their instant messages are much nicer for fleshing out plans and ' \
           'I would prefer to pay in advance which they let me do. Let me know if you are interested in chatting about ' \
           'what local experiences you offer over in %s on Tourzan.com' % (guide_firstname, username, country)

    msg4 = 'Hello %s my name is %s I am planning a trip to %s and wanted to see if you could ' \
           'show me around the local haunts. its a bit difficult to coordinate on here and I was hoping you had a ' \
           'profile on Tourzan.com so that we could chat in real time and get to know if our interests match up ' \
           'before I go on my trip. Let me know if you interested.' % (guide_firstname, username, country)

    msg5 = 'Hello %s my name is %s I planned to visit %s and a few other countries in a few months.' \
           'Before I go, I wanted to plan with a few locals to show me around outside the tourist traps. ' \
           'Are you on Tourzan.com? It would make coordinating this trip easier for both of us and ' \
           'it would allow me to pay in advance I was hoping we could chat on Tourzan. ' \
           'If you are not on it you should check it out, its a pretty awesome service.' % (guide_firstname, username, country)

    messages = [msg0, msg1, msg2, msg3, msg4, msg5]
    return choice(messages)


def get_subject():
    subject = ['Tourzan.com', 'Are you on Tourzan?', 'Can we chat on Tourzan?', 'Hello', 'Trying to plan a trip']
    return choice(subject)

def message(driver, email, name, country, username):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "viator.db")
    conn = sqlite3.connect(db_path)

    driver.get(email)
    guide_firstname = name.split(' ')[0]
    guide_name = guide_firstname[0].upper()+guide_firstname[1:].lower()
    print(guide_name)
    print(guide_firstname)
    if guide_firstname[1] == '.' or guide_firstname[2] == '.':
        guide_name = name
    message = message_generator(guide_name, username, country)
    subject = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtSubject')
    subject.send_keys(get_subject())
    body = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtMessage')
    body.send_keys(message)
    driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_lnkSend').click()

    c = conn.cursor()
    c.execute("UPDATE viator_guides SET contacted = 1 WHERE name = (?) and url = (?) and country = (?)", (name, email, country))
    conn.commit()
    c.close()
    conn.close()


def mira(rows):
    proxies = get_proxy()
    for proxy in proxies:
        try:
            driver = get_driver(proxy)
            login(driver, 'paze@5-mail.info', 'tytyisbaebae21')  # todo: make usernames and passwords
            for row in rows:
                message(driver=driver, email=row[0], name=row[1], country=row[2], username='Mira')
                sleep(time_gen('small'))
            driver.quit()
            break
        except:
            driver.quit()
            continue


def mellisa(rows):
    proxies = get_proxy()
    for proxy in proxies:
        try:
            driver = get_driver(proxy)
            login(driver, 'reve@mailsearch.net', 'junoisbestdog1')  # todo: make usernames and passwords
            for row in rows:
                message(driver=driver, email=row[0], name=row[1], country=row[2], username='Mellisa')
                sleep(time_gen('small'))
            driver.quit()
            break
        except:
            driver.quit()
            continue


def angela(rows):
    proxies = get_proxy()
    for proxy in proxies:
        try:
            driver = get_driver(proxy)
            login(driver, 'nuxuzuc@5-mail.info', 'metalbronx42')  # todo: make usernames and passwords
            for row in rows:
                message(driver=driver, email=row[0], name=row[1], country=row[2], username='Angela')
                sleep(time_gen('small'))
            driver.quit()
            break
        except:
            driver.quit()
            continue


def diana(rows):
    proxies = get_proxy()
    for proxy in proxies:
        try:
            driver = get_driver(proxy)
            login(driver, 'sevihed@first-email.net', 'redrose21')  # todo: make usernames and passwords
            for row in rows:
                message(driver=driver, email=row[0], name=row[1], country=row[2], username='Diana')
                sleep(time_gen('small'))
            driver.quit()
            break
        except:
            driver.quit()
            continue


def justin(rows):
    proxies = get_proxy()
    for proxy in proxies:
        try:
            driver = get_driver(proxy)
            login(driver, 'royudilew@red-mail.info', 'redbloom1')  # todo: make usernames and passwords
            for row in rows:
                message(driver=driver, email=row[0], name=row[1], country=row[2], username='Justin')
                sleep(time_gen('small'))
            driver.quit()
            break
        except:
            driver.quit()
            continue


def nate(rows):
    proxies = get_proxy()
    for proxy in proxies:
        try:
            driver = get_driver(proxy)
            login(driver, 'tixahoy@5-mail.info', 'bloomfield123')  # todo: make usernames and passwords
            for row in rows:
                message(driver=driver, email=row[0], name=row[1], country=row[2], username='Nate')
                sleep(time_gen('small'))
            driver.quit()
            break
        except:
            driver.quit()
            continue


def login(driver, username, password):
    driver.get('https://tourguides.viator.com/Member/Login.aspx')
    driver.find_element_by_id('ctl00_plcMain_TextBox_Email').send_keys(username) #'contactus@tourzan.com')
    driver.find_element_by_id('ctl00_plcMain_TextBox_Password').send_keys(password) # 'blaze2000')
    driver.find_element_by_name('ctl00$plcMain$Button_Login').click()
    driver.implicitly_wait(5)


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "viator.db")
    conn = sqlite3.connect(db_path)
    users = [mira, mellisa, nate, justin, angela, diana]
    for user in users:
        c = conn.cursor()
        c.execute("SELECT url, name, country FROM viator_guides WHERE contacted = 0 ORDER BY random() LIMIT 8")
        user(c.fetchall())
        sleep(time_gen('large'))
        c.close()
    conn.close()


if __name__ == "__main__":
    main()
