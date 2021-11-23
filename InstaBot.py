from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint,choice
import datetime
import time as tm
from selenium.webdriver.firefox.options import Options
import instaloader


# initial values
hashtag_list = ['#hackerrank']
comments_list = ['really cool! :)','Great work ! :)','Really cool!','that\'s amazing!','awesome work :)']

#options = Options()
#options.headless = True
driver = webdriver.Firefox()


# Getting login credentials
file = open("credentials.txt")
lis = file.readlines()
username = lis[0].strip("\n")
password = lis[1]



class InstaBot:
    def __init__(self,driver):
        self.driver = driver
        self.following_list=[]
        self.login_try = 0
        self.comments = 0
        self.follows = 0
        self.likes = 0
        

    def get_post(self,hashtag):
        try:
            print(f'!!!HASHTAG!!! : {hashtag}')
            self.driver.get('https://www.instagram.com/explore/tags/'+ hashtag.strip('#') + '/')
            sleep(2)
            first_thumbnail = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
            first_thumbnail.click()
            sleep(3)
            errors = self.driver.find_elements_by_link_text("Go back to Instagram.")
            if(len(errors) == 0):
                return True
            else:
                print("Hashtag not available")
                return False
        except:
            print("failes to open Hashtag")
            return False
    def next_post(self):
        try:
            self.driver.find_element_by_link_text('Next').click()
            print('**********NEXT POST**************')
            sleep(3)
            return True
        except:
            print("Failed to get Next post")
            return False
    def login(self,username,password):
        try:
            self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
            sleep(5)
            username_input = self.driver.find_element_by_css_selector("input[name='username']")
            password_input = self.driver.find_element_by_css_selector("input[name='password']")

            username_input.send_keys(username)
            password_input.send_keys(password)


            login_button = self.driver.find_element_by_xpath("//button[@type='submit']")
            login_button.click()
            sleep(3)
            errors = self.driver.find_elements_by_id("slfErrorAlert")
            if len(errors) == 0:
                print(f"Login successfull as: {username}")
                sleep(5)
                return True
            else:
                print("Wrong userName/password....\nEnter correct credentials")
                username = input("Enter Username: ")
                password = input("Enter password: ")
                self.login_try+=1
                if(self.login_try<5):
                    return self.login(username,password)
                else:
                    return False
        except:
            print("Failed to login....\nRetrying login")
            self.login_try+=1
            if(self.login_try<5):
                return self.login(username,password)
            else:
                return False
    
    def like_posts(self,tags,amount = 15):
        for hashtag in tags:
            if(self.get_post(hashtag)):
                sleep(randint(1,2))
                for i in range(amount):
                    try:
                        button_like = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                        button_like.click()
                        self.likes+=1
                        print('_POST LIKED_')
                        sleep(3)
                    except:
                        print("Failed to like to post")
                    if(self.next_post()):
                        pass
                    else:
                        break

    def follow_accounts(self,tags,amount = 10):
        file = open("followed.txt","a+")
        followed = file.readlines()
        followed = [i.strip("\n") for i in followed ]
        for hashtag in tags:
            if(self.get_post(hashtag)):
                sleep(randint(1,2))
                for i in range(amount):
                    try:
                        username = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                        print('USER NAME:',username)
                        if(username not in followed):
                            try:
                                username_button = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                                if  username_button.text == 'Follow':
                                    username_button.click()
                                    print(f'Started following {username} ')
                                    self.follows+=1
                                    self.following_list.append(username)
                                    username+="\n"
                                    file.write(username)
                                    sleep(3)
                                else:
                                    print(f"Already Following {username}")
                            except:
                                print("Failed to follow user!")
                        else:
                            print("Username Found in list")
                    except:
                        print("Failed to follow user")
                    if(self.next_post()):
                        pass
                    else:
                        print("Failed to get next post!")
                        break
        file.close()

    def comment(self,tags,comments_list,amount=5):
        for hashtag in tags:
            if(self.get_post(hashtag)):
                sleep(2)
                for i in range(amount):
                    try:
                        message = comments_list[randint(0,4)]
                        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea').click()
                        comment_box = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                        comment_box.send_keys(message)
                        submit_button = self.driver.find_element_by_xpath("//button[@type='submit']")
                        submit_button.click()
                        self.comments+=1
                        print(f'COMMENTED: {message}')
                        sleep(3)
                    except:
                        print("Failed to comment on the post")
                    if(self.next_post()):
                        pass
                    else:
                        print("Failed to get next post!")
                        break

                    
    def get_followees(self,profile):
        followees=[]
        for followee in profile.get_followees():
            followees.append(followee.username)
        return followees

    def get_followers(self,profile):
        followers = []
        for followee in profile.get_followers():
            followers.append(followee.username)
        return followers

    
    def unfollow(self):
        '''try:
            L = instaloader.Instaloader()
            try:
                L.login(username, password)
                profile = instaloader.Profile.from_username(L.context, username)# (login)
                print("Login successful")
            except instaloader.exceptions.BadCredentialsException: 
                print("Incorrect credentials\nPleases try again!!")
                return
        except:
            print("Failed to get instaloader instance!!")
            return
        print("Getting followers")
        #followers = self.get_followers(profile)
        print("Getting followees")
        #followees = self.get_followees(profile)
        print("Fetch successful")'''
        followers = ['asfdf']
        followees = ["_python.tutorials_"]
        for followee in followees:
            print(followee)
            if followee not in followers:
                driver.get(f'https://www.instagram.com/{followee}/')
                sleep(15)
                driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/div/div/div[2]/div/span/span[1]").click()
                sleep(3)
                button = driver.find_elements_by_xpath("//*[contains(text(), 'Unfollow')]")
                button.click()
                sleep(5)
                break
                
        
        
    def get_logs(self):
        print(f"Number of account's liked: {self.likes}\nNumber of account's followed: {self.follows}\nNumber of post's commented: {self.comments}")
        

    



#main 

bot = InstaBot(driver)

state = bot.login(username,password)
if (state):
    #bot.like_posts(hashtag_list)
    bot.follow_accounts(hashtag_list)
    #bot.comment(hashtag_list,comments_list)
    #bot.unfollow()
    bot.get_logs()
    driver.quit()
else:
    print("Failed to login multiple times.\n Exitting the program...")
    driver.quit()
    exit()

