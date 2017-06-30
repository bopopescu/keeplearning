#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
# element = driver.find_element_by_id("passwd-id")
# element = driver.find_element_by_name("passwd")
# element = driver.find_elements_by_tag_name("input")
# element = driver.find_element_by_xpath("//input[@id='passwd-id']")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
# element.clear()
print driver.page_source