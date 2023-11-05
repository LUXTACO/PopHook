import os
import re
import csv
import time
import image
import random
import logger as loglib
from pynput.keyboard import Listener, Key

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Start:
    def __init__(self, path=os.getcwd(), debug=False):
        self.debug = debug
        
        if self.debug:
            self.logger = loglib
        else:
            class logger:
                def Log(typeL, execPart, message):
                    pass
            self.logger = logger
            
        self.driverInfo = self.DriverSetup()
        if self.driverInfo:
            self.driverLoop = self.DriverMainLoop()
    
    def DriverSetup(self):
        self.name = None
        self.state = True
        self.roomCode = None
        self.roomName = None
        
        self.driver = None
        self.dummyDriver = None
        
        self.genUsername = lambda:None
        self.genUsername.host = None
        self.genUsername.dummy = None
        
        self.logger.Log("session", "", "")
        
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        if self.debug == False:
            self.chrome_options.add_argument("--headless")
            
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 50)
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
        
        self.driver.get("https://jklm.fun/")
        self.startTime = time.time()
        
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body")))
            self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[5]/div[1]")))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/button")))
            self.logger.Log("info", "PopSetup", "Page loaded successfully")
            time.sleep(2)
        except Exception as e:
            self.logger.Log("error", "PopSetup", type(e).__name__ + " - " + str(e))
            self.state = False
            
        if self.state:
            while True:
                try:
                    self.name = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/button/span").text
                    if self.name.lower().find("pophook") != -1:
                        self.logger.Log("info", "PopSetup", f"No need to change name: {self.name}")
                    else:
                        self.genUsername.host = "PopHook" + str(random.randint(1000, 9999))
                        self.logger.Log("notice", "PopSetup", f"Changing name from {self.name} to {self.genUsername.host}")
                        self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/button").click()
                        self.driver.find_element(By.XPATH, "/html/body/div/div[4]/div/form[1]/div[2]/input").send_keys(self.genUsername.host)
                        self.driver.find_element(By.XPATH, "/html/body/div/div[4]/div/form[1]/div[2]/button").click()
                        self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/button/span")))
                        self.name = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/button/span").text
                        if self.name.lower().find("pophook") != -1:
                            self.logger.Log("info", "PopSetup", f"Name changed successfully to {self.name}")
                            break
                        else:
                            self.logger.Log("error", "PopSetup", f"Failed to change name to {self.genUsername.host}")
                            self.state = False
                except Exception as e:
                    self.logger.Log("error", "PopSetup", type(e).__name__ + " - " + str(e))
                    self.state = False
            
            if self.state:
                while True:
                    try:
                        self.driver.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div[1]/div/form/div[1]/div[3]").click()
                        self.logger.Log("info", "PopSetup", "Successfully selected the gamemode")
                        try:
                            self.roomName = self.driver.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div[1]/div/form/div[2]/input[1]").text
                        except:
                            self.roomName = "Unknown"
                        self.driver.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div[1]/div/form/div[2]/label[2]").click()
                        self.logger.Log("info", "PopSetup", "Successfully selected the room type")
                        self.driver.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div[1]/div/form/div[2]/button").click()
                        self.logger.Log("info", "PopSetup", "Successfully created a room")
                        break
                    except Exception as e:
                        self.logger.Log("error", "PopSetup", type(e).__name__ + " - " + str(e))
                        self.state = False
                        self.driver.refresh()
            
                if self.state:
                    try:
                        self.logger.Log("info", "PopSetup", "Waiting for the room to load")
                        self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div[1]")))
                        self.logger.Log("info", "PopSetup", "Room loaded successfully")
                        self.roomCode = self.driver.current_url.replace("https://jklm.fun/", "")
                        self.logger.Log("info", "PopSetup", f"Room code: {self.roomCode}")
                    except Exception as e:
                        self.logger.Log("error", "PopSetup", type(e).__name__ + " - " + str(e))
                        self.state = False
                        
                    if self.state:
                        try:
                            self.dummyDriver = webdriver.Chrome(options=self.chrome_options)
                            self.dummyWait = WebDriverWait(self.dummyDriver, 50)
                            stealth(self.dummyDriver,
                                languages=["en-US", "en"],
                                vendor="Google Inc.",
                                platform="Win32",
                                webgl_vendor="Intel Inc.",
                                renderer="Intel Iris OpenGL Engine",
                                fix_hairline=True)
                            self.dummyDriver.get("https://jklm.fun/")
                            self.dummyWait.until(EC.presence_of_element_located((By.XPATH, "/html/body")))
                            self.dummyWait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[5]/div[1]")))
                            self.dummyWait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/button")))
                            time.sleep(2)
                            
                            self.name = self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/button/span").text
                            if self.name.lower().find("pophook") != -1:
                                self.logger.Log("info", "PopDummy", f"No need to change name: {self.name}")
                            else:
                                while True:
                                    try:
                                        self.genUsername.dummy = "PopHook" + str(random.randint(1000, 9999))
                                        self.logger.Log("notice", "PopDummy", f"Changing name from {self.name} to {self.genUsername.dummy}")
                                        self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/button").click()
                                        self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[4]/div/form[1]/div[2]/input").send_keys(self.genUsername.dummy)
                                        self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[4]/div/form[1]/div[2]/button").click()
                                        self.dummyWait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/button/span")))
                                        self.name = self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/button/span").text
                                        if self.name.lower().find("pophook") != -1:
                                            self.logger.Log("info", "PopDummy", f"Name changed successfully to {self.name}")
                                            break
                                        else:
                                            self.logger.Log("error", "PopDummy", f"Failed to change name to {self.genUsername.dummy}")
                                            self.state = False
                                    except Exception as e:
                                        self.logger.Log("error", "PopDummy", type(e).__name__ + " - " + str(e))
                                        self.state = False
                            
                            if self.state:
                                try:
                                    self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div[2]/div[1]/form/div/input").send_keys(self.roomCode)
                                    self.dummyDriver.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div[2]/div[1]/form/div/div[2]/button").click()
                                    self.logger.Log("info", "PopDummy", "Successfully joined the room")
                                    self.dummyWait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[1]/iframe")))
                                    self.logger.Log("info", "PopDummy", "Successfully loaded the game")
                                    self.dummyDriver.switch_to.frame(self.dummyDriver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/iframe"))
                                    self.dummyWait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/button")))
                                    self.dummyDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/button").click()
                                    self.logger.Log("info", "PopDummy", "Successfully joined the game")
                                except Exception as e:
                                    self.logger.Log("error", "PopDummy", type(e).__name__ + " - " + str(e))
                                    self.state = False   
                        except Exception as e:
                            self.logger.Log("error", "PopDummy", type(e).__name__ + " - " + str(e))
                            input(self.logger.Printcol("error", "PopDummy", f"Error with dummy driver, try to join with another browser (room code: {self.roomCode}) and press ENTER to continue"))
                        
                        if self.state:
                            try:
                                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/iframe"))
                                self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/button")))
                                self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/button").click()
                                self.logger.Log("info", "PopSetup", "Successfully joined the game")
                            except Exception as e:
                                self.logger.Log("error", "PopSetup", type(e).__name__ + " - " + str(e))
                                self.state = False
                            
                            if self.state:
                                try:
                                    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/button").click()
                                    try:
                                        while True:
                                            self.driver.find_element(By.CLASS_NAME, "remove").click()
                                    except Exception as e:
                                        pass
                                    self.logger.Log("info", "PopSetup", "Successfully removed the tags and exclusions")
                                    time.sleep(random.uniform(0.1, 0.5))
                                    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/fieldset/div[5]/div[3]/input[1]").click()
                                    
                                    self.actionChains = ActionChains(self.driver)
                                    self.actionChains.send_keys(Keys.BACKSPACE)
                                    self.actionChains.pause(0.1)
                                    self.actionChains.send_keys(Keys.BACKSPACE)
                                    self.actionChains.pause(0.1)
                                    self.actionChains.send_keys("7")
                                    self.actionChains.pause(0.1)
                                    self.actionChains.send_keys(Keys.ENTER)
                                    self.actionChains.perform()
                                    
                                    self.logger.Log("info", "PopSetup", "Successfully set 7 seconds per question")
                                    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/button").click()
                                    self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div/a")))
                                    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/a").click()
                                    self.logger.Log("info", "PopSetup", "Successfully started the game")
                                    self.endTime = time.time()
                                except Exception as e:
                                    self.logger.Log("error", "PopSetup", type(e).__name__ + " - " + str(e))
                                    self.state = False
                                
                                self.logger.Log("info", "PopSetup", f"Setup took {round(self.endTime - self.startTime, 2)} seconds")
                                return True

    def DriverMainLoop(self):
        self.image = None
        self.prompt = None
        self.answer = None
        self.text = None
        
        self.old_image = None
        self.old_prompt = None
        self.old_answer = None
        
        self.hashData = []
        self.answerData = []
        self.promptData = []
        
        self.imageElement = None
        
        self.waitshort = WebDriverWait(self.driver, 5)
        
        self.logger.Log("info", "PopMainS", "Variable setup complete, starting main loop")
        
        def KeyPress(key):
            if key == Key.f8:
                try:
                    self.currentPath = os.getcwd()
                    self.logger.Log("info", "PopMainS", "F8 pressed, saving data")
                    self.path = self.currentPath + "\\data\\database" + str(time.strftime("%d-%m-%Y")) + ".csv" 
                    with open(self.path, "a", newline="", encoding="utf-8") as csvfile:
                        self.writer = csv.writer(csvfile)
                        #check if file is empty
                        if os.stat(self.path).st_size == 0:
                            self.writer.writerow(["ImageHash", "Prompt", "Answer"])
                        for i in range(len(self.hashData)):
                            self.writer.writerow([self.hashData[i], self.promptData[i], self.answerData[i]])
                    
                    self.hashData.clear()
                    self.answerData.clear()
                    self.promptData.clear()
                    self.logger.Log("info", "PopMainS", "Successfully saved data")
                    
                except Exception as e:
                    self.logger.Log("error", "PopMainS", type(e).__name__ + " - " + str(e))
                    self.logger.Log("error", "PopMainS", "Failed to save data")
        
        with Listener(on_release=KeyPress) as listener:
            self.currentPath = os.getcwd()
            self.dataTempFiles = f"{self.currentPath}\\runtime\\PopHook_{self.roomCode}"
            os.system(f"mkdir {self.dataTempFiles}")
            self.logger.Log("info", "PopMainS", f"Created temporary folder: {self.dataTempFiles}")
            
            while True:
                try:
                    try:
                        while True:
                            try:
                                self.waitshort.until(EC.element_to_be_clickable((By.CLASS_NAME, "actual")))
                                self.imageElement = self.driver.find_element(By.CLASS_NAME, "actual")
                                self.imageUrl = self.driver.execute_script("function image() {return document.getElementsByClassName('actual')[0].getAttribute('style')};return image();")
                            except:
                                self.imageUrl = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/div").text
                                if (self.imageUrl != None or self.imageUrl != "None") and self.imageUrl != self.old_image:
                                    if self.imageUrl == None or self.imageUrl == "None" or len(self.imageUrl) == 0:
                                        self.text=None
                                    else:
                                        if self.imageUrl == self.old_image:
                                            self.text = None
                                        else:
                                            self.text = self.imageUrl.replace("\n", " ")
                                            self.logger.Log("info", "PopMainS", f"Successfully saved the text: {self.text}")
                                            break
                                else:
                                    self.text = None
                            if self.imageUrl == self.old_image:
                                continue
                            elif self.imageUrl == None or self.imageUrl == "None":
                                    continue
                            elif (self.imageUrl != None or self.imageUrl != "None") and self.imageUrl != self.old_image:
                                if self.imageUrl == None or self.imageUrl == "None" or len(self.imageUrl) == 0:
                                    continue
                                else:
                                    self.printimageUrl = re.search("(?P<url>https?://[^\s])", self.imageUrl).group("url")
                                    self.printimageUrl = self.printimageUrl.replace(");", "")
                                    self.logger.Log("info", "PopMainS", f"Successfully saved the image url: {self.printimageUrl}")
                                    break
                        self.old_image = self.imageUrl
                        if self.text != None:
                            self.image = self.text
                        else:
                            self.imageScreen = self.imageElement.screenshot(self.dataTempFiles + "\\image.png")
                            self.logger.Log("info", "PopMainS", "Successfully saved the image")
                            self.image = image.GatherData(self.dataTempFiles + "\\image.png", do_hash=True, hash_type="sha256", debug=self.debug)
                    except Exception as e:
                        self.logger.Log("error", "PopMainS", type(e).__name__ + " - " + str(e))
                        
                    try:
                        while True:
                            self.prompt = self.driver.execute_script("function prompt() {return document.getElementsByClassName('prompt')[0].textContent};return prompt();")
                            if self.prompt == self.old_prompt:
                                continue
                            elif self.prompt != None and self.prompt != self.old_prompt:
                                self.old_prompt = self.prompt
                                self.logger.Log("info", "PopMainS", f"Successfully saved the prompt: {self.prompt}")
                                break
                    except Exception as e:
                        self.logger.Log("error", "PopMainS", type(e).__name__ + " - " + str(e))
                    
                    try:
                        while True:
                            self.answer = self.driver.execute_script("function answer() {return document.getElementsByClassName('value')[0].textContent};return answer();")
                            if self.answer == self.old_answer:
                                continue
                            elif self.answer == None or self.answer == "None" or len(self.answer) == 0:
                                continue
                            elif (self.answer != None or self.answer != "None") and self.answer != self.old_answer:
                                self.old_answer = self.answer
                                self.logger.Log("info", "PopMainS", f"Successfully saved the answer: {self.answer}")
                                break
                    except Exception as e:
                        self.logger.Log("error", "PopMainS", type(e).__name__ + " - " + str(e))

                    if self.image != None and self.prompt != None and self.answer != None:
                        if self.text == None:
                            self.hashData.append(self.image.image_hash)
                        else:
                            self.hashData.append(self.image)
                        self.promptData.append(self.prompt)
                        self.answerData.append(self.answer)
                        self.logger.Log("info", "PopMainS", f"Successfully saved the data to the list")
                        self.logger.Log("info", "PopMainS", f"Total data saved: {len(self.hashData)}")
                        self.logger.Log("info", "PopMainS", f"Total answers saved: {len(self.answerData)}")
                        self.logger.Log("info", "PopMainS", f"Total prompts saved: {len(self.promptData)}")
                        
                        if len(self.hashData) >= 5:
                            KeyPress(Key.f8)
                        
                except Exception as e:
                    self.logger.Log("error", "PopMainS", type(e).__name__ + " - " + str(e))
                    
Start(debug=True)