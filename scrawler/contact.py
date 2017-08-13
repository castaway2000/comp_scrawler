#author: Adam Szablya
#Date: 08/09/2017
#Description: messaging section for the spider
import time
from selenium import webdriver
from threading import Thread


def contact(file):
    for idx, line in enumerate(open(file).read()):
        if idx != 0 and idx < 2:
            Thread(message(str(line))).start()


def message(url):
    msg = 'Hello! I saw your listing and thought you might be interested in tourzan.com its a tourguide service that ' \
          'lets locals like yourself make cash showing guests like me around. '\
          'its pretty neat from what i have seen its small but growing and I think it could benefit from more locals ' \
          'like you'

    contact_host_btn_class = "component_9w5i1l-o_O-component_button_r8o91c"
    text_area_class = "textarea_1wa8nj9-o_O-block_r99te6"
    submit_class = "container_1xx0s4e-o_O-container_rounded_sa8zo9-o_O-container_block_zdxht7-o_O-container_" \
                   "sizeRegular_1flp9iz-o_O-container_styleDefault_1gjmt49"
    driver = webdriver.Chrome()
    driver.get(url)
    # time.sleep(5)
    contact_btn = driver.find_element_by_class_name(contact_host_btn_class)
    contact_btn.click()
    # time.sleep(3)
    text_area = driver.find_element_by_class_name(text_area_class)
    text_area.send_keys(msg)
    submit_btn = driver.find_element_by_class_name(submit_class)
    # submit_btn.click()
    # text_area.clear()



