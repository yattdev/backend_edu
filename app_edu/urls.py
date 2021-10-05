#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('addvideo/', views.add_videos, name='addvideo'),
    path('add_course/', views.add_course, name='addcourse'),
    path('addpost/', views.add_post, name='addpost'),
    path('addcat/', views.add_cat, name='addcat'),
    path('allposts/', views.allposts, name='allposts'),
    path('allcat/', views.allcat, name='allcat'),
    path('allusers/', views.allusers, name='allusers'),
    path('allcourse/', views.allcourse, name='allcourses'),
    path('allorders/', views.allorders, name='allorders'),
    path('appprove_cert/<int:id>', views.approve_certificates, name='appprove_cert'),
    path('allvideos/', views.allvideos, name='allvideos'),
    path('webadmin/', views.webadmin, name='webadmin'),
    path('webadmin/addleftcat/', views.add_leftcat, name='addleftcat'),
    path('webadmin/addmiddlecat/', views.add_middlecat, name='addmiddlecat'),
    path('webadmin/addrightcat/', views.add_rightcat, name='addrightcat'),
    path('webadmin/editpost/<int:id>', views.edit_post, name='editpost'),
    path('webadmin/deletepost/<int:id>', views.delete_post, name='deletepost'),
    path('webadmin/editcat/<int:id>', views.edit_cat, name='editcat'),
    path('webadmin/editvideo/<int:id>', views.edit_videos, name='editvideo'),
    path('webadmin/deletecat/<int:id>', views.delete_cat, name='deletecat'),
    path('webadmin/deletevideo/<int:id>', views.delete_video, name='deletevideo'),
    path('webadmin/editcourse/<int:id>', views.edit_course, name='editcourse'),
    path('webadmin/deletecourse/<int:id>', views.delete_course, name='deletecourse'),
    path('webadmin/add_faq/', views.add_faq, name='add_faq'),
    path('webadmin/edit_faq/<int:id>', views.edit_faq, name='edit_faq'),
    path('webadmin/delete_faq/<int:id>', views.delete_faq, name='delete_faq'),
    path('webadmin/allfaq/', views.allfaq, name='allfaq'),
    path('webadmin/add_time/', views.add_time, name='add_time'),
    path('webadmin/edit_time/<int:id>', views.edit_time, name='edit_time'),
    path('webadmin/delete_time/<int:id>', views.delete_time, name='delete_time'),
    path('webadmin/alltime/', views.alltime, name='alltime'),
    path('webadmin/add_features/', views.add_features, name='add_features'),
    path('webadmin/edit_features/<int:id>', views.edit_features, name='edit_features'),
    path('webadmin/delete_features/<int:id>', views.delete_features, name='delete_features'),
    path('webadmin/allfeatures/', views.allfeatures, name='allfeatures'),
    path('webadmin/add_curriculam/', views.add_curriculam, name='add_curriculam'),
    path('webadmin/edit_curriculam/<int:id>', views.edit_curriculam, name='edit_curriculam'),
    path('webadmin/delete_curriculam/<int:id>', views.delete_curriculam, name='delete_curriculam'),
    path('webadmin/allcurriculam/', views.allcurriculam, name='allcurriculam'),
    path('webadmin/add_subcatg/', views.add_subcatg, name='add_subcatg'),
    path('webadmin/edit_subcatg/<int:id>', views.edit_subcatg, name='edit_subcatg'),
    path('webadmin/delete_subcatg/<int:id>', views.delete_subcatg, name='delete_subcatg'),
    path('webadmin/allsubcatg/', views.allsubcatg, name='allsubcatg'),
    path('webadmin/admin_reviews/', views.admin_reviews, name='admin_reviews'),
    path('webadmin/delete_admin_review/<int:id>', views.delete_admin_review, name='delete_admin_review'),
    path('webadmin/edit_admin_review/<int:id>', views.edit_admin_review, name='edit_admin_review'),
    path('webadmin/alladmin_review/', views.alladmin_review, name='alladmin_review'),
    path('webadmin/add_ribbon/', views.add_ribbon, name='add_ribbon'),
    path('webadmin/delete_ribbon/<int:id>', views.delete_ribbon, name='delete_ribbon'),
    path('webadmin/edit_ribbon/<int:id>', views.edit_ribbon, name='edit_ribbon'),
    path('webadmin/allribbon/', views.allribbon, name='allribbon'),
]