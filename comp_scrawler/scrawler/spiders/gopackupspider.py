import time
from selenium import webdriver
from selenium.common import exceptions


def get_guide_profiles(driver, url, total_listings):
    collection = []
    base_url = url
    for n in range(1, total_listings):
        base_url = base_url + '?page={}'.format(n)
        print(base_url)
        driver.get(base_url)
        userpages = driver.find_elements_by_xpath('//a[contains(@class, "ui image")]')
        for i in userpages:
            collection.append(i.get_attribute('href'))
        base_url = url
        # if n == 1:
        #     break
    return collection


def contact_guide(driver, url_list):
    for i in url_list:
        driver.get(i)
        driver.find_element_by_id('guide-contact-button').click()
        print(driver.current_url)
        #
        # msg = 'Hello, my name is Adam. I am reaching out to you because of your passion for showing tourists around. ' \
        #       'I hope you are doing well, If you have a moment I have a proposal. ' \
        #       'Last year I started tourzan.com with the idea that a city is best seen with a local. ' \
        #       'Its goal is to add value to what you are already doing, my goal is to help increase customers for you ' \
        #       'My respect for businesses and individual entrepreneurial types like yourself is great.' \
        #       'I would be honored if you would give my webservice a chance and a look over. ' \
        #       'let me know what you think. im not here to steal you from tours by locals. ' \
        #       'I am here to an additional place to list and increase your presence on the internet. \n\n' \
        #       'Thank you for your time \n' \
        #       'Adam Szablya'


def login_driver(driver):
    login = 'https://gopackup.com/login'
    driver.get(login)
    driver.find_element_by_name('email').send_keys('contactus@tourzan.com')
    driver.find_element_by_name('password').send_keys('')
    #
    # driver.execute_script("document.getElementsByName('email')[0].setAttribute('value', 'contactus@tourzan.com');")
    # driver.execute_script("document.getElementsByName('password')[0].setAttribute('value', '');")
    driver.find_element_by_id('go-btn-secondary').click()


def main():
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_argument('window-size=800x841')
    # options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    login_driver(driver)
    url = 'https://gopackup.com/guides/list'
    driver.get(url)
    total_pages = int(str(driver.find_element_by_link_text('>>').get_attribute("href"))[-3:])
    userpages = get_guide_profiles(driver, url, total_pages)
    contact_guide(driver, userpages)




if __name__ == "__main__":
    main()