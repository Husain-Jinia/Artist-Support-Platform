from django.db import models
import  datetime
# Create your models here.

# class User(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=12)
#     email = models.EmailField()
#     username = models.CharField(max_length=12)
#     password = models.CharField(max_length=15)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'


#     def register(self):
#         self.save()

#     @staticmethod
#     def get_customer_by_email(email):
#         try:
#             return User.objects.get(email = email)
#         except:
#             return False

        

#     def isExists(self):
#         if User.objects.filter(email = self.email):
#             return True

#         return False
class Tagname(models.Model):
    tag = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.tag
    
    def register(self):
        self.save()
    
    @staticmethod
    def get_all_tags():
        return Tagname.objects.all()


class Posts(models.Model):
    artist_name = models.CharField(max_length=50, default="anonymous")
    artist_link = models.CharField(max_length=200,default="", null=True, blank=True)
    likes = models.CharField(max_length=50, default=0, null=True)
    elapsed_time = models.CharField(max_length=50, null=True)
    post_time = models.CharField(max_length=50, null=True)
    post_link = models.CharField(max_length=500, null=True)
    artist_pp  =models.CharField(max_length=500, null=True, default="")
    instagram_post =models.ImageField(upload_to='posts', null=True, blank=True, default="images/paper.jpg" ) 
    tagname = models.ForeignKey(Tagname, on_delete=models.CASCADE,null=True,blank=True, default="")
    # user_like = models.ManyToManyField(User, related_name='instagram_posts')

    def __str__(self):
        return f"{self.artist_name} {self.tagname}"

    def register(self):
        self.save()

    # def total_likes(self):
    #     return self.user_like.count()

    @staticmethod
    def get_all_artists():
        return Posts.objects.all()

    @staticmethod
    def get_all_artists_by_tagid(tag_id):
        if tag_id:
            return Posts.objects.filter(tagname =tag_id)

        else:
            return Posts.get_all_artists()

    @staticmethod
    def get_artists_by_id(ids):
        return Posts.objects.filter(id__in = ids)

