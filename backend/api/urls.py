from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainSlidingView
)
urlpatterns = [
    path("", Index.as_view(), name="IndexEndPoint"),
    # path("getAllMovies", getAllMovies.as_view()),
    # path("getMovieById", getMovieById.as_view()),
    path("getMovies",getMovies.as_view()),
    path("getMovieTrailerById", getMovieTrailerById.as_view()),
    path("getPersons", getPersons.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("tokenJWT/", TokenObtainSlidingView.as_view()),
    path("token/refresh",TokenRefreshView.as_view()),
    path("token/verify/",TokenVerifyView.as_view()),
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("checkToken", checkToken.as_view()),
    path("loadUserImage/", loadUserImage.as_view()),
    path("getUserInfo", getUserInfo.as_view()),
    path("getUserData", getUserData.as_view()),
    path("getWatched", getWatched.as_view()),
    path("addWatched/", addWatched.as_view()),
    path("removeWatched/", removeWatched.as_view()),
    path("getFavorites", getFavorites.as_view()),
    path("addFavorite/", addFavorite.as_view()),
    path("removeFavorite/", removeFavorite.as_view()),
    path("Comments", CommentController.as_view())
]
