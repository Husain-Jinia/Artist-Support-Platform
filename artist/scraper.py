
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re


browser = webdriver.Firefox()

browser.get("https://www.instagram.com/?hl=en")

time.sleep(5)

username = browser.find_element_by_css_selector("[name='username']")

password = browser.find_element_by_css_selector("[name='password']")

login = browser.find_element_by_css_selector("button")


username.send_keys("tester02012001")

password.send_keys("tester123$")

login.click()

time.sleep(5)



tags = [

    "DigitalArt",
    "Art",
    "sketch",
]



while True:

    for tag in tags:
        sleepy_time = 5
        url= f"https://www.instagram.com/explore/tags/{tag}"
        browser.get(url)

        time.sleep(sleepy_time)


        browser.execute_script("window.scrollTo(0, 2000);")
        pictures = browser.find_elements_by_tag_name("div[class='eLAPa']")



        image_count = 0
        total_image_count = 0



        for picture in pictures:

            if total_image_count >= 9:
                break


            picture.click()

            time.sleep(5)

            # like_value = browser.find_element_by_xpath("div[@class='Igw0E']/div/a/span").text
            # print(like_value)

            like = browser.find_element_by_partial_link_text("like")
            like_value = like.text
            print("log"+like_value)
            like_value = re.split("\s", like_value)
            like_value = like_value[0]
            like_value = re.sub(",","",like_value)
            like_value = int(like_value)
            print(like_value)

            #getting the time it was posted on
            posted_on = browser.find_element_by_class_name("Nzb55").get_attribute("title")
            elapsed_time = browser.find_element_by_class_name("Nzb55").text
            elapsed_time = re.split("\s", elapsed_time)
            print(elapsed_time)
            day = elapsed_time[1]
            print(day)
            elapsed_time = elapsed_time[0]
            print(posted_on, elapsed_time)

            #getting the name and link of the artist
            artist_name = browser.find_element_by_class_name("yWX7d").text
            artist_link = browser.find_element_by_class_name("yWX7d").get_attribute("href")
            print(artist_name,artist_link)

            artist_pp = browser.find_element_by_class_name("_6q-tv").get_attribute("src")
            print(F'************************{artist_pp}')

            #getting the post
            artist_post = browser.find_element_by_class_name("FFVAD").get_attribute('src')
            print(artist_post)

            close = browser.find_element_by_css_selector("[aria-label='Close']")

            close.click()
            # print(int(like_value)<=500, int(elapsed_time)>1, day=="h")
            if int(like_value)<=500 and (int(elapsed_time)>=4 and day=="h"):
                # artist = Artist(artist_name = artist_name,
                # artist_link=artist_link, likes = like_value,
                # elapsed_time = elapsed_time, 
                # post_time = posted_on, 
                # post_link=artist_post, 
                # tag=tag)

                # artist.register()
                print("success")


            else:
                print("nice")

            time.sleep(2)
        
            total_image_count+=1
        

    time.sleep(3600)