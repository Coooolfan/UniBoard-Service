from django.contrib import admin

from api.models import *


# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'profile', 'avatar', 'contacts', 'slogan', 'banner', 'name_font')
    search_fields = ('name', 'version', 'profile', 'avatar', 'contacts', 'slogan', 'banner', 'name_font')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'insert_time', 'update_time')
    search_fields = ('title', 'value', 'insert_time', 'update_time')


@admin.register(NoteFile)
class NoteFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'insert_time', 'update_time')
    search_fields = ('file', 'insert_time', 'update_time')


@admin.register(HyperLink)
class HyperLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'icon', 'color', 'desc')
    search_fields = ('title', 'url', 'icon', 'color', 'desc')


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('long_url', 'short_url', 'gmt_create', 'count')
    search_fields = ('long_url', 'short_url', 'gmt_create', 'count')


@admin.register(SysConfig)
class SysConfigAdmin(admin.ModelAdmin):
    list_display = ('host', 'show_copyright')
    search_fields = ('host', 'show_copyright')


@admin.register(FileRecord)
class FileRecordAdmin(admin.ModelAdmin):
    list_display = ('file', 'desc', 'file_name', 'share_code', 'permission', 'password', 'create_time', 'count')
    search_fields = ('file', 'desc', 'file_name', 'share_code', 'permission', 'password', 'create_time', 'count')
