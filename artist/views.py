from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import Artist
import re
from .models import Tagname
import urllib3
from urllib3 import ProxyManager, make_headers
import requests
import tempfile
from django.core import files
from io import BytesIO
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
        "sketch"
    ]



    while True:

        for tag in tags:
            sleepy_time = 5
            url= f"https://www.instagram.com/explore/tags/{tag}"
            browser.get(url)

            time.sleep(3)


            browser.execute_script("window.scrollTo(0, 2000);")
            pictures = browser.find_elements_by_css_selector("div[class='eLAPa']")



            image_count = 0
            total_image_count = 0

            print(str(pictures)+"22222222222222222222222")

            artist_post = browser.find_elements_by_class_name("FFVAD")

            print(artist_post)
            c=0
            for picture in pictures:

                if total_image_count == 6:
                    break

                # artist_post = browser.find_element_by_class_name("FFVAD").get_attribute('src')
                # print(artist_post)

                

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
                

                artist_pp = browser.find_element_by_class_name("_6q-tv").get_attribute("src")
                print(artist_pp)

                #getting the post
            
                # # Stream the image from the url
                # response = requests.get(artist_post, stream=True)

                # # Was the request OK?
                # if response.status_code != requests.codes.ok:
                #     # Nope, error handling, skip file etc etc etc
                #     continue
                
                # # Get the filename from the url, used for saving later
                # file_name = artist_post.split('/')[-1]
                
                # # Create a temporary file
                # lf = tempfile.NamedTemporaryFile()

                # # Read the streamed image in sections
                # for block in response.iter_content(1024 * 8):
                    
                #     # If no more file then stop
                #     if not block:
                #         break

                #     # Write image block to temporary file
                #     lf.write(block)

                    # # Create the model you want to save the image to
                    # image = Image()

                    # # Save the temporary image to the model#
                    # # This saves the model so be sure that it is valid
                    # image.image.save(file_name, files.File(lf))
                link = artist_post[c].get_attribute("src")
                c=c+1
                resp = requests.get(link)
                fp = BytesIO()
                fp.write(resp.content)
                file_name = f"{artist_name}.jpg"  
                

                close = browser.find_element_by_css_selector("[aria-label='Close']")

                close.click()
                # print(int(like_value)<=500, int(elapsed_time)>1, day=="h")
                if int(like_value)<=5000 and (int(elapsed_time)>=1 and (day=="d"or day=='h')):

                    
                    print("rrrrrrrrrrrrrrrrrrr")
                    artist = Artist(artist_name = artist_name,
                    artist_link=artist_link, likes = like_value,
                    elapsed_time = elapsed_time, 
                    artist_pp = artist_pp,
                    post_time = posted_on, 
                    post_link=link,
                    tagname = tag
                    )
                    artist.instagram_post.save(file_name, files.File(fp))
                    # artist.instagram_post(file_name, files.File(lf))

                    # tag_name = Tagname(tag=tag)

                    artist.register()
                    # tag_name.register()
                    print("wohooooooooooooooooooooooooooooooooooooooo")


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


    

    
    
    
    
    
