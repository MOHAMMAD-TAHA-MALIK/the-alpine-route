from django.contrib import admin
from .models import Trek, TrekEvent, Comment, TrekImage, TrekEventImage


class TrekImageInline(admin.TabularInline):
    model = TrekImage
    extra = 1


class TrekEventImageInline(admin.TabularInline):
    model = TrekEventImage
    extra = 1


@admin.register(Trek)
class TrekAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'date', 'difficulty', 'created_by')
    list_filter = ('difficulty', 'date')
    search_fields = ('title', 'destination')
    inlines = [TrekImageInline]


@admin.register(TrekEvent)
class TrekEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'date', 'created_at')
    list_filter = ('date',)
    search_fields = ('title', 'destination')
    inlines = [TrekEventImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Fixed: Replaced 'event' with 'trek' to match your Comment model field
    list_display = ('user', 'trek', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')