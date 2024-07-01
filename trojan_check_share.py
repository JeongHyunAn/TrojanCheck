import os
from selenium import webdriver
import datetime
from datetime import timedelta
from twilio.rest import Client
import schedule
import time

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

def complete_daily_health_check(driver):
    driver.get('https://trojancheck.usc.edu/login')
    login = driver.find_elements_by_xpath('//*[contains(text(), "Log in with your USC NetID")]')
    login[0].click()
    driver.implicitly_wait(3)

    id = driver.find_elements_by_name('j_username')
    id[0].send_keys('username')
    pw = driver.find_elements_by_id('password')
    pw[0].send_keys('pw')

    signin = driver.find_elements_by_name("_eventId_proceed")
    signin[0].click()
    driver.implicitly_wait(3)
    cont_button = driver.find_element_by_xpath('/html/body/app-root/app-consent-check/main/section/section/button')
    cont_button.click()
    driver.implicitly_wait(3)
    try:
        begin = driver.find_elements_by_xpath('/html/body/app-root/app-dashboard/main/div/section[1]/div[2]/button')
        begin[0].click()
        driver.implicitly_wait(3)

        start_screening = driver.find_elements_by_xpath('/html/body/app-root/app-assessment-start/main/section[1]/div[2]/button[2]')
        start_screening[0].click()
        driver.implicitly_wait(3)

        #screening question 1
        q1 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-3-button"]')
        q2 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-5-button"]')
        q1[0].click()
        q2[0].click()
        next_button = driver.find_elements_by_xpath('/html/body/app-root/app-assessment-questions/main/section/section[3]/button')
        next_button[0].click()
        driver.implicitly_wait(3)

        #screening question 2
        s1 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-14-button"]')
        s2 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-16-button"]')
        s3 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-18-button"]')
        s4 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-20-button"]')
        s5 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-22-button"]')
        s6 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-24-button"]')
        s7 = driver.find_elements_by_xpath('//*[@id="mat-button-toggle-26-button"]')

        qs = [s1, s2, s3, s4, s5, s6, s7]
        for s in qs:
            s[0].click()

        next_button = driver.find_elements_by_xpath('/html/body/app-root/app-assessment-questions/main/section/section[8]/button')
        next_button[0].click()
        driver.implicitly_wait(3)

        toggle = driver.find_elements_by_xpath('//*[@id="mat-checkbox-1"]')
        toggle[0].click()
        submit_button = driver.find_elements_by_xpath('/html/body/app-root/app-assessment-review/main/section/section[11]/button')
        submit_button[0].click()
        driver.implicitly_wait(3)
    except:
        if "You already took your assessment today" in driver.page_source:
            return False

    return True

def complete_trojan_check_and_send_text():
    driver = webdriver.Chrome('/home/namj/Desktop/tc/chromedriver')
    completed = False
    while not completed:
        try:
            completed = complete_daily_health_check(driver)
        except:
            driver.close()

    qrcode_filename = '{}.png'.format(datetime.date.today())
    try:
        daypass = driver.find_elements_by_xpath('/html/body/app-root/app-dashboard/main/div/section[1]/div/div[2]/app-day-pass/div')
        daypass[0].screenshot('./qrcodes/{}'.format(qrcode_filename))
    except:
        daypass = driver.find_elements_by_xpath('/html/body/app-root/app-assessment-confirmation/main/section[1]/app-day-pass/div')
        daypass[0].screenshot('./qrcodes/{}'.format(qrcode_filename))
    driver.close()

    # send message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                    body='Here is your QR code!', 
                                    from_='+twilionum', 
                                    to='+1yournum',
                                    media_url=['http://760b-104-12-142-133.ngrok.io/qrcodes/{}'.format(qrcode_filename)]
                                    )
    print('message sent!')

if __name__ == '__main__':
    schedule.every().day.at("05:30").do(complete_trojan_check_and_send_text)

    while True:
        schedule.run_pending()
        time.sleep(1)