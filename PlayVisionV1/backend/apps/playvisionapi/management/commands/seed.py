from django.core.management.base import BaseCommand
from faker import Faker
from apps.playvisionapi.models import Country , Season , Competition ,Team , TeamCompetitionStats , TeamInsights , Player , PlayerCompetitionStats, PlayerSeasonStats , Match , MatchEvent , MatchStats

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):

        countries = Country.objects.all().delete()
        seasons = Season.objects.all().delete()
        competitions = Competition.objects.all().delete()
        teams = Team.objects.all().delete()
        team_competition_stats = TeamCompetitionStats.objects.all().delete()
        team_insights = TeamInsights.objects.all().delete()
        players = Player.objects.all().delete()
        player_competition_stats = PlayerCompetitionStats.objects.all().delete()
        player_season_stats = PlayerSeasonStats.objects.all().delete()
        matches = Match.objects.all().delete()
        match_stats = MatchStats.objects.all().delete()
        match_events = MatchEvent.objects.all().delete()

        fake = Faker()
        
        #Example of seeding a Country model
        if Country.objects.exists():
            self.stdout.write(self.style.WARNING('Countries already seeded. Skipping.'))

        countries = ['Spain']

        for _ in countries:
            Country.objects.create(
                country_name=_,
                flag_url= fake.image_url(width=200, height=100, placeholder_url='https://via.placeholder.com/200x100')    
            )

        # Example of seeding a Season model
        if Season.objects.exists():
            self.stdout.write(self.style.WARNING('Seasons already seeded. Skipping.'))
        
        Season.objects.create(year_start='2024', year_end='2025')

        # Example of seeding a Competition model
        if not Competition.objects.exists():
            for i in range(1, 6):
                Competition.objects.create(
                    slug=fake.slug(),
                    title=fake.company(),
                    competition_type='league',
                    logo_url=fake.image_url(width=100, height=100, placeholder_url='https://via.placeholder.com/100x100'),
                    
                    country=Country.objects.first(),
                )
        else:
            self.stdout.write(self.style.WARNING('Competitions already seeded. Skipping.'))
        
        #Example of seeding Team model
        if not Team.objects.exists():
            for i in range(1, 21):
                Team.objects.create(
                    slug=fake.slug(),
                    title=fake.company(),
                    logo_url=fake.image_url(width=100, height=100, placeholder_url='https://via.placeholder.com/100x100'),
                    shortname=fake.company_suffix(),
                    stadium=fake.company(),
                    coach=fake.name(),
                    preferred_formation='4-3-3',
                )
        else:
            self.stdout.write(self.style.WARNING('Teams already seeded. Skipping.'))

        #Example of seeding TeamCompetitionStats model
        if not TeamCompetitionStats.objects.exists():
            teams = Team.objects.all()
            competitions = Competition.objects.all()
            seasons = Season.objects.all()

            for team in teams:
                TeamCompetitionStats.objects.create(
                    matches_played=fake.random_int(min=0, max=38),
                    goals_for=fake.random_int(min=0, max=100),
                    goals_against=fake.random_int(min=0, max=100),
                    goal_difference=fake.random_int(min=-50, max=50),
                    win = fake.random_int(min=0, max=38),
                    draw = fake.random_int(min=0, max=38),
                    lose = fake.random_int(min=0, max=38),
                    point = fake.random_int(min=0, max=114),
                    yellow_card = fake.random_int(min=0, max=100),
                    red_card = fake.random_int(min=0, max=20),

                    home_matches_played=fake.random_int(min=0, max=19),
                    home_win=fake.random_int(min=0, max=50),
                    home_draw=fake.random_int(min=0, max=50),
                    home_lose=fake.random_int(min=0, max=50),
                    home_goals_for=fake.random_int(min=0, max=50),
                    home_goals_against=fake.random_int(min=0, max=50),
                    home_points=fake.random_int(min=0, max=57),

                    away_matches_played=fake.random_int(min=0, max=19),
                    away_win=fake.random_int(min=0, max=50),
                    away_draw=fake.random_int(min=0, max=50),
                    away_lose=fake.random_int(min=0, max=50),
                    away_goals_for=fake.random_int(min=0, max=50),
                    away_goals_against=fake.random_int(min=0, max=50),
                    away_points=fake.random_int(min=0, max=57),

                    team=team,
                    competition=competitions.first(),
                    season=seasons.first(),
                )
        else:
            self.stdout.write(self.style.WARNING('TeamCompetitionStats already seeded. Skipping.'))

        #Example of seeding TeamInsights model
        if not TeamInsights.objects.exists():
            teams = Team.objects.all()
            seasons = Season.objects.all()
            for team in teams:
                TeamInsights.objects.create(
                    insight_type=fake.random_element(elements=('strength', 'weakness')),
                    title=fake.sentence(nb_words=6),
                    category=fake.random_element(elements=('offense', 'defense', 'mental', 'tactical','physical')),
                    description=fake.paragraph(nb_sentences=3),
                    created_at=fake.date_time_this_year(),
                    updated_at=fake.date_time_this_year(),

                    team=team,
                    season = seasons.first(),
                )
        else:
            self.stdout.write(self.style.WARNING('TeamInsights already seeded. Skipping.'))

        #Example of seeding Player model
        if not Player.objects.exists():
            teams = Team.objects.all()
            for team in teams:
                Player.objects.create(
                    slug =fake.slug(),
                    common_name=fake.name(),
                    pname=fake.first_name(),
                    lastname=fake.last_name(),
                    age =fake.random_int(min=18, max=40),
                    height =fake.random_int(min=160, max=200),
                    nationality =fake.country(),
                    nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                    position ='GK',
                    foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                    team_dorsal = fake.random_int(min=1, max=99),

                    team=team,
                )
                Player.objects.create(
                    slug =fake.slug(),
                    common_name=fake.name(),
                    pname=fake.first_name(),
                    lastname=fake.last_name(),
                    age =fake.random_int(min=18, max=40),
                    height =fake.random_int(min=160, max=200),
                    nationality =fake.country(),
                    nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                    position ='LB',
                    foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                    team_dorsal = fake.random_int(min=1, max=99),

                    team=team,
                )
                Player.objects.create(
                    slug =fake.slug(),
                    common_name=fake.name(),
                    pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='RB',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='LCB',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='RCB',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='CDB',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='RCM',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='LCM',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='DC',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='RW',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
            Player.objects.create(
                slug =fake.slug(),
                common_name=fake.name(),
                pname=fake.first_name(),
                lastname=fake.last_name(),
                age =fake.random_int(min=18, max=40),
                height =fake.random_int(min=160, max=200),
                nationality =fake.country(),
                nationality_flag =fake.image_url(width=100, height=50, placeholder_url='https://via.placeholder.com/100x50'),
                position ='LW',
                foot =fake.random_element(elements=('Left', 'Right', 'Both')),
                team_dorsal = fake.random_int(min=1, max=99),

                team=team,
            )
        else:
            self.stdout.write(self.style.WARNING('Players already seeded. Skipping.'))
        
        #Example of seeding PlayerCompetition model
        if not PlayerCompetitionStats.objects.exists():
            players = Player.objects.all()
            competitions = Competition.objects.all()
            seasons = Season.objects.all()

            for player in players:
                PlayerCompetitionStats.objects.create(
                    matches_played=fake.random_int(min=0, max=38),
                    minutes_played=fake.random_int(min=0, max=3420),
                    goals=fake.random_int(min=0, max=30),
                    head_goals=fake.random_int(min=0, max=10),
                    penalty_goals=fake.random_int(min=0, max=10),
                    freekick_goals=fake.random_int(min=0, max=10),
                    assists=fake.random_int(min=0, max=20),
                    yellow_cards=fake.random_int(min=0, max=10),
                    red_cards=fake.random_int(min=0, max=5),
                    correct_passes_media = fake.random_int(min=0, max=100),
                    tackles = fake.random_int(min=0, max=100),
                    cleansheets = fake.random_int(min=0, max=100),
                    media =fake.random_int(min=0, max=10),

                    player=player,
                    competition=competitions.first(),
                    season=seasons.first(),
                )
        else:
            self.stdout.write(self.style.WARNING('PlayerCompetitionStats already seeded. Skipping.'))
        
        #Example of seeding PlayerSeasonStats model
        if not PlayerSeasonStats.objects.exists():
            players = Player.objects.all()
            seasons = Season.objects.all()
            for player in players:
                PlayerSeasonStats.objects.create(
                    matches_played=fake.random_int(min=0, max=38),
                    minutes_played=fake.random_int(min=0, max=3420),
                    goals=fake.random_int(min=0, max=30),
                    head_goals=fake.random_int(min=0, max=10),
                    penalty_goals=fake.random_int(min=0, max=10),
                    freekick_goals=fake.random_int(min=0, max=10),
                    assists=fake.random_int(min=0, max=20),
                    yellow_cards=fake.random_int(min=0, max=10),
                    red_cards=fake.random_int(min=0, max=5),
                    tackles = fake.random_int(min=0, max=100),
                    cleansheets= fake.random_int(min=0, max=100),
                    correct_passes_media = fake.random_int(min=0, max=100),
                    recoveries_media = fake.random_int(min=0, max=100),
                    media =fake.random_int(min=0, max=10),

                    player=player,
                    team=player.team,
                    season=seasons.first(),
                )
        else:
            self.stdout.write(self.style.WARNING('PlayerSeasonStats already seeded. Skipping.'))
        
        #Example of seeding Match model
        if not Match.objects.exists():
            teams = Team.objects.all()
            competitions = Competition.objects.all()
            seasons = Season.objects.all()
            for i in range(1, 21):
                Match.objects.create(
                    match_date=fake.date_time_this_year(),
                    home_goals=fake.random_int(min=0, max=5),
                    away_goals=fake.random_int(min=0, max=5),
                    stadium=fake.company(),
                    start_time=fake.time(),
                    status='FT',
                    
                    home_team=teams.order_by('?').first(),
                    away_team=teams.order_by('?').first(),
                    competition=competitions.first(),
                    season=seasons.first(),
                )
        else:
            self.stdout.write(self.style.WARNING('Matches already seeded. Skipping.'))
        
        #Example of seeding MatchStats model
        if not MatchStats.objects.exists():
            matches = Match.objects.all()
            for match in matches:
                MatchStats.objects.create(
                    home_shots = fake.random_int(min=0, max=20),
                    home_shots_ontarget = fake.random_int(min=0, max=10),
                    home_corners = fake.random_int(min=0, max=10),
                    home_possession = fake.random_int(min=40, max=60),
                    home_fouls = fake.random_int(min=0, max=20),
                    home_yellow_cards = fake.random_int(min=0, max=5),
                    home_red_cards = fake.random_int(min=0, max=2),
                    home_offsides = fake.random_int(min=0, max=5),

                    away_shots = fake.random_int(min=0, max=20),
                    away_shots_ontarget = fake.random_int(min=0, max=10),
                    away_corners = fake.random_int(min=0, max=10),
                    away_possession = fake.random_int(min=40, max=60),
                    away_fouls = fake.random_int(min=0, max=20),
                    away_yellow_cards = fake.random_int(min=0, max=5),
                    away_red_cards = fake.random_int(min=0, max=2),
                    away_offsides = fake.random_int(min=0, max=5),

                    match=match,
                )
        else:
            self.stdout.write(self.style.WARNING('MatchStats already seeded. Skipping.'))

        #Example of seeding MatchEvent model
        if not MatchEvent.objects.exists():
            matches = Match.objects.all()
            players = Player.objects.all()
            for match in matches:
                for i in range(fake.random_int(min=1, max=8)):
                    MatchEvent.objects.create(
                        event_type=fake.random_element(elements=('Goal', 'Yellow Card', 'Red Card', 'Substitution')),
                        minute=fake.random_int(min=1, max=90),
                        description=fake.sentence(nb_words=6),

                        match=match,
                        player=players.order_by('?').first(),
                        player_assist=players.order_by('?').first() if fake.boolean(chance_of_getting_true=50) else None,
                        player_out=players.order_by('?').first() if fake.boolean(chance_of_getting_true=50) else None,
                    )
        else:
            self.stdout.write(self.style.WARNING('MatchEvents already seeded. Skipping.'))
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))