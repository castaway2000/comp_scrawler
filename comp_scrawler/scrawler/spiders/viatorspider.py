import re
import os
import optparse
from selenium import webdriver
from selenium.common import exceptions


def is_previously_messaged(profile, writer=False):
    doc = open('contacted_on_yelp.txt', 'r+')
    if profile in doc.readlines():
        return False
    if writer:
        doc.write('%s\n' % profile)
    return True


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
           'Hungary': {},
           'United+Arab+Emirates': {'Dubai': ['Dubai']},
           'Singapore': {'':['']},
           'Malaysia':{'Kuala+Lumpur': ['Kuala+Lumpur']},
           'Turkey': {'Istanbul': ['Istanbul']},
           'Japan': {'Tokyo': ['Tokyo'], 'Kanagawa': ['Kamakura'], 'Osaka': ['Osaka']},

           'Chile': {'Santiago': 'Santiago'},
           'Peru': {'Lima': ['Lima']},
           'Mexico': {'Mexico+City': ['Mexico+City'], 'Cancun': ['Cancun'], 'Mazatlan': ['Mazatlan']},
           'India': {'New+Dheli': ['New+Dheli']},
           'Italy': {'Rome': ['Rome'], 'Venice': ['Venice']},
           'Greece': {'Athens': ['Athens']},
           'Egypt': {'Cairo': ['Cairo'], 'Luxor': ['Luxor']},
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
        # for key in uri[country].keys():
        #     for val in uri[country][key]:
        url = 'https://tourguides.viator.com/Listing.aspx?Country=%s' % country
        collection.append(url)
    email_url = []
    for u in collection:
        email_url.extend(get_links(driver, u))
        link = find_next(driver, u)
        while link != False:
            email_url.extend(get_links(driver, str(link)))
            link = find_next(driver, link)
    print len(email_url)
    message = 'Hello my name is Adam, I am reaching out to you because ' \
              'I started a business called tourzan.com to let tourists more easily find local guides and tour ' \
              'operators. As an entrepreneur and a doer I feel confident in inviting you to be a part of ' \
              'an exclusive group of tour operators and individuals to on-board during the launch of my company ' \
              'It is my goal to get you in front of as many people as possible.' \
              'I was hoping you might take two minutes of your time to give tourzan.com a try. ' \
              'See what you could gain and how it might grow your customer base and give you a competitive edge. ' \
              'It costs nothing to sign up or list yourself and tour packages. ' \
              'Tourzan.com makes money when you make money and as a result i do the heavy lifting for you. ' \
              'At the very least, as a startup and business to business, ' \
              'I would appreciate your feedback all the same to help make my company the best it can be. \n\n' \
              'Thank you for your time in checking out tourzan.com I look forward to hearing from you. \n' \
              '-Adam Szablya'
    for email in email_url:
        if is_previously_messaged(email):
            driver.get(email)
            subject = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtSubject')
            subject.send_keys('Tourzan.com')
            body = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtMessage')
            body.send_keys(message)
            button = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_lnkSend')
            # button.click()
            is_previously_messaged(email, writer=True)


if __name__ == "__main__":
    main()