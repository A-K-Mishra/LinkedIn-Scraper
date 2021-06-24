from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('d:/Scrapy/chromedriver_win32/chromedriver.exe')
driver.maximize_window()
sleep(0.5)
driver.get('https://www.linkedin.com/')
sleep(2)
driver.find_element_by_xpath('//a[text() = "Sign in"]').click()
sleep(2)
username_input = driver.find_element_by_name('session_key')
username_input.send_keys(os.environ['EMAIL_USER'])
sleep(2)
password_input = driver.find_element_by_name('session_password')
password_input.send_keys(os.environ['LINKEDIN_PASS'])
sleep(2)
sign_in_btn =driver.find_element_by_xpath('//button[text()="Sign in"]')
sign_in_btn.click()
sleep(2)
# I have 2-step verification enabled, so next step is to get OTP
otp_input = driver.find_element_by_name('pin')
print('Enter OTP send to your registred mobile number ...')
otp = input().strip()
otp_input.send_keys(otp)
sleep(2)
#click submit
driver.find_element_by_xpath('//button[text()="Submit"]').click()
print('You have successfully logged in ...')

#go to google.com to search profiles
driver.get('https://www.google.com/')
sleep(2)
search_input = driver.find_element_by_name('q')
search_input.send_keys('site: linkedin.com/in/ AND "Python Developer" AND "India"')
sleep(1)
search_input.send_keys(Keys.RETURN)
sleep(3)
# get the search  results
profiles = driver.find_elements_by_xpath('//*[@class="g"]/div/div/div/a')
profiles=[profile.get_attribute('href') for profile in profiles]
sleep(2)
