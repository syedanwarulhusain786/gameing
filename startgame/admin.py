from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GameData

admin.site.register(GameData)


from django.contrib import admin
from .forms import UserCreateForm
from django.contrib.auth.models import User

class CustomUserAdmin(admin.ModelAdmin):
    form = UserCreateForm

    def add_view(self, request, form_url='', extra_context=None):
        self.form = self.get_form(request)
        return super().add_view(request, form_url, extra_context)

admin.site.unregister(GameData)
admin.site.register(GameData, CustomUserAdmin)
