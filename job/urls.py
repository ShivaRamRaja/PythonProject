from .views import LoginAPIView, \
    JobPostAPIView, JobPostAPIViewOne, JobApplicationsAPIView, JobApplicationAPIView, ApplicantView, HomeAPIView, \
    LogoutAPIView
from django.urls import path, include
from rest_framework import routers


urlpatterns = [

    path("", HomeAPIView.as_view(), name="home"),
    path("login/", LoginAPIView.as_view(), name="user_login"),
    path("logout/", LogoutAPIView.as_view(), name="user_logout"),
    path("jobs/", JobPostAPIView.as_view(), name="job_post"),
    path("signup/", ApplicantView.as_view(),  name="signup"),
    path("jobs/<int:id>/", JobPostAPIViewOne.as_view(), name="job_post_one"),
    path("applications/", JobApplicationsAPIView.as_view(), name="job_applications"),
    path(r"application/", JobApplicationAPIView.as_view(), name="job_application"),
    path(r"application/<int:id>/", JobApplicationAPIView.as_view(), name="job_application"),


]
