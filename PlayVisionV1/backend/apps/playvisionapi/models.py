from django.db import models
from django.utils.text import slugify

# Create your models here.
    
class Competition(models.Model):
    slug = models.SlugField(max_length=150,unique=True,blank=True)
    title = models.CharField(max_length=100)
    competition_type = models.CharField(max_length=100)
    logo_url = models.ImageField(upload_to="competitionlogo/")

    country = models.ForeignKey("Country",related_name="competition_country",on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}")
            slug = base_slug
            counter = 1
            while Competition.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Season(models.Model):
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    
    def __str__(self):
        return f"{self.year_start}-{self.year_end}"

class Team(models.Model):
    slug = models.SlugField(max_length=150,unique=True,blank=True)
    title = models.CharField(max_length=200)
    logo_url = models.ImageField(upload_to="teamlogos/")
    shortname = models.CharField(max_length=200,default="URL")
    stadium = models.CharField(max_length=200, null=True)
    coach = models.CharField(max_length=200, null=True)
    preferred_formation = models.CharField(max_length=100,null=True, default="4-3-3")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}")
            slug = base_slug
            counter = 1
            while Team.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class TeamCompetitionStats(models.Model):
    matches_played = models.IntegerField()
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    goal_difference = models.IntegerField(default=0)
    win = models.IntegerField()
    draw = models.IntegerField()
    lose = models.IntegerField()
    point = models.IntegerField()
    yellow_card = models.IntegerField()
    red_card = models.IntegerField()

    home_matches_played = models.IntegerField()
    home_win = models.IntegerField()
    home_draw = models.IntegerField()
    home_lose = models.IntegerField()
    home_goals_for = models.IntegerField()
    home_goals_against = models.IntegerField()
    home_points = models.IntegerField()

    away_matches_played = models.IntegerField()
    away_win = models.IntegerField()
    away_draw = models.IntegerField()
    away_lose = models.IntegerField()
    away_goals_for = models.IntegerField()
    away_goals_against = models.IntegerField()
    away_points = models.IntegerField()

    team = models.ForeignKey(Team,related_name="team_stats", on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition,related_name="team_competition_stats", on_delete=models.CASCADE)
    season = models.ForeignKey(Season,related_name="team_season_stats", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["team","competition","season"],name="unique_team_competition_season")
        ]

class InsightType(models.TextChoices):
    STRENGTH = "strength", "Strength"
    WEAKNESS = "weakness", "Weakness"

class InsightCategory(models.TextChoices):
    OFFENSE = "offense", "Offense"
    DEFENSE = "defense", "Defense"
    TACTICAL = "tactical", "Tactical"
    PHYSICAL = "physical", "Physical"
    MENTAL = "mental", "Mental"

class TeamInsights(models.Model):
    insight_type = models.CharField(max_length=20, choices=InsightType.choices)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=InsightCategory.choices)
    description = models.TextField(
        help_text="Detailed explanation of the insight."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(Team, related_name="team_insights", on_delete=models.CASCADE)
    season = models.ForeignKey(Season, related_name="season_team_insights", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.team.title} - {self.insight_type} - {self.title}"

class PlayerPosition(models.TextChoices):
    GK = "GK", "Goalkeeper"
    LB = "LB", "Left Back"
    LCB = "LCB", "Left Center Back"
    RCB = "RCB", "Right Center Back"
    RB = "RB", "Right Back"
    CDM = "CDM", "Central Defensive Midfielder"
    LCM = "LCM", "Left Center Midfielder"
    CM = "CM", "Central Midfielder"
    RCM = "RCM", "Right Center Midfielder"
    MP = "MP", "Midfielder Playmaker"
    LM = "LM", "Left Midfielder"
    RM = "RM", "Right Midfielder"
    CAM = "CAM", "Central Attacking Midfielder"
    LW = "LW", "Left Winger"
    RW = "RW", "Right Winger"
    DC = "DC", "Center Striker"
    SS = "SS", "Second Striker"

class Player(models.Model):
    slug = models.SlugField(max_length=150,unique=True,blank=True)
    common_name = models.CharField(max_length=100,null=True)
    pname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.DecimalField(decimal_places=2,max_digits=5,null=True,default=0)
    nationality = models.CharField(max_length=100)
    nationality_flag = models.ImageField(upload_to="flags/")
    position = models.CharField(max_length=100,choices=PlayerPosition.choices, default=PlayerPosition.CM)
    foot = models.CharField(max_length=100)
    team_dorsal = models.IntegerField()
    
    team = models.ForeignKey(Team,related_name="team_players",on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id","team"],name="unique_id_player_team")
        ]
    def __str__(self):
        return self.pname
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.pname} {self.lastname}")
            slug = base_slug
            counter = 1
            while Player.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
