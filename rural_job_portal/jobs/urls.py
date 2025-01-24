# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('jobs/<int:job_id>/applications/', views.manage_job_applications, name='manage_job_applications'),
    path('explore-schemes/', views.explore_schemes, name='explore_schemes'),
]
