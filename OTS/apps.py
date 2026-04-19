from django.apps import AppConfig


class OtsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OTS'

    def ready(self):
        from django.contrib import admin
        admin.site.site_header = "OTS — Admin Panel"
        admin.site.site_title  = "Online Testing System"
        admin.site.index_title = "Welcome, Teacher 👋"
