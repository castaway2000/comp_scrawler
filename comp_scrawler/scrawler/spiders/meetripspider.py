import re
import os
import optparse
from selenium import webdriver
from selenium.common import exceptions


def get_links(driver, links):
    email_url = []
    driver.get(links)
    href = driver.find_elements_by_partial_link_text('Email')
    for h in href:
        email_url.append(h.get_attribute('href'))
    return email_url


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


def main():
    uri = {'United+States+of+America': {'Washington': ['Seattle'], 'New+York': ['New+York'], 'Nevada':['Las+Vegas'],
                                        'California': ['Los+Angeles', 'San+Francisco', 'Napa'], 'Illinois': ['Chicago'],
                                        'Oregon': ['Portland'], 'Hawaii': ['Honolulu'], 'Louisiana': ['New+Orleans']},
           'Thailand': {'Bangkok': ['Bangkok'], 'Phuket': ['Phuket'], 'Chiang+Mai': ['Chiang+Mai'], 'Chon+Buri': ['Pattaya'],
                        'Phra+Nakhon+Si+Ayutthaya': ['Ayutthaya']},
           'United+Kingdom': {'England': ['London', 'Bath']},
           'France': {'Ile-de-France': ['Paris', 'Versailles']},
           'United+Arab+Emirates': {'Dubai': ['Dubai']},
           'Singapore': {'':['']},
           'Malaysia':{'Kuala+Lumpur': ['Kuala+Lumpur']},
           'Turkey': {'Istanbul': ['Istanbul']},
           'Japan': {'Tokyo': ['Tokyo'], 'Kanagawa': ['Kamakura'], 'Osaka': ['Osaka']},
           'Korea': {'Seoul': ['Seoul']}
           }
    #TODO: add napal, myanmar, sri lanka, columbia, serbia, madagascar, montenegro, canada,
    #TODO: mongolia, south africa, zambia, egypt to the list.
    #TODO: login https://tourguides.viator.com
    collection = []

    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    for country in uri.keys():
        for key in uri[country].keys():
            for val in uri[country][key]:
                url = 'https://tourguides.viator.com/Listing.aspx?Country=%s&Region=%s&City=%s' % (country, key, val)
                collection.append(url)
    email_url = []
    for u in collection:
        email_url.extend(get_links(driver, u))
        link = find_next(driver, u)
        while link != False:
            email_url.extend(get_links(driver, str(link)))
            link = find_next(driver, link)
    msg = 'Hello, my name is Adam. I am reaching out to you because of your passion for showing tourists around. ' \
          'I hope you are doing well, If you have a moment I have a proposal. ' \
          'Last year I started tourzan.com with the idea that a city is best seen with a local. ' \
          'Its goal is to add value to what you are already doing, my goal is to help increase customers for you ' \
          'My respect for businesses and individual entrepreneurial types like yourself is great.' \
          'I would be honored if you would give my webservice a chance and a look over. ' \
          'let me know what you think. im not here to steal you from meetrip. ' \
          'I am here to an additional place to list and increase your presence on the internet. \n\n' \
          'Thank you for your time \n' \
          'Adam Szablya'
    for email in email_url:
        driver.get(email)
        #TODO: match this with the right elements
        # subject = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtSubject')
        # subject.send_keys('Tourzan.com')
        # body = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtMessage')
        # body.send_keys(msg)
        # button = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_lnkSend')
        # button.click()


if __name__ == "__main__":
    main()