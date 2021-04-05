from django.contrib import admin

from .models import Page, User, EmailEntry


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'url_pathname', 'title', 'sub_title', 'background_colour',)
    search_fields = ('url_pathname', 'title', 'sub_title', 'background_colour',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


@admin.register(EmailEntry)
class EmailEntryAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
