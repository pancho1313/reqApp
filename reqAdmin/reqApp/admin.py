from django.contrib import admin
from reqApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from random import randrange
from django.contrib import messages
from django.core.mail import EmailMessage

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
    
    actions = ['reassignUserPass']
    
    def reassignUserPass(self, request, queryset):
        c = 0
        for u in queryset:
            npass = (randrange(9)+1)*1000+(randrange(9)+1)*100+(randrange(9)+1)*10+(randrange(9)+1)
            u.set_password(npass)
            message = EmailMessage('Bienvenido a MainReq!', 'Username:%s    Password:%s'%(u.username,npass), to=[u.email])
            try:
                message.send()
                messages.success(request, "password changed & sent by email (user: %s)" % u.username)
                u.save()
                c = c + 1
            except Exception, e:
                messages.error(request, "Error: can't send email! (user: %s)" % u.username)
        messages.info(request, "%s passwords changed & sent by email." % c)#warning, debug, info, success, error
        
    reassignUserPass.short_description = "Re-assign password & notify by email"
    
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
