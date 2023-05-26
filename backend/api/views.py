from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core import serializers
from django.conf import settings
from django.db.models import Q
from .models import Movie, Person, User
import json
from django.contrib.auth.models import User as DjangoUser

def getUserToken(id):
    userInfo = User.objects.filter(userAccount=id)
    jsonUserInfo = serializers.serialize("json", userInfo,  use_natural_foreign_keys = True )
    try:
        token = json.loads(jsonUserInfo)[0]["fields"]["authToken"]
        return token
    except Exception as e:
        return "error"

class Index(APIView):
    def get(self, request):
        return JsonResponse(
            {
                "message": "Это главный эндпоинт нашего api вот список доступных поинтов на данный момент",
                "getMovies": "Позволяет получить список одного или всех фильмов (query: id:integer)",
                "getMovieTrailerById": "Позволяет получить трейлер фильма по его id (query: id:integer) | EXPERIMENTAL ",
            }
        )


class getMovies(APIView):
    def get(self,request):
        if (request.GET.get("id")):
            movie = serializers.serialize("json",Movie.objects.filter(id=request.GET.get("id")), use_natural_foreign_keys=True)
            return HttpResponse(movie, content_type="application/json")  
        elif (request.GET.get("screenWriterId")):
            try:
                screenWriterModel = Person.objects.filter(id = request.GET.get("screenWriterId")) 
                movie = serializers.serialize("json", Movie.objects.filter( screenWriter = screenWriterModel[0]), use_natural_foreign_keys=True)
                return HttpResponse(movie, content_type="application/json")  
            except Exception as e:
                print(e)
                return JsonResponse({'message':"error"}, status=404)
        elif (request.GET.get("filmDirectorId")):
            try:
                filmDirectorModel = Person.objects.filter(id = request.GET.get("filmDirectorId")) 
                movie = serializers.serialize("json", Movie.objects.filter( filmDirector = filmDirectorModel[0]), use_natural_foreign_keys=True)
                return HttpResponse(movie, content_type="application/json")
            except Exception as e:
                print(e)
                return JsonResponse({'message':"error"}, status=404)
        elif (request.GET.get("personId")):
            try:
                PersonModel = Person.objects.filter(id = request.GET.get("personId"))
                movie = serializers.serialize("json", set(Movie.objects.filter( Q(filmDirector = request.GET.get("personId")) | Q(screenWriter = request.GET.get("personId")) )), use_natural_foreign_keys=True)
                return HttpResponse(movie, content_type="application/json")
            except Exception as e:
                print(e)
                return JsonResponse({'message':"error"}, status=404)
        else:
            movies = serializers.serialize("json",Movie.objects.all(), use_natural_foreign_keys=True)
            return HttpResponse(movies,content_type="application/json")

class getMovieTrailerById(APIView):
    def get(self, request):
        film = Movie.objects.filter(id=request.GET.get("id")).get()
        file_path = f"{settings.BASE_DIR}/{film.trailer_file.url}"
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'video/mp4'
        response['Accept-Ranges'] = 'bytes'
        if 'HTTP_RANGE' in request.headers:
            range_header = request.headers['HTTP_RANGE']
            range_values = range_header.split('=')[1].split('-')
            start = int(range_values[0])
            end = int(range_values[1]) if range_values[1] else None
            response = HttpResponse(
                response.file_to_stream(), status=206, content_type='video/mp4')
            response['Content-Range'] = f'bytes {start}-{end}/{response.file_to_stream().size}'
        return response

class getPersons(APIView):
    def get(self,request):
        
        if(request.GET.get("id")):
            person = serializers.serialize("json", Person.objects.filter(id = request.GET.get("id")), use_natural_foreign_keys=True)
            return HttpResponse(person, content_type="application/json")
        elif(request.GET.get("name")):
            person = serializers.serialize("json", Person.objects.filter(name = request.GET.get("name")), use_natural_foreign_keys=True)
        else:
            persons = serializers.serialize("json", Person.objects.all(), use_natural_foreign_keys=True)
            return HttpResponse(persons, content_type="application/json")
        


class getUserData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if(request.GET.get("id")):
            token = getUserToken(request.GET.get("id"))
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                userData = DjangoUser.objects.filter(id = request.GET.get("id"))
                response = serializers.serialize("json", userData)
                return HttpResponse(response, content_type="application/json")
            else: return JsonResponse({"status":"Error, it's not your account, or tokens expired"}, safe=False, status=401)
        else:
            return JsonResponse({"status":"Error, need a userId "}, safe=False)

class getUserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if(request.GET.get("id")):
            token = getUserToken(request.GET.get("id"))
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                userInfo = User.objects.filter(userAccount=request.GET.get("id"))
                jsonUserInfo = serializers.serialize("json", userInfo,  use_natural_foreign_keys = True )
                return HttpResponse(jsonUserInfo, content_type="application/json")
            else: return JsonResponse({"status":"Error, it's not your account, or tokens expired"}, safe=False, status=401)
        else:
            return JsonResponse({"status":"Error, need a userId "}, safe=False, status = 404)


