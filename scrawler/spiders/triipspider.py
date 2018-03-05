# coding: utf-8

from selenium import webdriver
from selenium.common import exceptions
import time


def is_previously_messaged(profile, writer=False):
    with open('contacted_on_triip.txt', 'rw') as doc:
        if profile in doc.readlines():
            return False
        if writer:
            doc.write(str(profile))
    return True


def get_links(driver, link):
    """
    This is the part where we get the tourguides listings as links
    :param driver: Selenium Webdriver object
    :param link: unicode url
    :return: False if no links or list of links
    """
    listing = []
    driver.get(link)
    try:
        href = driver.find_elements_by_xpath("//*[@class='tour-thumb imgix-fluid']")
        for h in href:
            listing.append(h.get_attribute('href'))
        return listing
    except Exception:
        return False


def message(driver, listing):
    msg = 'Hello, my name is Adam. I am reaching out to you because of your passion for showing tourists around. ' \
          'I hope you are doing well, If you have a moment I have a proposal. ' \
          'Last year I started tourzan.com with the idea that a city is best seen with a local. ' \
          'Its goal is to add value to what you are already doing, my goal is to help increase customers for you ' \
          'My respect for businesses and individual entrepreneurial types like yourself is great.' \
          'I would be honored if you would give my webservice a chance and a look over. ' \
          'let me know what you think. im not here to steal you from Triip. ' \
          'I am here to an additional place to list and increase your presence on the internet. \n\n' \
          'Thank you for your time \n' \
          'Adam Szablya'
    driver.get(listing)
    msg_btn = driver.find_element_by_xpath("//a[contains(@class,'contact-creator-full-button hidden-xs hidden-sm visible-md-block visible-lg-block js-top-message-button')]")
    msg_btn.click()
    body = driver.find_element_by_xpath("//textarea[contains(@class, 'input_required required_field_empty js-message-input')]")
    body.send_keys(msg)
    button = driver.find_element_by_id('msg_login_btn')
    # button.click()
    is_previously_messaged(listing, writer=True)


def customers(driver, listing_url):
    """
    Here we compile a list of unique users based on the large list of links we compiled earlier on.
    :param driver: Selenium webdriver object
    :param listing_url: list of unicode url's
    :return: list of unique customers
    """
    users = set()
    # TODO: uncomment this when creating a new list. fair warning it takes about 12-24 hours to complete
    # for listing in listing_url:
    #     timeout = False
    #     while True:
    #         driver.get(listing)
    #         if timeout:
    #             driver.set_page_load_timeout(10)
    #         try:
    #             name = driver.find_element_by_xpath("//a[contains(@class,'bold avatar lg')]")
    #             link = name.get_attribute('href')
    #             if link not in users:
    #                 # message(driver.get(listing))
    #                 users.append(link)
    #                 break
    #             else:
    #                 break
    #         except exceptions.NoSuchElementException:
    #             continue
    #         except exceptions.TimeoutException as e:
    #             timeout = True
    #             continue
    '''
    # this is for re-writing data from duplicates to unique values
        print link
    u = open('triipscrape.txt', 'rw')
    for item in u.readlines():
        users.add(item.rstrip('\n'))
    print len(users)
    print users
    '''
    f = open('triipusers.txt', 'w')
    for item in users:
        f.write("%s\n" % item)
    return users


def market(driver, users):
    """
    gets the first listing of each unique user and messages the user.
    :param driver: 
    :param users: 
    :return: 
    """
    for user in users:
        if is_previously_messaged(user):
            driver.get(user)
            listing = driver.find_element_by_class_name("tour-thumb").get_attribute('href')
            message(driver, listing)


def main():
    """
    crawls over Triip.com for all listings and unique users.
    commented out code is no longer needed once the initial scrape is completed.
    :return: None
    """
    url = 'https://www.triip.me/search/'
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    # TODO: uncomment this when creating a new list. fair warning it takes about an hour to complete
    # page = 1
    # listing_url = []
    # while True:
    #     link = url+'?page={}'.format(page)
    #     listings = get_links(driver, str(link))
    #     if len(listings) > 0:
    #         print link
    #         listing_url.extend(listings)
    #         page += 1
    #     if page > 436:
    #         break
    # f = open('triiplistings.txt', 'w')
    # for item in listing_url:
    #     f.write("%s\n" % item)
    # with open('triiplistings.txt', 'r') as f:
    #     listing_url = f.readlines()
    # customers(driver, listing_url)
    with open('triipusers.txt', 'r') as f:
        user_url = f.readlines
    market(driver, user_url)


if __name__ == "__main__":
    main()