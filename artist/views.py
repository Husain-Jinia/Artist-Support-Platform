from django.shortcuts import render,redirect
from django.views import View
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import Artist
import re
from .models import Tagname
from .credentials import my_username, my_password

# Create your views here.
def home(request):
    
    return render(request, "homepage.html")


def adminpage(request):
    return render(request, "adminpage.html")

def scrape(request):

    browser = webdriver.Firefox()

    browser.get("https://www.instagram.com/?hl=en")

    time.sleep(5)

    username = browser.find_element_by_css_selector("[name='username']")

    password = browser.find_element_by_css_selector("[name='password']")

    login = browser.find_element_by_css_selector("button")


    username.send_keys(my_username)

    password.send_keys(my_password)

    login.click()

    time.sleep(5)



    tags = [

        "DigitalArt",
        "Art",
    ]



    while True:

        for tag in tags:
            sleepy_time = 5
            url= f"https://www.instagram.com/explore/tags/{tag}"
            browser.get(url)

            time.sleep(sleepy_time)


            browser.execute_script("window.scrollTo(0, 2000);")
            pictures = browser.find_elements_by_css_selector("div[class='eLAPa']")



            image_count = 0
            total_image_count = 0



            for picture in pictures:

                if total_image_count >= 9:
                    break


                picture.click()

                time.sleep(5)



                like = browser.find_element_by_partial_link_text("like")
                like_value = like.text
                print("bruhhhhhhhhhhhhhhhh"+like_value)
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

                #getting the post
                artist_post = browser.find_element_by_class_name("FFVAD").get_attribute('src')
                print(artist_post)

                close = browser.find_element_by_css_selector("[aria-label='Close']")

                close.click()
                # print(int(like_value)<=500, int(elapsed_time)>1, day=="h")
                if int(like_value)<=5000 and (int(elapsed_time)>=1 and day=="h"):
                    artist = Artist(artist_name = artist_name,
                    artist_link=artist_link, likes = like_value,
                    elapsed_time = elapsed_time, 
                    post_time = posted_on, 
                    post_link=artist_post, 
                    tag=tag)

                    artist.register()


                else:
                    print("nice")

                time.sleep(2)
            
                total_image_count+=1
            

        time.sleep(3600)

        return redirect("adminpage.html")

def artpage(request):
    artists = None
        
    Tags = Tagname.get_all_tags()
    TagId = request.GET.get('tagname')
    if TagId:
        artists = Artist.get_all_artists_by_tagid(TagId)
    else:
        artists= Artist.get_all_artists()
    data = {}
    data['artists']= artists
    data['tags'] = Tags
    return render(request, 'artpage.html', data)


    

    
    
    
    
    
