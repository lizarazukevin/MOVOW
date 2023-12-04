from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(People)
admin.site.register(PeopleAliases)
admin.site.register(Genres)
admin.site.register(Providers)
admin.site.register(Regions)
admin.site.register(Movies)
admin.site.register(MovieCastingCredits)
admin.site.register(MovieCrewCredits)
admin.site.register(Shows)
admin.site.register(ShowCastingCredits)
admin.site.register(ShowCrewCredits)
admin.site.register(Seasons)
