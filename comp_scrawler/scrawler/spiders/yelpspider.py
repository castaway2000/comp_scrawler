import time
from selenium import webdriver
from selenium.common import exceptions


def get_links(driver, links):
    profile_url = []
    driver.get(links)
    href = driver.find_elements_by_xpath("//a[contains(@class, 'biz-name js-analytics-click')]")
    for h in href:
        profile_url.append(h.get_attribute('href'))
    return profile_url


def find_next(driver, links):
    driver.get(links)
    try:
        if driver.find_element_by_xpath(
                '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[11]/a/span[1]'):
            return driver.find_element_by_xpath(
                '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[11]/a')\
                .get_attribute('href')
    except exceptions.NoSuchElementException:
        return False


def main():
    uri = {'United+States+of+America': {'WA': ['Seattle'], 'NY': ['New+York'], 'NV':['Las+Vegas'],
                                        'CA': ['Los+Angeles', 'San+Francisco', 'Napa'], 'IL': ['Chicago'],
                                        'OR': ['Portland'], 'HI': ['Honolulu'], 'LA': ['New+Orleans']},
           # 'Thailand': {'Bangkok': ['Bangkok'], 'Phuket': ['Phuket'], 'Chiang+Mai': ['Chiang+Mai'], 'Chon+Buri': ['Pattaya'],
           #              'Phra+Nakhon+Si+Ayutthaya': ['Ayutthaya']},
           'United+Kingdom': {'England': ['London', 'Bath']},
           'France': {'Ile-de-France': ['Paris', 'Versailles']},
           # 'United+Arab+Emirates': {'Dubai': ['Dubai']},
           'Singapore': {'Singapore': ['Singapore']},
           'Malaysia':{'Kuala+Lumpur': ['Kuala+Lumpur']},
           'Turkey': {'Istanbul': ['Istanbul']},
           'Japan': {'Tokyo': ['Tokyo'], 'Kamakura': ['Kamakura'], 'Osaka': ['Osaka'], 'Nara': ['Nara']},
           # 'Korea': {'Seoul': ['Seoul']}
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
        for region in uri[country].keys():
            for city in uri[country][region]:
                url = 'https://www.yelp.com/search?find_desc=Private+Tour+Guide&find_loc={0},+{1}'.format(city, country)
                collection.append(url)
    profile_url = []
    for u in collection:
        profile_url.extend(get_links(driver, u))
        link = find_next(driver, u)
        while link != False:
            profile_url.extend(get_links(driver, str(link)))
            link = find_next(driver, link)
    print len(profile_url)
    tally = {'pass': 0, 'fail': 0}
    #pass, fail
    for profile in profile_url:
        print profile
        driver.get(profile)
        try:
            try:
                msg_btn = driver.find_element_by_class_name('js-message-biz')
            except exceptions.UnexpectedAlertPresentException:
                driver.switch_to.alert.accept()
                msg_btn = driver.find_element_by_class_name('js-message-biz')
            msg_btn.click()
            time.sleep(1)
            textarea = driver.find_element_by_name('message_to_business')
            textarea.send_keys('messege')
            email_field = driver.find_element_by_class_name('js-email-input')
            email_field.send_keys('contactus@tourzan.com')
            name_field = driver.find_element_by_class_name('js-first-name-input')
            name_field.send_keys('Adam Szablya')
            submit = driver.find_element_by_xpath("//button[contains(@class, 'ybtn ybtn--primary ybtn--small js-message-the-business-submit')]")
            # submit.click()
            tally['pass'] += 1
        except exceptions.NoSuchElementException:
            tally['fail'] += 1
    print tally

if __name__ == "__main__":
    main()