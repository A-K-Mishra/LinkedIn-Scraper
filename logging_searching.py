from selenium import webdriver
from time import sleep
from parameters import * 
from parsel import Selector
from selenium.webdriver.common.keys import Keys
import csv

# open csv file to write data out
writer = csv.writer(open(result_file,'w',encoding = 'utf-8'))
writer.writerow(['name','job','location','education','LinkedIn Url'])


# open driver
driver = webdriver.Chrome('d:/Scrapy/chromedriver_win32/chromedriver.exe')
driver.maximize_window()
sleep(0.5)

# log in to linked in
driver.get('https://www.linkedin.com/')
sleep(2)
driver.find_element_by_xpath('//a[text() = "Sign in"]').click()
sleep(2)
username_input = driver.find_element_by_name('session_key')
username_input.send_keys(username)
sleep(2)
password_input = driver.find_element_by_name('session_password')
password_input.send_keys(password)
sleep(2)
sign_in_btn =driver.find_element_by_xpath('//button[text()="Sign in"]')
sign_in_btn.click()
sleep(5)


# I have 2-step verification enabled, so next step is to get OTP
print('Enter OTP sent to your registered mobile number ...')
otp = input().strip()
    
otp_input = driver.find_element_by_name('pin')

otp_input.send_keys(otp)
sleep(2)


#click submit
driver.find_element_by_xpath('//button[text()="Submit"]').click()
print('You have successfully logged in ...')


#go to google.com to search profiles
driver.get('https://www.google.com/')
sleep(2)
search_input = driver.find_element_by_name('q')
search_input.send_keys(search_query)
sleep(1)
search_input.send_keys(Keys.RETURN)
sleep(3)


# get the search  results
profiles = driver.find_elements_by_xpath('//*[@class="g"]/div/div/div/a')
profiles=[profile.get_attribute('href') for profile in profiles]
sleep(2)

for profile in profiles:
    driver.get(profile)
    sleep(10)
    sel  = Selector(text=driver.page_source)
    name = sel.xpath('//h1/text()').extract_first()
    name = name.strip()
    if 'Jobs' in name:
        continue
    desg = sel.xpath('//main//section//div/h1/../following-sibling::div[1]/text()').extract_first()
    if desg :
        desg = desg.strip()
    location= sel.xpath('//div[@class="pb2"]/span[1]/text()').extract_first()
    if location :
        location = location.strip()
    education = sel.xpath('//*[contains(@class,"pv-entity__school-name")]/text()').extract()

    writer.writerow([name,desg,location,education,driver.current_url])
    dist_value = sel.xpath('//span[@class="dist-value "]/text()').extract_first().strip()
    if dist_value and dist_value == '3rd':
        driver.find_element_by_xpath('//*[text()="More"]').click()
        sleep(2)
        cnct_st = sel.xpath('//*[@data-control-name="connect"]/span[1]/text()').extract_first()
        if cnct_st and cnct_st == 'Pending' :
            continue
        driver.find_element_by_xpath('//*[text()="Connect"]').click()
        sleep(2)
        driver.find_element_by_xpath('//*[text()="Connect"]').click()
        sleep(2)
        driver.find_element_by_xpath('//*[text()="Send"]').click()
        sleep(2)
    elif dist_value and dist_value == '2nd':
        cnct_st = sel.xpath('//*[@data-control-name="connect"]/span[1]/text()').extract_first()
        if cnct_st and cnct_st == 'Pending' :
            continue
        driver.find_element_by_xpath('//*[text()="Connect"]').click()
        sleep(2)
        driver.find_element_by_xpath('//*[text()="Send"]').click()
        sleep(2)
    else:
        continue

        





driver.quit()

