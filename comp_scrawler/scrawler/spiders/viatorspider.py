import re
import os
import optparse
from selenium import webdriver
from selenium.common import exceptions


def is_previously_messaged(profile, writer=False):

    doc = open('contacted_on_viator.txt', 'r+')
    if profile in doc.readlines():
        print 'line found in file, returning False'
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
           'Canada': {''},
           'Jamaica': {''},
           'Barbados': {''},
           'Bahamas': {''},

           'United+Kingdom': {'England': ['London', 'Bath']},
           'France': {'Ile-de-France': ['Paris', 'Versailles']},
           'Hungary': {},
           'Italy': {'Rome': ['Rome'], 'Venice': ['Venice']},
           'Greece': {'Athens': ['Athens']},
           'Serbia': {''},
           'Montenegro': {''},
           'Spain': {''},

           'Madagascar': {''},
           'United+Arab+Emirates': {'Dubai': ['Dubai']},
           'Egypt': {'Cairo': ['Cairo'], 'Luxor': ['Luxor']},

           'Thailand': {'Bangkok': ['Bangkok'], 'Phuket': ['Phuket'], 'Chiang+Mai': ['Chiang+Mai'],
                        'Chon+Buri': ['Pattaya'],
                        'Phra+Nakhon+Si+Ayutthaya': ['Ayutthaya']},
           'Singapore': {'':['']},
           'Malaysia':{'Kuala+Lumpur': ['Kuala+Lumpur']},
           'Turkey': {'Istanbul': ['Istanbul']},
           'Japan': {'Tokyo': ['Tokyo'], 'Kanagawa': ['Kamakura'], 'Osaka': ['Osaka']},
           'India': {'New+Dheli': ['New+Dheli']},
           'Korea': {'Seoul': ['Seoul']},
           'China': {''},
           'Nepal': {''},
           'Myanmar': {''},
           'Sri+Lanka': {''},
           'Vietnam': {''},
           'Cambodia': {''},
           'Indonesia': {''},

           'Australia': {''},
           'New+Zealand': {''},

           'Chile': {'Santiago': 'Santiago'},
           'Peru': {'Lima': ['Lima']},
           'Mexico': {'Mexico+City': ['Mexico+City'], 'Cancun': ['Cancun'], 'Mazatlan': ['Mazatlan']},
           'Columbia': {''},
           'Argentina': {''},
           'Brazil': {''},
           'Bolivia': {''},
           'Nicaragua': {''},
           'Costa+Rica': {''},
           'Puerto+Rico': {''}
           }

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
    message = 'Hello my name is Adam, I am reaching out to invite you to help shape a new tour guide service.' \
              'I started a business called tourzan.com to let tourists more easily find locals to be their guide. ' \
              'I feel confident in inviting you to be a part of an exclusive group of tour operators and individuals ' \
              'to on-board during the launch of my company I was hoping you might take two minutes of your time ' \
              'to give tourzan.com a try. I would love for you join me in shaping it. ' \
              'Come see what you could gain and how it might grow your customer base and give you a competitive edge. ' \
              'It costs nothing to sign up or list yourself or your tour packages. ' \
              'There is no direct cost to you but your time. We cover your liability as an independent guide as well' \
              'I do the heavy lifting to help market you. At the very least, from industry professional to startup ' \
              'I would appreciate your feedback all the same to help make my company be the best it can be. ' \
              'Feel free to reach out to me with any questions or concerns you may have.\n\n' \
              'Thank you for your time and consideration. I look forward to hearing from you over at tourzan.com. \n' \
              '-Adam Szablya'

    driver.get('https://tourguides.viator.com/Member/Login.aspx')
    driver.find_element_by_id('ctl00_plcMain_TextBox_Email').send_keys('contactus@tourzan.com')
    driver.find_element_by_id('ctl00_plcMain_TextBox_Password').send_keys('blaze2000')
    driver.find_element_by_name('ctl00$plcMain$Button_Login').click()
    driver.implicitly_wait(5)
    for email in email_url:
        print email
        if is_previously_messaged(email):
            driver.get(email)
            subject = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtSubject')
            subject.send_keys('Tourzan.com')
            body = driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_txtMessage')
            body.send_keys(message)
            driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_CheckBox_ReUseText').click()
            #driver.find_element_by_id('ctl00_ctl00_plcMain_ContentPlaceHolder_Body_lnkSend').click()
            is_previously_messaged(email, writer=True)


if __name__ == "__main__":
    main()