class Register(APIView):

    def post(self,request):
        json_data = json.loads(request.body)
        try:
            userDjango = DjangoUser.objects.create_user(username=json_data["username"], password= json_data["password"])
            userDjango.save()
            user = User.objects.create(
                userAccount = userDjango,
                birthDate = json_data["birthday"]
            )
            user.save()
            return JsonResponse({"status":"success"}, safe=False)
        except Exception as e:
            DjangoUser.objects.filter(username=json_data["username"]).delete()
            print(e)
            return JsonResponse({"status":"error","message":f"{e}"}, safe=False)
    
class Login(APIView):

    def post(self,request):
        json_data = json.loads(request.body)
        try:
            user = User.objects.get(userAccount=json_data["id"])
            user.authToken = json_data["authToken"]
            user.refreshToken = json_data["refreshToken"]
            user.save()
            user = User.objects.filter(userAccount=json_data["id"])
            response = serializers.serialize("json", user,  use_natural_foreign_keys = True )
            return HttpResponse(response, content_type="application/json")
        
        except Exception as e:
            print(e)
            return JsonResponse({"status":"error","message":f"{e}"}, safe=False)

class loadUserImage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        image = request.FILES.get("image")
        id = request.POST.get("id")
        print(id)
        user = User.objects.get(userAccount = id)
        user.image = image
        user.save()
        return JsonResponse({"message":"succes"}, safe = False)


class checkToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.GET.get("id"):
            token = getUserToken(request.GET.get("id"))
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
              
                return JsonResponse({"status": "true"}, safe=False)      
            else: return JsonResponse({"status":"Error, it's not your account, or tokens expired"}, safe=False, status=401)

class getFavorites(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.GET.get("id"):
            token = getUserToken(request.GET.get("id"))
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                userInfo = User.objects.filter(userAccount=request.GET.get("id"))
                favorites_id = json.loads(serializers.serialize("json",userInfo))[0]["fields"]["favorites"]
                favorites = serializers.serialize("json", Movie.objects.filter(id__in=favorites_id), use_natural_foreign_keys = True)
                return HttpResponse(favorites, content_type="application/json")
            else: return JsonResponse({"status":"Error, it's not your account, or tokens expired"}, safe=False, status=401)
        else:
            return JsonResponse({"status":"Error, need a userId "}, safe=False, status = 404)
        



class addFavorite(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        json_data = json.loads(request.body)
        try:
            token = getUserToken(json_data["id"])
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                user = User.objects.get(userAccount = json_data["id"])
                user.favorites.add(Movie.objects.get(id=json_data["film_id"]))
                user.save()
                return JsonResponse({"message":"succes"},safe = False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":"error","message":f"{e}"}, safe=False)


class removeFavorite(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        json_data = json.loads(request.body)
        try:
            token = getUserToken(json_data["id"])
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                user = User.objects.get(userAccount = json_data["id"])
                user.favorites.remove(Movie.objects.get(id=json_data["film_id"]))
                user.save()
                return JsonResponse({"message":"succes"},safe = False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":"error","message":f"{e}"}, safe=False)

class getWatched(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.GET.get("id"):
            token = getUserToken(request.GET.get("id"))
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                userInfo = User.objects.filter(userAccount=request.GET.get("id"))
                watched_id = json.loads(serializers.serialize("json",userInfo))[0]["fields"]["watched"]
                watched = serializers.serialize("json", Movie.objects.filter(id__in=watched_id), use_natural_foreign_keys = True)
                return HttpResponse(watched, content_type="application/json")
            else: return JsonResponse({"status":"Error, it's not your account, or tokens expired"}, safe=False, status=401)
        else:
            return JsonResponse({"status":"Error, need a userId "}, safe=False, status = 404)

class addWatched(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        json_data = json.loads(request.body)
        try:
            token = getUserToken(json_data["id"])
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                user = User.objects.get(userAccount = json_data["id"])
                user.watched.add(Movie.objects.get(id=json_data["film_id"]))
                user.save()
                return JsonResponse({"message":"succes"},safe = False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":"error","message":f"{e}"}, safe=False)


class removeWatched(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        json_data = json.loads(request.body)
        try:
            token = getUserToken(json_data["id"])
            requestToken = request.headers["Authorization"].split(" ")[-1]
            if requestToken == token:
                user = User.objects.get(userAccount = json_data["id"])
                user.watched.remove(Movie.objects.get(id=json_data["film_id"]))
                user.save()
                return JsonResponse({"message":"succes"},safe = False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":"error","message":f"{e}"}, safe=False)
