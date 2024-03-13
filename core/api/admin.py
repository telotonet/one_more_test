from django.contrib import admin
from .models import Organization, Event
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models


# Organizations admin

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address', 'postcode')
    search_fields = ('title', 'description', 'address', 'postcode')
    list_filter = ('members', 'postcode')


admin.site.register(Organization, OrganizationAdmin)    


# Events admin

class CustomAdminFileWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        if value:
            if hasattr(value, "url"):
                result.append(
                    f'''<a href="{value.url}" target="_blank">
                        '<img src="{value.url}" alt="{value}"  width="100" height="auto" />'
                        </a>'''
                )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))

class EventAdmin(admin.ModelAdmin):
    list_display = ('get_image_preview', 'title', 'description', 'get_organizations', 'date')
    search_fields = ('title', 'description', 'date')
    filter_horizontal = ('organizations',)
    list_filter = ('organizations', 'date')
    
    formfield_overrides = { 
        models.ImageField: {"widget": CustomAdminFileWidget}
    }

    def get_organizations(self, obj):
        return ", ".join([org.title for org in obj.organizations.all()])
    get_organizations.short_description = 'Organizations'

    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{url}" width="100" height="auto" />'.format(url=obj.image.url))
        else:
            return '(No image)'
    get_image_preview.short_description = 'Image Preview'

admin.site.register(Event, EventAdmin)