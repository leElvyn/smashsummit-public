from django.db import models

# Create your models here.

class Member(models.Model):
    last_known_name = models.CharField(verbose_name="Nom" , max_length=200)
    tournaments = models.IntegerField(default=0)
    points = models.IntegerField(default=1000)
    points_float = models.FloatField(default=1000)
    sigma = models.FloatField(null=True, blank=True)
    previous_sigma = models.FloatField(null=True, blank=True)
    previous_points_float = models.FloatField(null=True, blank=True)
    user_id = models.BigIntegerField(verbose_name="ID discord", primary_key=True)
    PP_link = models.CharField(verbose_name="lien de la PP", max_length=1000, default="https://cdn.discordapp.com/embed/avatars/1.png")
    team = models.ForeignKey("Teams", verbose_name=("Équipe"), on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    member_badges = models.ManyToManyField("Badge", verbose_name="Badges", blank=True)
    did_tournament = models.BooleanField(default=False)
    #if the member already did a tournament today
    is_winning = models.BooleanField(null=True, blank=True)

    def get_team_short(self):
        team = self.team
        return team.short_name
    
    def write_round(self, rate):
        self.points = int(rate.mu)
        self.points_float = rate.mu
        self.sigma = rate.sigma
        self.save()

    def write_previous(self):
        self.previous_sigma = self.sigma
        self.previous_points_float = self.points_float
        self.save()

    def rollback(self):
        self.sigma = self.previous_sigma
        self.points_float = self.previous_points_float
        self.points = int(self.points_float)
        team = self.team
        team.rollback()
        self.save()

    def __str__(self):
        return self.last_known_name

class Badge(models.Model):
    name = models.CharField("Nom du badge", max_length=50)
    tooltip = models.CharField(max_length=100)
    svg = models.TextField("modèle", blank=True)

    class Meta:
        verbose_name = ("Badges")
        verbose_name_plural = ("Badges")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Badges_detail", kwargs={"pk": self.pk})

    

class Teams(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=4)
    team_points = models.IntegerField(default=1000)
    points_float = models.FloatField(default=1000)
    sigma = models.FloatField(null=True, blank=True)
    previous_sigma = models.FloatField(null=True, blank=True)
    previous_points_float = models.FloatField(null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    role = models.BigIntegerField()

    def __str__(self):
        return self.name

    def write_round(self, rate):
        self.team_points = int(rate.mu)
        self.points_float = rate.mu
        self.sigma = rate.sigma
        self.save()
    
    def write_previous(self):
        self.previous_sigma = self.sigma
        self.previous_points_float = self.points_float
        self.save()

    def rollback(self):
        self.sigma = self.previous_sigma
        self.points_float = self.previous_points_float
        self.points = int(self.points_float)
        self.save()

class Match(models.Model):
    class matchTypes(models.IntegerChoices):
        Freeplay = 1
        Tournament = 2
        Inter_team = 3

    winner = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="%(class)s_winner")
    loser = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="%(class)s_loser")
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()
    match_type = models.IntegerField(choices=matchTypes.choices)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
        
'''
class ScoreState(models.model):
    #todo
    new_points_float = models.FloatField(default=1000)
    sigma = models.FloatField(null=True, blank=True)
    previous_sigma = models.FloatField(null=True, blank=True)
    previous_points_float = models.FloatField(null=True, blank=True)
'''
