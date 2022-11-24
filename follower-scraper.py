from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
import getpass


#Define function "followerscrepe()" which is responsible for the scraping process
def followerscrape(usr, pw, ig_usr):

    #Author and Copyright references
    print("[Notice] - Follower List Scraper by NaBo-00\n[Notice] - Copyright NaBo-00 | All Rights Reserved")

    #Actual Scraping process starts
    print("[START] - followerscraper.py")

    #Set up Driver for Google Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #Specify the path to chromedriver.exe
    s = Service('chromedriver.exe')
    myDriver = webdriver.Chrome(service=s, options=options)

    #Specify the website you want to scrape data from
    myDriver.get("https://www.instagram.com")

    #Specify the timeout of the driver
    timeout = 15

    #Handle Alert - allow only neccessary cookies
    cookies = WebDriverWait(myDriver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]' ))).click()

    #Login to IG by identifying the necessary input fields
    #Specify username and password input field
    username = WebDriverWait(myDriver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input' ))) #//*[@id="loginForm"]/div/div[1]/div/label/input
    password = WebDriverWait(myDriver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input' ))) #//*[@id="loginForm"]/div/div[2]/div/label/input

    #Make sure that the input fields are empty
    username.clear()
    password.clear()

    #Enter username and password
    username.send_keys(usr)
    password.send_keys(pw)

    #Click LogIn Button
    loginBtn = WebDriverWait(myDriver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button' ))).click() #//*[@id="loginForm"]/div/div[3]/button/div
    time.sleep(5)

    #Return response - Login
    print("[Info] - Successful Login")

    #Handle Alert - not now (save credentials) --> remove comments of the following two lines if needed
    #time.sleep(2)
    #notNowCredentials = WebDriverWait(myDriver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button' ))).click()

    #Handle Alert - not now (notifications)
    WebDriverWait(myDriver, 5)
    notNowNotification = WebDriverWait(myDriver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]' ))).click()

    #Switch to profile
    myDriver.get('https://www.instagram.com/' + ig_usr)
    time.sleep(5)

    #Identify User Information
    numberPosts = myDriver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/div/span").text
    numberFollowers = myDriver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span').text
    numberFollowing = myDriver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span').text
    profile_header = myDriver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/span').text

    #Remove . from numberFollowers --> This applies only fom values of 1000
    numberFollowers = numberFollowers.replace(".", "")
    time.sleep(3.5)

    #Switch to the follower list of the IG's profile
    myDriver.get('https://www.instagram.com/' + ig_usr + '/followers')
    time.sleep(5)

    #Return Response - Scraping
    print("[Info] - Scraping...")

    #Loop through followers
    time.sleep(5)
    #Calculate how often the follower list needs to be scrolled to capture all followers
    totalScroll = int(numberFollowers)//12
    countScroll = 0
    print("[Info] - Total Number of Scrolls: " + str(totalScroll))

    for i in range(totalScroll):
        #After click follower button, wait until dialog appear
        time.sleep(5)
        #Idedntify the follower list dialog box
        dialog = WebDriverWait(myDriver, 10).until(lambda d: d.find_element(by=By.XPATH, value='/ html / body / div[1] / div / div / div / div[2] / div / div / div[1] / div / div[2] / div / div / div / div / div / div / div / div[2]'))
        time.sleep(5)
        #Execute scroll
        myDriver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;', dialog)
        #Return number of current scroll iteration
        print("[Info] - Iteration of Scrolls: " + str(countScroll + 1) + "/" + str(totalScroll))
        countScroll += 1

    time.sleep(10)

    #Define Arrays to structure and store IG user's profile data
    arrayCounter = []
    arrayFollowersLink = []
    arrayFollowers = []
    count = 1

    #Append scraped data to the aforementioned Arrays
    for i in range(1, int(numberFollowers) + 1):
        options = myDriver.find_elements(by=By.XPATH, value="/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div/div[" + str(i) + "]/div[2]/div[1]/div/div/div/a")

        for option in options:
            arrayFollowersLink.append(option.get_attribute('href')) # Followers Profile Link
            arrayFollowers.append(option.get_attribute('href').split("/")[3]) # Followers Profile Name
            arrayCounter.append(count) # Followers Profile ID
            count += 1

    #Save scraped data in a DataFrame using Pandas
    #Stores general profile info
    df_general = pd.DataFrame({'Profile_name': [ig_usr], 'Profile_header': [profile_header],
                        'Posts': [numberPosts], 'Followers': [numberFollowers],
                        'Following': [numberFollowing]})

    #Stores follower list
    df_followers = pd.DataFrame({'ID': arrayCounter, 'Followers Profile Name': arrayFollowers, 'Followers Link': arrayFollowersLink })

    #Remove the comments for the following two lines to return the dataframes in the console
    #print(df_general)
    #print(df_followers)


    #Prepare excel file
    print('[Info] - Creating Excel File: follower_list-' + ig_usr + '.xlsx' )

    #Save data in an excel file (includes two sheets)
    #Sheets name can only be 31 characters long
    short_profile_name = 'FollowersList of ' + ig_usr
    sheet_name = short_profile_name[:30]

    #Configure excel file -> df_general on sheet 1 called "Profile Overview" and df_follower on sheet 2 called sheet_name
    dataframes = {'Profile-Overview': df_general, sheet_name: df_followers}

    #Create excel file
    excelPath = 'follower_list-' + ig_usr + '.xlsx'

    #Set writer
    writer = pd.ExcelWriter(excelPath, engine='xlsxwriter')

    #Loop through the sheets, write the data and save the file
    for sheet_name in dataframes.keys():
        dataframes[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()
    time.sleep(5)

    print("[Info] - Excel File creation was successful")

    #Clos the browser
    myDriver.close()

    #Return info to the user
    print("[Done] - Finished scraping!")
    print("[STOP] - followerscraper.py")

#Execution:
try:
    # Query User's credentails and the profile's IG name, which needs to be scraped
    print("Please insert your Instagram credentials:")

    # Save User's credentials
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    # Save Profile's IG name
    instagram_user = input("Please enter an Instagram-User to scrape their Follower-List from: ")

    # Execute the aforementioned function called "followerscrape(usr, pw, ig_usr)"
    followerscrape(username, password, instagram_user)
except:
    #Return message on error
    print("Oh NO! - Something went wrong. Check your credentials and try again.")
