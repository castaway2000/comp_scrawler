from selenium import webdriver


def is_previously_messaged(profile, writer=False):
    with open('contacted_on_toursbylocals.txt', 'rw') as doc:
        if profile in doc.readlines():
            return False
        if writer:
            doc.write(str(profile))
    return True


def main():
    uri = ['Seattle-Tour-Guides', 'New-York-City-Tour-Guides', 'Los-Angeles-Tour-Guides', 'Las-Vegas-Tour-Guides',
           'San-Francisco-Tour-Guides', 'Chicago-Tour-Guides', 'Portland-Tour-Guides', 'Honolulu-Tour-Guides',
           'NEw-Orleans-Tour-Guides',
           'Bangkok-Tour-Guides', 'Phuket-Tour-Guides', 'Chiang-Mai-Tour-Guides', 'Paris-Tour-Guides',
           'Dubai-Tour-Guides', 'Kuala-Lumpur-Tour-Guides', 'Tokyo-Tour-Guides', 'Istanbul-Tour-Guides',
           'Yokohama-Tour-Guides', 'Osaka-Tour-Guides', 'Kyoto-Tour-Guides']
    #TODO: add napal, myanmar, sri lanka, columbia, serbia, madagascar, montenegro, canada,
    #TODO: mongolia, south africa, zambia, egypt to the list.

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

    msg = 'Hello, my name is Adam. I am reaching out to you because of your passion for showing tourists around. ' \
          'I hope you are doing well, If you have a moment I have a proposal. ' \
          'Last year I started tourzan.com with the idea that a city is best seen with a local. ' \
          'Its goal is to add value to what you are already doing, my goal is to help increase customers for you ' \
          'My respect for businesses and individual entrepreneurial types like yourself is great.' \
          'I would be honored if you would give my webservice a chance and a look over. ' \
          'let me know what you think. im not here to steal you from tours by locals. ' \
          'I am here to an additional place to list and increase your presence on the internet. \n\n' \
          'Thank you for your time \n' \
          'Adam Szablya'
    for e in email_url:
        if is_previously_messaged(e):
            print e
            driver.get(e)
            firstname = driver.find_element_by_name('37.1.23.1.1')
            firstname.send_keys('Adam')
            lastname = driver.find_element_by_name('37.1.23.1.3')
            lastname.send_keys('Szablya')
            email = driver.find_element_by_name('37.1.23.1.5')
            email.send_keys('contactus@tourzan.com')
            confirm_email = driver.find_element_by_name('37.1.23.1.7')
            confirm_email.send_keys('contactus@tourzan.com')
            textarea = driver.find_element_by_name('37.1.23.5')
            textarea.send_keys(msg)
            button = driver.find_element_by_name('37.1.23.21')
            # button.click()
            is_previously_messaged(e, writer=True)

if __name__ == "__main__":
    main()