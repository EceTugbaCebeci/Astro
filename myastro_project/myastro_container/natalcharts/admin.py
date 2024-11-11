from django.contrib import admin
from .models import Relative, PlanetaryPosition, PersonalizedProbability, ProbabilitiesComments, AstroFunContent, AskAstroQuestion

admin.site.register(Relative)
admin.site.register(PlanetaryPosition)
admin.site.register(PersonalizedProbability)
admin.site.register(ProbabilitiesComments)
admin.site.register(AstroFunContent)
admin.site.register(AskAstroQuestion)

