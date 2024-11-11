from django.db import models
from accounts.models import PersonBase, User
from django.conf import settings


class Relative(PersonBase):
    role_choices = [
        ('Parent', 'Parent'),
        ('Sibling', 'Sibling'),
        ('Spouse', 'Spouse'),
        ('Friend', 'Friend'),
        ('Child', 'Child'),
        ('Other', 'Other')
    ]

    role = models.CharField(max_length=20, choices=role_choices, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatives')


class PlanetaryPosition(models.Model):
    planet = models.CharField(max_length=50)
    sign = models.CharField(max_length=50)
    ai_comment = models.TextField()

    def __str__(self):
        return f"{self.planet} in {self.sign}"


class ProbabilitiesComments(models.Model):
    sun_sign = models.CharField(max_length=20)
    ascendant_sign = models.CharField(max_length=20)
    daily_comment = models.TextField()
    weekly_comment = models.TextField()
    monthly_comment = models.TextField(default="default")
    yearly_comment = models.TextField()

    class Meta:
        unique_together = ('sun_sign', 'ascendant_sign')

    def __str__(self):
        return f"Probabilities for Sun: {self.sun_sign} and Ascendant: {self.ascendant_sign}"


class PersonalizedProbability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personalized_probabilities')
    probabilities_comments = models.ForeignKey(ProbabilitiesComments, on_delete=models.CASCADE, related_name='personalized_probabilities', null=True, blank=True)
    daily_comment = models.TextField()
    weekly_comment = models.TextField()
    monthly_comment = models.TextField()
    yearly_comment = models.TextField()

    def __str__(self):
        return f"Personalized probabilities for {self.user.username}"
    

class AstroFunContent(models.Model):
    sun_sign = models.CharField(max_length=20)
    ascendant_sign = models.CharField(max_length=20)
    movie_recommendation = models.TextField()
    song_recommendation = models.TextField()
    city_recommendation = models.TextField()

    class Meta:
        unique_together = ('sun_sign', 'ascendant_sign')

    def __str__(self):
        return f"AstroFun for Sun: {self.sun_sign} and Ascendant: {self.ascendant_sign}"
    

class AskAstroQuestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user.username} on {self.created_at}"
    
