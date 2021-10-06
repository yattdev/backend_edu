#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app_edu import models
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """ Serialize Category Models from app_edu """
    class Meta:
        model = models.Category
        # return all field in models
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """ Serialize Post Models from app_edu """

    class Meta:
        model = models.Post
        # return all field in models
        fields = '__all__'

