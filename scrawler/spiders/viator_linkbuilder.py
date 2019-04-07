import os
import sqlite3
from sqlite3 import IntegrityError
from selenium.common import exceptions


def insert_into(email_list):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "viator.db")
    conn = sqlite3.connect(db_path)
    for item in email_list:
        for country, details in item.items():
            for name, link_list in details.items():
                for url in link_list:
                    try:
                        if '+' in country:
                            country = str(country).replace('+', ' ')
                        if 'Korea' in country:
                            country = "South Korea"
                        c = conn.cursor()
                        c.execute("insert into viator_guides (url, contacted, name, country) values (?, ?, ?, ?)",
                                  (url, 0, name, country))
                        conn.commit()
                        c.close()
                    except IntegrityError:
                        continue
    conn.close()


def get_links(driver, links, country):
    print(links)
    listings = {country: None}
    guides = dict()
    driver.get(links)

    listing = driver.find_elements_by_xpath("//*[contains(@id, Panel_ItemResultOuter)]/div[1]/div/div[2]/h2/a")
    for l in listing:
        name = l.text
        email_link = l.find_element_by_xpath('../../../../../div[2]/div/a').get_attribute('href')
        if name in guides.keys():
            guides[name].append(email_link)
        else:
            guides[name] = [email_link]
    listings[country] = guides
    return listings


def find_next(driver, links):
    driver.get(links)
    try:
        if driver.find_element_by_id(
                'ctl00_ctl00_plcMain_ContentPlaceHolder_Body_SearchResultsPager_Bottom_HyperLink_Next'):
            return driver.find_element_by_id(
                'ctl00_ctl00_plcMain_ContentPlaceHolder_Body_SearchResultsPager_Bottom_HyperLink_Next').get_attribute(
                'href')
    except exceptions.NoSuchElementException:
        return False


def get_emails(driver):
    uri = {
        # 'United+States+of+America': {'Washington': ['Seattle'], 'New+York': ['New+York'], 'Nevada':['Las+Vegas'],
        #                                 'California': ['Los+Angeles', 'San+Francisco', 'Napa'], 'Illinois': ['Chicago'],
        #                                 'Oregon': ['Portland'], 'Hawaii': ['Honolulu'], 'Louisiana': ['New+Orleans']},
        # 'Canada': {''},
        # 'Mexico': {'Mexico+City': ['Mexico+City'], 'Cancun': ['Cancun'], 'Mazatlan': ['Mazatlan']},

        # 'Chile': {'Santiago': 'Santiago'},
        # 'Peru': {'Lima': ['Lima']},
        # 'Columbia': {''},
        # 'Argentina': {''},
        # 'Brazil': {''},
        # 'Bolivia': {''},
        # 'Nicaragua': {''},
        # 'Costa+Rica': {''},
        # 'Puerto+Rico': {''},
        # 'Ecuador': {''},

        # 'Jamaica': {''},
        # 'Barbados': {''},
        # 'Bahamas': {''},

        # 'Austria': {''},
        # 'Norway': {''},
        # 'Sweden': {''},
        # 'Finland': {''},
        # 'Croatia': {''},
        # 'Poland': {''},
        # 'Czech+Republic': {''},
        # 'Laos': {''},
        # 'Mongolia': {''},

        # 'Russia': {''},
        # 'Germany': {''},
        # 'Ukraine': {''},
        # 'Iceland': {''},
        # 'South+Africa': {''},
        # 'Switzerland': {''},
        # 'Portugal': {},
        # 'United+Kingdom': {'England': ['London', 'Bath']},
        # 'France': {'Ile-de-France': ['Paris', 'Versailles']},
        # 'Hungary': {},
        # 'Italy': {'Rome': ['Rome'], 'Venice': ['Venice']},
        # 'Greece': {'Athens': ['Athens']},
        # 'Serbia': {''},
        # 'Montenegro': {''},
        # 'Spain': {''},
        # 'Turkey': {'Istanbul': ['Istanbul']},

        # 'Madagascar': {''},
        # 'Zambia': {''},
        # 'Kenya': {''},
        # 'Tanzania': {''},
        # 'Uganda': {''},
        # 'Morocco': {''},
        # 'United+Arab+Emirates': {'Dubai': ['Dubai']},
        # 'Egypt': {'Cairo': ['Cairo'], 'Luxor': ['Luxor']},

        # 'Thailand': {'Bangkok': ['Bangkok'], 'Phuket': ['Phuket'], 'Chiang+Mai': ['Chiang+Mai'],
        #              'Chon+Buri': ['Pattaya'],
        #              'Phra+Nakhon+Si+Ayutthaya': ['Ayutthaya']},
        # 'Singapore': {''},
        # 'Malaysia': {'Kuala+Lumpur': ['Kuala+Lumpur']},
        # 'Japan': {'Tokyo': ['Tokyo'], 'Kanagawa': ['Kamakura'], 'Osaka': ['Osaka']},
        # 'India': {'New+Dheli': ['New+Dheli']},  # TODO 800+ guides
        # 'Korea+(South)': {''},
        # 'China': {''},
        # 'Nepal': {''},
        # 'Myanmar': {''},
        # 'Sri+Lanka': {''},
        # 'Vietnam': {''},
        # 'Cambodia': {''},
        # 'Indonesia': {''},
        # 'Taiwan': {''},

        # 'Australia': {''},
        # 'New+Zealand': {''},
    }

    collection = []
    for country in uri.keys():
        url = 'https://tourguides.viator.com/Listing.aspx?Country=%s' % country
        collection.append([url, country])

    email_url = []
    for u in collection:
        email_url = []  # remove after initial run
        email_url.append(get_links(driver, u[0], u[1]))
        link = find_next(driver, u[0])
        while link != False:
            email_url.append(get_links(driver, str(link), u[1]))
            link = find_next(driver, link)
        insert_into(email_url)
    return email_url


# uncomment to build new links
# email_list = get_emails(driver)
# insert_into(email_list)