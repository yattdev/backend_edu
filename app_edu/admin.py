from django.contrib import admin
from .models import *
from django.utils.html import format_html
#  from django.contrib.auth.models import User

# Register your models here.


class CuricullamAdmin(admin.StackedInline):
    model = Curriculam


class featuresAdmin(admin.StackedInline):
    model = features


class faqAdmin(admin.StackedInline):
    model = faq


class timeAdmin(admin.StackedInline):
    model = timing


class CertificateAdmin(admin.StackedInline):
    model = Certificate


class videoAdmin(admin.StackedInline):
    model = video


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CuricullamAdmin, featuresAdmin, faqAdmin, timeAdmin, CertificateAdmin,
        videoAdmin
    ]

    class Meta:
        model = Post


@admin.register(Curriculam)
class CuricullamAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(MainCourse)
#  admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(Subcat)
admin.site.register(promocode)
admin.site.register(offers)
