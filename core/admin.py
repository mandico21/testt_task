from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    site_header = 'Панель администратора'
    site_title = 'Панель администратора'
    index_title = 'Администрирование сайтом'
