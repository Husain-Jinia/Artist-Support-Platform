from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import Posts
import re
import os
from .models import Tagname
import requests
from django.core import files
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.urls import reverse_lazy, reverse
from .credentials import my_username, my_password
from django.core.checks.messages import Error
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.hashers import  check_password, make_password
from .models import User
from django.views import View

# home view
def home(request):
    return render(request, "homepage.html")

#scraper
def scrape(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    browser.get("https://www.instagram.com/?hl=en")

    time.sleep(2)

    username = browser.find_element_by_css_selector("[name='username']")

    password = browser.find_element_by_css_selector("[name='password']")

    login = browser.find_element_by_css_selector("button")

    username.send_keys(my_username)

    password.send_keys(my_password)

    login.click()

    time.sleep(5)


    tags=[]
    tags = request.GET.get('hashtag')
    tags = tags.split(",")


    tag_counter = 0
    while True:

        for tag in tags:
            sleepy_time = 5
            url= f"https://www.instagram.com/explore/tags/{tag}"
            browser.get(url)

            time.sleep(10)

            browser.execute_script("window.scrollTo(0, 2000);")
            pictures = browser.find_elements_by_css_selector("div[class='eLAPa']")

            total_image_count = 0

            artist_post = browser.find_elements_by_class_name("FFVAD")

            print(artist_post)
            post_counter=0
            for picture in pictures:

                if total_image_count == 6:
                    break

                picture.click()

                time.sleep(6)
                
                #getting likes value
                like = browser.find_element_by_partial_link_text("like")
                like_value = like.text
                like_value = re.split("\s", like_value)
                like_value = like_value[0]
                like_value = re.sub(",","",like_value)
                like_value = int(like_value)
                print(like_value)

                #getting the time it was posted on
                posted_on = browser.find_element_by_class_name("Nzb55").get_attribute("title")
                elapsed_time = browser.find_element_by_class_name("Nzb55").text
                elapsed_time = re.split("\s", elapsed_time)
                elapsed_time = elapsed_time[0]

                #getting the name and link of the artist
                artist_name = browser.find_element_by_class_name("yWX7d").text
                artist_link = browser.find_element_by_class_name("yWX7d").get_attribute("href")
                
                artist_pp = browser.find_element_by_class_name("_6q-tv").get_attribute("src")

                #saving image
                link = artist_post[post_counter].get_attribute("src")
                post_counter=post_counter+1
                resp = requests.get(link)
                fp = BytesIO()
                fp.write(resp.content)
                file_name = f"{artist_name}.jpg"  

                close = browser.find_element_by_css_selector("[aria-label='Close']")

                close.click()

                if int(like_value)<=5000:
                    if not Tagname.objects.filter(tag__icontains=tag):

                        tag_name = Tagname(tag=tag)
                        tag_name.register()
                        artist = Posts(artist_name = artist_name,
                        artist_link=artist_link, likes = like_value,
                        elapsed_time = elapsed_time, 
                        artist_pp = artist_pp,
                        post_time = posted_on, 
                        post_link=link,
                        )
                    else:
                        artist = Posts(artist_name = artist_name,
                        artist_link=artist_link, likes = like_value,
                        elapsed_time = elapsed_time, 
                        artist_pp = artist_pp,
                        post_time = posted_on, 
                        post_link=link,
                        )
                    artist.instagram_post.save(file_name, files.File(fp))
                    
                    
                    artist.register()

                time.sleep(3)
        
                total_image_count+=1
            
        time.sleep(10)

        return redirect("adminpage")

#explore page view
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

    stuff = get_object_or_404(Posts)
    total_likes = stuff.total_likes()
    data = {}
    data['total likes']= total_likes
    data['artists']= artists
    data['tags'] = Tags
    return render(request, 'artpage.html', data)

#about page view
def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request,'contactus.html')

#admin page view
@login_required
def adminpage(request):
    return render(request, "adminpage.html")
    
#admin login view
def adminlogin(request):
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is not None:
        return render(request, 'adminpage.html')
    
    return render(request, 'adminlogin.html')
    
#admin logout view  
def adminlogout(request):
    logout(request)
    return render(request, 'adminlogout.html')


#user login
class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = User.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or password invalid !!'
        else:
            error_message = 'Email or password invalid !!'

        return render(request, 'login.html', {'error': error_message})

        
        
def logout(request):
    request.session.clear()
    return redirect('login')

#user signup
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone_number = postData.get('phone_number')
        email = postData.get('email')
        password = postData.get('password')

        #validation
        value ={
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email
        }
        error_message = None

        customer = User(first_name=first_name,
                                last_name=last_name,
                                phone_number = phone_number,
                                email= email,
                                password=password)

        error_message = self.validateCustomer(customer)

        
        
        
        print(first_name, last_name, phone_number, email, password)
        
            
        
        if not error_message:
            

            customer.password = make_password(customer.password)
            customer.register()

            return redirect('homepage')
        else:
            data ={
                'error': error_message,
                'values' : value
            }
            return render(request, 'signup.html', data )

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message= "First name required"
        elif len(customer.first_name) < 4:
            error_message = "First Name must be 4 character long or more"
        elif not customer.last_name:
            error_message="Last name required"
        elif len(customer.last_name) < 4 :
            error_message="last name must be atleast 4 characters"
        elif not customer.phone_number:
            error_message="Phone number is required"
        elif len(customer.phone_number) > 10:
            error_message= "phone number should not exceed 10 characters"
        elif len(customer.password) < 6:
            error_message = "Password must be atleast 6 character long"
        elif len(customer.email) < 5:
            error_message = "Email must be atleast 5 character long"
        elif customer.isExists():
            error_message = 'Email Address already registered . . '
            
        return error_message

def LikeView(request, pk):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    post.user_like.add(request.customer)
    return HttpResponseRedirect(reverse('artpage',args=[str(pk)]))

