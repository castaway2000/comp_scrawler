import re
import os
import optparse
from selenium import webdriver


def main():
    uri = ['Seattle-Tour-Guides', 'New-York-City-Tour-Guides', 'Los-Angeles-Tour-Guides', 'Las-Vegas-Tour-Guides',
           'San-Francisco-Tour-Guides', 'Chicago-Tour-Guides', 'Portland-Tour-Guides', 'Honolulu-Tour-Guides',
           'NEw-Orleans-Tour-Guides',
           'Bangkok-Tour-Guides', 'Phuket-Tour-Guides', 'Chiang-Mai-Tour-Guides', 'Paris-Tour-Guides',
           'Dubai-Tour-Guides', 'Kuala-Lumpur-Tour-Guides', 'Tokyo-Tour-Guides', 'Istanbul-Tour-Guides',
           'Yokohama-Tour-Guides', 'Osaka-Tour-Guides', 'Kyoto-Tour-Guides']
    #TODO: add napal, myanmar, sri lanka, columbia, serbia, madagascar, montenegro, canada,
    #TODO: mongolia, south africa, zambia, egypt to the list.

    collection = []

    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    email_url = []
    for val in uri:
        url = 'https://www.toursbylocals.com/{}'.format(val)
        driver.set_page_load_timeout(10)
        driver.get(str(url))
        link = driver.find_elements_by_xpath("//a[contains(@href,'messageGuide')]")
        for h in link:
            email_url.append(h.get_attribute('href'))
    for e in email_url:
        print e
    print len(email_url)
        # driver.get(e)
        # firstname = driver.find_element_by_name('37.1.23.1.1')
        # firstname.send_keys('Robert')
        # lastname = driver.find_element_by_name('37.1.23.1.1')
        # lastname.send_keys('Johnson')
        # email = driver.find_element_by_name('37.1.23.1.5')
        # email.send_keys('contactus@tourzan.com')
        # confirm_email = driver.find_element_by_name('37.1.23.1.7')
        # confirm_email.send_keys('contactus@tourzan.com')
        # textarea = driver.find_element_by_name('37.1.23.5')
        # textarea.send_keys('something goes here')
        # button = driver.find_element_by_name('37.1.23.21')
        # button.click()

if __name__ == "__main__":
    main()