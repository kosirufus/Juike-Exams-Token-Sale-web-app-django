from django.contrib import admin
from .models import Product, Token
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render, redirect
import csv

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'session')
    search_fields = ('name', 'session')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('code', 'product', 'assigned')
    list_filter = ('product', 'assigned')
    search_fields = ('code',)

   