class PlayerCompetitionStats(models.Model):
    matches_played = models.IntegerField()
    minutes_played = models.IntegerField()
    goals = models.IntegerField()
    head_goals = models.IntegerField()
    penalty_goals = models.IntegerField()
    freekick_goals = models.IntegerField()
    assists = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    correct_passes_media= models.DecimalField(decimal_places=2,max_digits=5)
    tackles = models.IntegerField()
    cleansheets = models.IntegerField()
    media = models.DecimalField(decimal_places=2,max_digits=5)

    player = models.ForeignKey(Player,related_name="player_competition_stats",on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition,related_name="player_competition_stats",on_delete=models.CASCADE)
    season = models.ForeignKey(Season,related_name="player_competition_stats",on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["player","competition","season"],name="unique_player_competition_stats")
        ]

class PlayerSeasonStats(models.Model):
    matches_played = models.IntegerField()
    minutes_played = models.IntegerField()
    goals = models.IntegerField()
    head_goals = models.IntegerField()
    penalty_goals = models.IntegerField()
    freekick_goals = models.IntegerField()
    assists = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    tackles = models.IntegerField()
    cleansheets = models.IntegerField()
    correct_passes_media= models.DecimalField(decimal_places=2,max_digits=5)
    recoveries_media = models.DecimalField(decimal_places=2,max_digits=5)
    media = models.DecimalField(decimal_places=2,max_digits=5)

    player = models.ForeignKey(Player,related_name="player_season_stats",on_delete=models.CASCADE)
    team = models.ForeignKey(Team,related_name="player_team_season_stats",on_delete=models.CASCADE)
    season = models.ForeignKey(Season,related_name="player_season",on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["player","team","season"],name="unique_player_season_stats")
        ]

class MatchStatus(models.TextChoices):
    NOT_STARTED = "NP", "Not Started"
    PLAYING = "P" , "Playing"
    FINISHED = "FT" , "Finished"

class Match(models.Model):
    match_date = models.DateField()
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    stadium = models.CharField(max_length=100, null=True)
    start_time = models.TimeField()
    status = models.CharField(max_length=30,choices=MatchStatus.choices,default=MatchStatus.NOT_STARTED)
    round = models.CharField(null=True,default="none")
    description = models.CharField(null=True,default="none")

    home_team = models.ForeignKey(Team,related_name="home_team_match",on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team,related_name="away_team_match",on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition,related_name="match_competition",on_delete=models.CASCADE)
    season = models.ForeignKey(Season,related_name="season_match",on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["home_team","away_team","competition","season"],name="unique_match_competition_season")
        ]


class MatchStats(models.Model):
    home_shots = models.IntegerField(default=0)
    home_shots_ontarget = models.IntegerField(default=0)
    home_corners = models.IntegerField(default=0)
    home_possession = models.IntegerField(default=0)
    home_passes = models.IntegerField(default=0)
    home_fouls = models.IntegerField(default=0)
    home_yellow_cards = models.IntegerField(default=0)
    home_red_cards = models.IntegerField(default=0)
    home_offsides = models.IntegerField(default=0)
    
    away_shots = models.IntegerField(default=0)
    away_shots_ontarget = models.IntegerField(default=0)
    away_corners = models.IntegerField(default=0)
    away_possession = models.IntegerField(default=0)
    away_passes = models.IntegerField(default=0)
    away_fouls = models.IntegerField(default=0)
    away_yellow_cards = models.IntegerField(default=0)
    away_red_cards = models.IntegerField(default=0)
    away_offsides = models.IntegerField(default=0)

    match = models.ForeignKey(Match,related_name="match_stats",on_delete=models.CASCADE)

class MatchEventType(models.TextChoices):
    GOAL = "GOAL", "Goal"
    YELLOW_CARD = "YELLOW_CARD", "Yellow Card"
    RED_CARD = "RED_CARD", "Red Card"
    SUBSTITUTION = "SUBSTITUTION", "Substitution"


class MatchEvent(models.Model):
    event_type = models.CharField(max_length=100 , choices=MatchEventType.choices)
    minute = models.IntegerField()
    description = models.CharField(max_length=200,null=True)

    match = models.ForeignKey(Match,related_name="match_events",on_delete=models.CASCADE)
    player = models.ForeignKey(Player,related_name="player_events",on_delete=models.CASCADE)
    player_assist = models.ForeignKey(Player,related_name="assist_events",on_delete=models.CASCADE,null=True,blank=True)
    player_out = models.ForeignKey(Player,related_name="player_out_events",on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id","match","player"],name="unique_match_event_player")
        ]

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    flag_url = models.ImageField(upload_to="countryflags/")

    def __str__(self):
        return self.country_name