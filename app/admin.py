from django.contrib import admin
from django.utils.html import format_html

from .models import Page, User, EmailEntry


admin.site.site_url = None


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'url_pathname', 'title', 'sub_title', 'background_colour',)
    search_fields = ('url_pathname', 'title', 'sub_title', 'background_colour',)
    readonly_fields = ('date_created', 'webpage',)

    def webpage(self, obj):
        return format_html(f'<a href="http://localhost:8000/{obj.url_pathname}" '
                           f'target="_blank" rel="noopener noreferrer">Your Web Page</a>')
    webpage.allow_tags = True

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)

    def has_module_permission(self, request):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset


@admin.register(EmailEntry)
class EmailEntryAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added',)
    search_fields = ('email',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)

    def has_module_permission(self, request):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(page__user=request.user)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.readonly_fields = ('email', 'date_added',)
            self.exclude = ('page',)
        return super(EmailEntryAdmin, self).get_form(request, obj, **kwargs)
