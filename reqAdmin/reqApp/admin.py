from django.contrib import admin
from reqApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    filter_horizontal = ("proyectos",)

class UserAdmin(AuthUserAdmin):
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups')}),
    )
    
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)

admin.site.register(Proyecto)



# custom auth permissions
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

class MyGroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group

    permissions = forms.ModelMultipleChoiceField(
        Permission.objects.filter(codename__startswith = PERM_PRE),
        widget=admin.widgets.FilteredSelectMultiple('permissions', False))


class MyGroupAdmin(admin.ModelAdmin):
    form = MyGroupAdminForm
    search_fields = ('name',)

admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)

"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from reqApp.models import UserProfile

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
"""
