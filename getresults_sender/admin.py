from django.contrib import admin

from getresults.admin import admin_site

from .models import Sender, SenderPanel, SenderPanelItem, SenderModel


class SenderAdmin(admin.ModelAdmin):
    list_display = ('sender_model', 'serial_number')
    search_fields = (
        'sender_model__name', 'serial_number', 'sender_model__make',
        'sender_model__description')
admin_site.register(Sender, SenderAdmin)


class SenderInline(admin.TabularInline):
    model = Sender
    extra = 0


class SenderModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'description')
    search_fields = ('name', )
    inlines = [SenderInline, ]
admin_site.register(SenderModel, SenderModelAdmin)


class SenderPanelItemAdmin(admin.ModelAdmin):
    list_display = ('sender_panel', 'utestid')
    search_fields = ('utestid', 'sender_panel__name')
admin_site.register(SenderPanelItem, SenderPanelItemAdmin)


class SenderPanelItemInline(admin.TabularInline):
    model = SenderPanelItem
    extra = 0


class SenderPanelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    inlines = [SenderPanelItemInline]
admin_site.register(SenderPanel, SenderPanelAdmin)
