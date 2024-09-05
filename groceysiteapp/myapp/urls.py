"""
URL configuration for groceysiteapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
     path("",views.index,name="index"),
     path('fb/',views.fb,name="fb"),
      path('fc/',views.fc,name="fc"),
        path('ff/',views.ff,name="ff"),
        path('foodcat/',views.foodcat,name="foodcat"),
      path('navbar/',views.navbar,name="navbar"),
        path('insert_fbought/',views.insert_fbought,
        name="insert_fbought"),


           path('insert_fconsumed/',views.insert_fconsumed,name="insert_fconsumed"),

 path('insert_food_cat/',views.insert_food_cat,name="insert_food_cat"),
           
             path('viewtables/',views.viewtables,name="viewtables"),

            #  path('', views.viewtables_exp, name="index"),

             path('deletefbitem/<int:id>',views.deletefbitem,name="deletefbitem"),

              path('deletefcitem/<int:id>',views.deletefcitem,
              name="deletefcitem"),

                 path('deletefreezeritem/<int:id>',views.deletefreezeritem,
              name="deletefreezeritem"),



              path('editfbitem/<int:id>',views.editfbitem,name="editfbitem"),




              path('editfcitem/<int:id>',views.editfcitem,name="editfcitem"),
              

              path('editfreezeritem/<int:id>',views.editfreezeritem,name="editfreezeritem"),

              
              path('updatefc/<int:id>',views.updatefcitem,name="updatefcitem")

              ,
path('updatefbitem/<int:id>', views.updatefbitem, name='updatefbitem')
              ,
              path('updatefcitem/<int:id>', views.updatefcitem, name='updatefcitem'),
              
             path('updatefreezeritem/<int:id>',views.updatefreezeritem,name="updatefreezeritem")

              ,


         path('remaining_food/', views.remaining_food, name="remaining_food"),




              path('insert_ffreeze/', views.insert_ffreeze, name='insert_ffreeze'),
     




    

]
