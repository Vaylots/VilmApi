from django.db import models
# Create your models here.
from django.contrib.auth.models import User as DjangoUser




class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

    def natural_key(self):
        return {"name":self.name, "id":self.id}

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

    def natural_key(self):
        return {"name":self.name, "id":self.id}

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="PersonsImages", null=True, default=None)
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField("api.Genre")
    careers = models.ManyToManyField("api.Career")
    height = models.IntegerField()
    birthday = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def natural_key(self):
        return {"name":self.name, "id":self.id}


class Career(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name 

    def natural_key(self):
        return {"name":self.name, "id":self.id}

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("api.User", on_delete=models.CASCADE)
    body = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
     
    def __str__(self) -> str:
        return f'{self.id}, {self.author}'
    
    def natural_key(self):
        return {"author":self.author.userAccount.username, "body":self.body, "publish_date":self.publish_date}


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    nameRu = models.CharField(max_length=255, blank=True)
    poster = models.FileField( upload_to="posters", null=True, default=None)
    rating = models.DecimalField(max_digits=3,decimal_places=2, null=True)
    description = models.TextField()
    year = models.IntegerField()
    country = models.ManyToManyField("api.Country")
    genre = models.ManyToManyField("api.Genre")
    filmDirector = models.ManyToManyField("api.Person", related_name="filmDirector")
    screenWriter = models.ManyToManyField("api.Person", related_name="screenWriter")
    budjet = models.CharField(max_length=15)
    moneyUsa = models.CharField(max_length=15)
    moneyTotal = models.CharField(max_length=15)
    premier = models.DateField(auto_now=False, auto_now_add=False)
    premierRu = models.DateField(auto_now=False, auto_now_add=False)
    age = models.IntegerField()
    time = models.IntegerField()
    trailer_file = models.FileField(
        upload_to="trailers", null=True, default=None)
    comment = models.ManyToManyField("api.Comment")

    def __str__(self):
        return f"{self.name} / {self.nameRu}"
    
    def natural_key(self):
        return {"nameRu":self.nameRu, "name":self.name}


class User(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField( upload_to="UserImages", null=True, default=None)
    favorites = models.ManyToManyField("api.Movie",related_name="FavoritesMovies", blank=True)
    userAccount = models.ForeignKey(DjangoUser,null=False, on_delete=models.CASCADE)
    watched = models.ManyToManyField("api.Movie",related_name="WatchedMovies", blank=True)
    birthDate = models.DateField(auto_now=False, auto_now_add=False)
    authToken = models.CharField(max_length=255,default="", null=True, blank = True)
    refreshToken = models.CharField(max_length=255,default="", null=True, blank = True)
    
    def __str__(self):
        return f"{self.userAccount.username} / {self.id}"
    
   

    
   
    
