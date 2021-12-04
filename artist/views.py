from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import Posts
import re
from .models import Tagname
import urllib3
from urllib3 import ProxyManager, make_headers
import requests
import tempfile
from django.core import files
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from io import BytesIO
from .credentials import my_username, my_password

# Create your views here.
def home(request):
    
    return render(request, "homepage.html")

@login_required
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
        "oc"
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

                    tag_name = Tagname(tag=tag)
                    print("rrrrrrrrrrrrrrrrrrr")
                    artist = Posts(artist_name = artist_name,
                    artist_link=artist_link, likes = like_value,
                    elapsed_time = elapsed_time, 
                    artist_pp = artist_pp,
                    post_time = posted_on, 
                    post_link=link,
                    )
                    artist.instagram_post.save(file_name, files.File(fp))
                    # artist.instagram_post(file_name, files.File(lf))

                    
                    tag_name.register()
                    artist.register()
                    
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
    query = request.GET.get('query')
    
    if TagId:
        artists = Posts.get_all_artists_by_tagid(TagId)
    elif query:
        artists = Posts.objects.filter(artist_name__icontains=query)
    else:
        artists= Posts.get_all_artists()
    
    
    
    data = {}
    data['artists']= artists
    data['tags'] = Tags
    return render(request, 'artpage.html', data)

def about(request):
    return render(request, "about.html")
    

def adminlogin(request):
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is not None:
        return render(request, 'adminpage.html')
    
    return render(request, 'adminlogin.html')
    
    
def adminlogout(request):
    logout(request)
    return render(request, 'adminlogout.html')