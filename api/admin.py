from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from api.models import *


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'role',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'full_name',
            'role',
            'department',
            'phone',
            'avatar'
        )

    def clean_password(self):
        return self.initial['password']


class TaskStatusInline(admin.TabularInline):
    model = TaskStatus


class AchievementsInline(admin.TabularInline):
    model = Achievement


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'full_name')
    list_filter = ('role',)
    inlines = [TaskStatusInline]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Пользователь', {'fields': ('full_name', 'role', 'phone')}),
        ('Общее', {'fields': ('department', 'avatar')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskStatusInline]
    fieldsets = [
        (None, {'fields': ('name', 'desc', 'type')}),
        ('Other', {'fields': ('total_count', 'experience', 'price', 'achievements', 'pic')}),
        ('Timestamps', {'fields': ('start_timestamp', 'end_timestamp')})
    ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Achievement)
admin.site.register(Request)
admin.site.register(Task, TaskAdmin)
admin.site.register(Level)
admin.site.register(Department)
