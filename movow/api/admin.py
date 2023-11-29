from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Movies)
admin.site.register(Genres)
admin.site.register(People)
admin.site.register(PeopleAliases)
admin.site.register(MovieCastingCredits)
