import time
from selenium import webdriver
from selenium.common import exceptions


def is_previously_messaged(profile, writer=False):
    doc = open('contacted_on_yelp.txt', 'r+')
    if str(profile) in doc.read():
        print 'line found in file, returning False'
        return False
    if writer:
        doc.write('%s\n' % profile)
    return True


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
                '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[10]/a'):
            print 'True'
            return driver.find_element_by_xpath(
                '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[10]/a')\
                .get_attribute('href')
    except exceptions.NoSuchElementException:
        print 'NOPE!'
        return False


def list_of_guides():
    out = []
    guides = open('contacted_on_yelp1.txt', 'r')
    for g in guides:
        out.append(g.strip('\n'))
    return out

def main():
    uri = {'United+States+of+America': {'WA': ['Seattle'], 'NY': ['New+York'], 'NV':['Las+Vegas'] ,
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
           # TODO: add more ares below this line till target reaches 1000
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
    # options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    for country in uri.keys():
        for region in uri[country].keys():
            for city in uri[country][region]:
                url = 'https://www.yelp.com/search?find_desc=Tour+Guide&find_loc={0},+{1}'.format(city, country)
                # url = 'https://www.yelp.com/search?find_desc=Private+Tour+Guide&find_loc={0},+{1}'.format(city, country)
                collection.append(url)
    profile_url = list_of_guides()  # []
    # for u in collection:
    #     profile_url.extend(get_links(driver, u))
    #     link = find_next(driver, u)
    #     while link != False:
    #         profile_url.extend(get_links(driver, str(link)))
    #         link = find_next(driver, link)
    print len(profile_url)
    tally = {'pass': 0, 'fail': 0}
    #pass, fail
    for profile in profile_url:
        while True:  # fo use with compiled list only.
            if is_previously_messaged(profile) != False:
                try:
                    try:
                        driver.get(profile)
                        driver.implicitly_wait(15)
                        btn = driver.execute_script('document.getElementsByClassName("js-message-biz").length')
                        if btn == 0:
                            # continue
                            break  # while loop only
                        else:
                            print 'clicking biz button at:'
                            print driver.current_url
                            driver.execute_script('document.getElementsByClassName("js-message-biz")[0].click()')
                    except exceptions.UnexpectedAlertPresentException:
                        driver.switch_to.alert.dismiss()
                        print 'alert happened, fixed it. inner try'
                        continue
                        # print driver.current_url
                        # driver.execute_script('document.getElementsByClassName("js-message-biz")[0].click()')
                    except exceptions.WebDriverException as e:
                        if 'Element is not clickable at point' in e.message:
                            print e.message
                            print 'element not clickable at %s' % driver.current_url
                            driver.implicitly_wait(10)
                            driver.execute_script('document.getElementsByClassName("js-message-biz")[0].click()')
                        elif "Cannot read property 'click' of undefined" in e.message:
                            continue
                        else:
                            print e
                            print 'at %s' % driver.current_url
                            print 'continuing'
                            continue
                    message = 'Hello my name is Adam, I came accross your listing on yelp wanted to reach out to you to touch base. ' \
                              'I am starting a business called tourzan.com to let tourists easily find tour operators in the city they are visiting. ' \
                              'As an entrepreneur and a doer I feel confident in inviting you to be a part of ' \
                              'an exclusive group of individuals and businesses to on-board during the launch of my company. ' \
                              'It is entirely Free to list your services on tourzan.com as well.' \
                              'It is my goal to get you in front of as many people as possible to increase your business.' \
                              'I was hoping you might take two minutes of your time to give tourzan.com a try. ' \
                              'See what you could gain from it and how it might grow your business and give you a competitive edge. ' \
                              'Its completely free to sign up, list yourself, business and tours. ' \
                              'Tourzan.com makes money when you make money and as a result its my job to do the heavy lifting for you. ' \
                              'At the very least, as a startup and business to business, I would appreciate your ' \
                              'feedback all the same to help make this a success. \n\n' \
                              'Thank you for your time in checking out tourzan.com I look forward to hearing from you. \n' \
                              '-Adam Szablya'
                    time.sleep(1)
                    textarea = driver.find_element_by_name('message_to_business')
                    textarea.send_keys(message)
                    print 'message written'
                    email_field = driver.find_element_by_class_name('js-email-input')
                    email_field.send_keys('contactus@tourzan.com')
                    print 'email written'
                    name_field = driver.find_element_by_class_name('js-first-name-input')
                    name_field.send_keys('Adam Szablya')
                    print 'name written'
                    driver.execute_script('document.getElementsByClassName("ybtn ybtn--primary arrange_unit js-message-the-business-submit u-space-r3")[0].click()')
                    print 'AAAAND Sent'
                    tally['pass'] += 1
                    is_previously_messaged(profile, writer=True)
                except exceptions.NoSuchElementException:
                    print 'no such element, plz check'
                    print profile
                    tally['fail'] += 1
                    break
            else:
                break
            print tally

if __name__ == "__main__":
    main()
    # list_of_guides()