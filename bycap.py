from speech_recognition import Recognizer, AudioFile
from os import getcwd, remove
from urllib import request
from pydub import AudioSegment
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def resolveCaptcha(browser):
    # Wait for recaptcha to load
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[0])
    # Check if captcha is alredy solve
    if str(browser.find_element_by_id('recaptcha-anchor').get_attribute("aria-checked")) == "true":
        browser.switch_to.default_content()
        return 2 # Alredy solve
    # Click on captcha checkbox
    browser.find_element_by_id('recaptcha-anchor').click()
    # Switch to ReCaptcha challenge iframe
    browser.switch_to.default_content()
    browser.switch_to.frame(browser.find_element_by_css_selector('iframe[title="recaptcha challenge"]'))
    sleep(1)
    # Check if captcha is alredy open
    try:
        browser.find_element_by_class_name('rc-button-audio').click()
    except:
        browser.switch_to.default_content()
        return 1
    # Switch to ReCaptcha challenge iframe
    browser.switch_to.default_content()
    browser.switch_to.frame(browser.find_element_by_css_selector('iframe[title="recaptcha challenge"]'))
    sleep(0.5)
    try:
        browser.find_element_by_class_name("rc-doscaptcha-header-text")
    except:
        return getRecaptchaAudio(browser)
    browser.switch_to.default_content()
    return 1 # ReCaptcha is block

def getRecaptchaAudio(browser):
    browser.switch_to.default_content()
    browser.switch_to.frame(browser.find_element_by_css_selector('iframe[title="recaptcha challenge"]'))
    # downloading and parsing audio
    request.urlretrieve(browser.find_element_by_css_selector(".rc-audiochallenge-tdownload-link").get_attribute("href"), getcwd()+'/sample.mp3')
    AudioSegment.from_mp3(getcwd()+'/sample.mp3').export(getcwd()+'/sample.wav', format="wav")
    sample_audio = AudioFile(getcwd()+'/sample.wav')
    # recognize audio using google
    r = Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    text = r.recognize_google(audio)
    remove(getcwd()+'/sample.mp3')
    remove(getcwd()+'/sample.wav')
    browser.find_element_by_id("audio-response").send_keys(text.lower())
    browser.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    sleep(1)
    browser.switch_to.default_content()
    browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[0])
        
    if str(browser.find_element_by_id('recaptcha-anchor').get_attribute("aria-checked")) == "true":
        browser.switch_to.default_content()
        return 0 # Solve
    return getRecaptchaAudio(browser)
        
def checkForRecapcha(browser):
    try:
        if browser.find_elements_by_tag_name("iframe")[0].get_attribute("title") == "reCAPTCHA":
            return 1 # Captcha detected
        return 0
    except:
        pass