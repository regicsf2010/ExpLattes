# From system
import os
import time
import random
import pyautogui
# From selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# For solving recaptcha
import speech_recognition as sr
import urllib
import pydub
# Others
import zipfile
import xml.etree.ElementTree as et

def downloadCL(id_cnpq, save_path):

    # Define download path
    path_to_download = os.getcwd() + '/' + save_path

    # Define a new instance of firefox with specific options
    options = Options()
    # options.headless = True # Hide firefox window
    options.set_preference('browser.download.folderList', 2) # use specific folder
    options.set_preference('browser.download.dir', path_to_download) # Se path to download
    options.set_preference('browser.helperApps.alwaysAsk.force', False) # Do not ask anything (no pop up)
    options.set_preference('browser.download.manager.showWhenStarting', False) # Do not show anything (no pop up)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip') # MIME type for zip
    print('[INFO] Preferences: OK')

    # Define a new firefox instance
    driver = webdriver.Firefox(options = options)
    width = height = 800
    ss_w, ss_h= pyautogui.size() # Cross-platform to get screen resolution
    driver.set_window_size(width, height)
    driver.set_window_position(ss_w / 2 - width / 2, ss_h / 2 - height / 2) # Center the window
    print('[INFO] Firefox: opened OK')

    # Define default URL
    # Note that the last option (idcnpq) is the professor lattes ID
    location = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq=' + id_cnpq
            
    driver.get(location)
    print('[INFO] Firefox: page loaded OK')

    # Find iframe tag and switch to that iframe context
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(frames[0])

    # Click on recaptcha checkbox and switch to default context
    driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
    driver.switch_to.default_content()

    # Investigate submit button
    button = driver.find_element(By.ID, 'submitBtn')
    time.sleep(random.randint(1, 2))

    # If true, do recaptcha
    # if button.get_attribute('disabled'):
    if not button.is_enabled():
        print('[INFO] Firefox: solve recaptcha for idcnpq {}'.format(id_cnpq))
        # Find iframe tag and switch to that iframe context
        frames = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]').find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[0])

        # Click on recaptcha audio button (alternative way to solve recaptcha)
        time.sleep(random.randint(1, 2))
        driver.find_element(By.ID, 'recaptcha-audio-button').click()

        # Switch to default context again
        driver.switch_to.default_content()

        # Find iframe tag and switch to the last context
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[-1])

        # [Optional] Wait 1 second and play audio
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/button').click()

        #================================================#
        # From now on: download the mp3 audio source,
        # convert to wav format,
        # feed speech recognition algorithm,
        # translate to string,
        # and send string back to recaptcha frame
        #================================================#

        # Download mp3 file
        src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
        file_name = path_to_download + '/sample.mp3'
        urllib.request.urlretrieve(src, file_name)
        print('[INFO] Firefox: download audio OK')

        # Get file and convert to wav extension
        sound = pydub.AudioSegment.from_mp3(file_name)
        file_name = file_name.replace('.mp3', '.wav')
        sound.export(file_name, format = 'wav')
        print('[INFO] Firefox: converted audio OK')

        # Submit audio to a speechrecognition algorithm from Google
        sample_audio = sr.AudioFile(file_name)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)

        key = r.recognize_google(audio)
        print('[INFO] Recaptcha code: {}'.format(key))

        # Send string (key) back to recaptcha page and switch to default context again
        driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
        driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
        driver.switch_to.default_content()

        # Submit solution by clicking the button
        time.sleep(1)
        driver.find_element(By.ID, 'submitBtn').click()
        print('[INFO] Firefox: download zip file OK')

    else: # If false, just click and download zip file
        print('[INFO] Firefox: no recaptcha to solve for {}'.format(id_cnpq))
        time.sleep(1)
        button.click()
        print('[INFO] Firefox: download zip file OK')

    driver.quit()
    
    try:
        os.remove(save_path + '/sample.mp3')
    except 'FileNotFoundError':
        pass
    else:
        print('[INFO] File sample.mp3 deleted.')
        
    try:
        os.remove(save_path + '/sample.wav')
    except 'FileNotFoundError':
        pass
    else:
        print('[INFO] File sample.wav deleted.')  
        

def convert_zip2xml(id_cnpq, in_path, out_path):
    unzip_file(in_path + '/' + id_cnpq + '.zip', out_path)
    
    in_file_name = out_path + '/curriculo.xml'
    out_file_name = out_path + '/' + id_cnpq + '.xml'
    
    os.rename(in_file_name, out_file_name)
    print(f'[INFO] Output:  {out_file_name}')
            
def load_only(in_path, ext):
    files = os.listdir(in_path + '/') 
    return [f for f in files if f.endswith(ext)]
    
def unzip_file(in_path, out_path):
    with zipfile.ZipFile(in_path, 'r') as zip_ref:
        zip_ref.extractall(out_path)