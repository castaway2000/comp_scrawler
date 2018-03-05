import time
import pytesseract
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver


def handle_captia(image):
    print(image.get_attribute('src'))
    req = requests.get(image.get_attribute('src'))
    try:
        img = Image.open(BytesIO(req.content))
        text = pytesseract.image_to_string(img).encode('utf-8').replace(' ', '1')
        print("captia: %s" % text)
        return text
    except IOError:
        print('ioerror')
        return None


def refresh(driver):
    driver.refresh()
    driver.implicitly_wait(30)
    driver.find_elements_by_class_name('ad')


def send_msg(driver, url, i):
    msg = "Hello my name is Adam Szablya. I started a company called tourzan.com which lets locals, tour guides and " \
          "tour companies make side cash through the gig market. I am reaching out to you to invite you to try my " \
          "webservice. Unlike Shiroube it costs nothing to list yourself or your services. We make money when you do " \
          "through transaction fees. So there is never a membership or payment you need to make to us. \n \nRegarding " \
          "tourzan.com Here is some benefits of the platform. \n- Free to use and get started. \n- Fully featured " \
          "dashboard for creating, managing, maintaining relationships and bookings\n-LGBTQ Friendly\n-Disability " \
          "friendly, encouraging a tailored approach\n-Listens to and supports its users feedback\n-Each free guide " \
          "account comes with direct marketing for each guide profile created.\n-Fee per order service so there is no " \
          "membership or expenses needing to be paid\n-Directed email alerts for a fix and forget style of user." \
          "\n-Complimentary mobile app for both guides and tourists is in the works\n-Website is optimized for mobile" \
          " users\n-Personalized guide profiles\n-Social experiences to share on twitter and facebook.\n-Industry leading" \
          " trustworthiness and identity verification backed by onfido.com and payment rails.\n-All guides are screened " \
          "through watchlists.\n-Highly filterable search engine.\n-2 million dollar insurance policy for liability and " \
          "cases where things were not as expected and someone got hurt. Underwritten and guaranteed globally by " \
          "Gryphon Underwriting. Only applicable to bookings made through tourzan.\n-Integration services for r" \
          "e-listing tourzan's offerings in other web-services.\n-100% mitigation guarantee. We will refund customers " \
          "in a timely manner if things are not up to our localized acceptable standards.\n-We hold high standards " \
          "across our guides any guide who falls short of standards gets removed from the service.\n-Reasonable and " \
          "localized pricing.\n-We pay out in most every currency to most every country in the planet\n-We are " \
          "improving the website every day.\n-We are working to increase speed in regions outside of the USA.\n-We are " \
          "PCI compliant through braintree payments, a paypal company. As a result we never store credit card info in " \
          "our databases.\n-Supports local economies\n-Translated into 7 highly predominant languages by locals living " \
          "in that region for better use by customers globally.\n-While others charge as much as 40% fees. We deduct as l" \
          "ittle as 13% which is the lowest I know of in the industry.\n\nIf you know anyone or any organizations who " \
          "would be interested in listing with us please send them our way. We hope to hear back from you soon. Let us " \
          "know if there is any social media we can link to and follow and any shout out you can give would be well" \
          " received from us. \n\nThank you for your time. \nSincerely, \nAdam Szablya\nFounder and CEO at Tourzan.com"
    driver.get(url)
    driver.implicitly_wait(30)
    users = driver.find_elements_by_class_name('ad')
    for idx in range(0, len(users)):
        try:
            driver.execute_script("document.getElementsByClassName('toggle_ad_link user')[{}].click();".format(idx))
            driver.find_elements_by_xpath('//input[@id="email_name"]')[idx].send_keys('Adam Szablya')
            driver.find_elements_by_xpath('//input[@id="email_email"]')[idx].send_keys('contactus@tourzan.com')
            driver.find_elements_by_xpath('//input[@id="email_subject"]')[idx].send_keys('Looking for guides')
            driver.find_elements_by_xpath('//textarea[@id="email_body"]')[idx].send_keys(msg)
            image = driver.find_elements_by_xpath('//div[@class="simple_captcha_image"]/img')[idx]
            captia = handle_captia(image)
            if captia is None:
                refresh(driver)
                continue
            driver.find_elements_by_xpath('//input[@id="email_captcha"]')[idx].send_keys(captia)
            driver.execute_script("document.getElementsByName('commit')[{}].click();".format(idx + 2))
            print('user: %s, page: %s' % (idx, i))
            refresh(driver)
        except Exception as err:
            print(err)
            continue


def main():
    page = 0
    for i in range(0, 476):
        # if failure after prod. manually re-start on next page.
        # uncomment email tag on line 57 before running
        page += 1
        options = webdriver.ChromeOptions()
        options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        options.add_argument('window-size=800x841')
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = 'http://shiroube.com/main#34~15~1~4095~0~0~English~~1~{}'.format(page)
        print(page)
        send_msg(driver, url, i)
        driver.quit()  # possible problem child
        time.sleep(1)

if __name__ == "__main__":
    main()
