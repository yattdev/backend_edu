#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from api_edu import views

urlpatterns = [
    #  Return list of categories
    path('categories/', views.CategoryList.as_view(), name="categoryList"),
    #  Get details for category identify by pk=id
    path('category/<int:pk>',
         views.CategoryDetails.as_view(),
         name="CategoryDetails"),
    # Return details of post identify by pk
    path('post/<int:pk>', views.PostDetails.as_view(), name="postDetails"),
    #  Return list of posts
    path('', views.PostList.as_view(), name="postList"),
 ]
