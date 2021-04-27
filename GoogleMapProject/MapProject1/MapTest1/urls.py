from django.urls import  path
from  .views import calculate_distance_view

app_name='MapTest1'

urlpatterns=[
    path('',calculate_distance_view)

]