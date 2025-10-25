#!/usr/bin/env python3
"""
Real-time Sports Score Display for 32x128 RGB LED Matrix
Displays scores from MLB, NFL, NBA, NCAA Football, NCAA Basketball, and NCAA Baseball
Prioritizes Houston Astros and Arkansas Razorbacks with live score tracking
Version 2.0 - Team Colors Edition
"""

import time
import requests
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from config import *

class SportsScoreDisplay:
    def __init__(self):
        # Configure the matrix from config.py
        options = RGBMatrixOptions()
        options.rows = MATRIX_HEIGHT
        options.cols = MATRIX_WIDTH
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = MATRIX_HARDWARE_MAPPING
        options.gpio_slowdown = MATRIX_GPIO_SLOWDOWN
        
        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()
        
        # Load fonts from config
        self.font_large = graphics.Font()
        self.font_large.LoadFont(FONT_LARGE)
        
        self.font_small = graphics.Font()
        self.font_small.LoadFont(FONT_SMALL)
        
        # Colors
        self.white = graphics.Color(255, 255, 255)
        self.green = graphics.Color(0, 255, 0)
        self.red = graphics.Color(255, 0, 0)
        self.blue = graphics.Color(0, 150, 255)
        self.yellow = graphics.Color(255, 255, 0)
        self.orange = graphics.Color(255, 165, 0)
        self.priority_color = graphics.Color(255, 0, 255)  # Magenta for priority teams
        
        # Team colors database (RGB values)
        self.team_colors = {
            # MLB
            'HOU': graphics.Color(235, 110, 37),   # Astros Orange
            'NYY': graphics.Color(19, 39, 79),      # Yankees Navy
            'BOS': graphics.Color(189, 48, 57),     # Red Sox Red
            'LAD': graphics.Color(0, 90, 156),      # Dodgers Blue
            'ATL': graphics.Color(206, 17, 65),     # Braves Red
            'CHC': graphics.Color(14, 51, 134),     # Cubs Blue
            'STL': graphics.Color(196, 30, 58),     # Cardinals Red
            'SF': graphics.Color(253, 90, 30),      # Giants Orange
            'LAA': graphics.Color(186, 0, 33),      # Angels Red
            'SD': graphics.Color(47, 36, 29),       # Padres Brown
            'TEX': graphics.Color(0, 50, 120),      # Rangers Blue
            'MIA': graphics.Color(0, 163, 224),     # Marlins Blue
            'NYM': graphics.Color(0, 45, 114),      # Mets Blue
            'PHI': graphics.Color(232, 24, 40),     # Phillies Red
            'WSH': graphics.Color(171, 0, 3),       # Nationals Red
            'TB': graphics.Color(9, 44, 92),        # Rays Navy
            'TOR': graphics.Color(19, 74, 142),     # Blue Jays Blue
            'BAL': graphics.Color(223, 70, 1),      # Orioles Orange
            'CLE': graphics.Color(0, 56, 93),       # Guardians Navy
            'DET': graphics.Color(12, 35, 64),      # Tigers Navy
            'KC': graphics.Color(0, 70, 135),       # Royals Blue
            'MIN': graphics.Color(0, 43, 92),       # Twins Navy
            'CWS': graphics.Color(39, 37, 31),      # White Sox Black
            'OAK': graphics.Color(0, 56, 49),       # Athletics Green
            'SEA': graphics.Color(12, 44, 86),      # Mariners Navy
            'MIL': graphics.Color(18, 40, 75),      # Brewers Navy
            'PIT': graphics.Color(39, 37, 31),      # Pirates Black
            'CIN': graphics.Color(198, 1, 31),      # Reds Red
            'COL': graphics.Color(51, 0, 111),      # Rockies Purple
            'ARI': graphics.Color(167, 25, 48),     # Diamondbacks Red
            
            # NFL
            'KC': graphics.Color(227, 24, 55),      # Chiefs Red
            'BUF': graphics.Color(0, 51, 141),      # Bills Royal Blue
            'DAL': graphics.Color(0, 34, 68),       # Cowboys Navy
            'GB': graphics.Color(24, 48, 40),       # Packers Green
            'NE': graphics.Color(0, 34, 68),        # Patriots Navy
            'SF': graphics.Color(170, 0, 0),        # 49ers Red
            'PHI': graphics.Color(0, 76, 84),       # Eagles Green
            'PIT': graphics.Color(255, 182, 18),    # Steelers Gold
            'BAL': graphics.Color(26, 25, 95),      # Ravens Purple
            'MIN': graphics.Color(79, 38, 131),     # Vikings Purple
            'LAR': graphics.Color(0, 53, 148),      # Rams Blue
            'LAC': graphics.Color(0, 128, 198),     # Chargers Blue
            'MIA': graphics.Color(0, 142, 151),     # Dolphins Aqua
            'CIN': graphics.Color(251, 79, 20),     # Bengals Orange
            'DEN': graphics.Color(251, 79, 20),     # Broncos Orange
            'SEA': graphics.Color(0, 34, 68),       # Seahawks Navy
            'ATL': graphics.Color(167, 25, 48),     # Falcons Red
            'NO': graphics.Color(211, 188, 141),    # Saints Gold
            'TB': graphics.Color(213, 10, 10),      # Buccaneers Red
            'CAR': graphics.Color(0, 133, 202),     # Panthers Blue
            'CHI': graphics.Color(11, 22, 42),      # Bears Navy
            'DET': graphics.Color(0, 118, 182),     # Lions Blue
            'NYG': graphics.Color(1, 35, 82),       # Giants Blue
            'NYJ': graphics.Color(18, 87, 64),      # Jets Green
            'WAS': graphics.Color(90, 20, 20),      # Commanders Burgundy
            'CLE': graphics.Color(49, 29, 0),       # Browns Brown
            'TEN': graphics.Color(12, 35, 64),      # Titans Navy
            'JAX': graphics.Color(0, 103, 120),     # Jaguars Teal
            'IND': graphics.Color(0, 44, 95),       # Colts Blue
            'HOU': graphics.Color(3, 32, 47),       # Texans Navy
            'LV': graphics.Color(0, 0, 0),          # Raiders Black
            'ARI': graphics.Color(151, 35, 63),     # Cardinals Red
            
            # NBA
            'LAL': graphics.Color(85, 37, 130),     # Lakers Purple
            'BOS': graphics.Color(0, 122, 51),      # Celtics Green
            'GSW': graphics.Color(29, 66, 138),     # Warriors Blue
            'MIA': graphics.Color(152, 0, 46),      # Heat Red
            'CHI': graphics.Color(206, 17, 65),     # Bulls Red
            'NYK': graphics.Color(0, 107, 182),     # Knicks Blue
            'BKN': graphics.Color(0, 0, 0),         # Nets Black
            'PHI': graphics.Color(0, 107, 182),     # 76ers Blue
            'TOR': graphics.Color(206, 17, 65),     # Raptors Red
            'MIL': graphics.Color(0, 71, 27),       # Bucks Green
            'CLE': graphics.Color(134, 0, 56),      # Cavaliers Wine
            'IND': graphics.Color(0, 45, 98),       # Pacers Navy
            'DET': graphics.Color(200, 16, 46),     # Pistons Red
            'ATL': graphics.Color(225, 68, 52),     # Hawks Red
            'CHO': graphics.Color(29, 17, 96),      # Hornets Purple
            'WAS': graphics.Color(0, 43, 92),       # Wizards Navy
            'ORL': graphics.Color(0, 125, 197),     # Magic Blue
            'DEN': graphics.Color(13, 34, 64),      # Nuggets Navy
            'UTA': graphics.Color(0, 43, 92),       # Jazz Navy
            'POR': graphics.Color(224, 58, 62),     # Trail Blazers Red
            'OKC': graphics.Color(0, 125, 195),     # Thunder Blue
            'MIN': graphics.Color(12, 35, 64),      # Timberwolves Navy
            'PHX': graphics.Color(29, 17, 96),      # Suns Purple
            'LAC': graphics.Color(200, 16, 46),     # Clippers Red
            'SAC': graphics.Color(91, 43, 130),     # Kings Purple
            'DAL': graphics.Color(0, 83, 188),      # Mavericks Blue
            'HOU': graphics.Color(206, 17, 65),     # Rockets Red
            'SAS': graphics.Color(196, 206, 211),   # Spurs Silver
            'NOP': graphics.Color(0, 22, 65),       # Pelicans Navy
            'MEM': graphics.Color(93, 118, 169),    # Grizzlies Blue
            
            # College - Arkansas
            'ARK': graphics.Color(157, 34, 53),     # Razorbacks Cardinal
            
            # College - SEC
            'ALA': graphics.Color(158, 27, 50),     # Alabama Crimson
            'UGA': graphics.Color(186, 12, 47),     # Georgia Red
            'LSU': graphics.Color(70, 29, 124),     # LSU Purple
            'TENN': graphics.Color(255, 130, 0),    # Tennessee Orange
            'FLA': graphics.Color(0, 33, 165),      # Florida Blue
            'TEX': graphics.Color(191, 87, 0),      # Texas Burnt Orange
            'OKLA': graphics.Color(132, 17, 31),    # Oklahoma Crimson
            'MISS': graphics.Color(14, 35, 86),     # Ole Miss Navy
            'MSST': graphics.Color(102, 0, 0),      # Mississippi State Maroon
            'TAMU': graphics.Color(80, 0, 0),       # Texas A&M Maroon
            'AU': graphics.Color(12, 35, 64),       # Auburn Navy
            'MO': graphics.Color(241, 184, 45),     # Missouri Gold
            'SC': graphics.Color(115, 0, 10),       # South Carolina Garnet
            'UK': graphics.Color(0, 51, 160),       # Kentucky Blue
            'VAN': graphics.Color(134, 109, 75),    # Vanderbilt Gold
            
            # College - Big Ten
            'OSU': graphics.Color(187, 0, 0),       # Ohio State Scarlet
            'MICH': graphics.Color(0, 39, 76),      # Michigan Blue
            'PSU': graphics.Color(4, 30, 66),       # Penn State Navy
            'WIS': graphics.Color(197, 5, 12),      # Wisconsin Red
            'NEB': graphics.Color(208, 0, 0),       # Nebraska Red
            'IOWA': graphics.Color(255, 205, 0),    # Iowa Gold
            'MSU': graphics.Color(24, 69, 59),      # Michigan State Green
            'IND': graphics.Color(153, 0, 0),       # Indiana Crimson
            'ILL': graphics.Color(19, 41, 75),      # Illinois Navy
            'PUR': graphics.Color(206, 184, 136),   # Purdue Gold
            'MINN': graphics.Color(122, 0, 25),     # Minnesota Maroon
            'NW': graphics.Color(78, 42, 132),      # Northwestern Purple
            'MD': graphics.Color(224, 58, 62),      # Maryland Red
            'RUT': graphics.Color(204, 0, 51),      # Rutgers Scarlet
        
            # College - ACC & Others
            'DUKE': graphics.Color(0, 26, 87),      # Duke Blue
            'UNC': graphics.Color(123, 175, 212),   # UNC Carolina Blue
            'CLEM': graphics.Color(246, 103, 51),   # Clemson Orange
            'FSU': graphics.Color(120, 47, 64),     # Florida State Garnet
            'ND': graphics.Color(12, 35, 64),       # Notre Dame Navy
            'USC': graphics.Color(153, 27, 30),     # USC Cardinal
            'UCLA': graphics.Color(39, 116, 174),   # UCLA Blue
            'ORE': graphics.Color(18, 71, 52),      # Oregon Green
            'WASH': graphics.Color(51, 0, 111),     # Washington Purple
            'KU': graphics.Color(0, 81, 186),       # Kansas Blue
            'GONZ': graphics.Color(4, 30, 66),      # Gonzaga Navy
            'VILL': graphics.Color(0, 32, 91),      # Villanova Navy
        }
        
        self.scroll_pos = 0
        self.current_games = []
        self.priority_games = []
        self.last_priority_scores = {}
        
    def fetch_scores(self, sport, league):
        """Fetch live scores from ESPN API"""
        url = f"http://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching {league}: {e}")
        return None
    
    def is_priority_team(self, team_name, league):
        """Check if a team is in the priority list"""
        if league not in PRIORITY_TEAMS:
            return False
        
        priority_names = PRIORITY_TEAMS[league]
        for priority in priority_names:
            if priority.lower() in team_name.lower():
                return True
        return False
    
    def parse_game_data(self, data, league_name, league_key):
        """Parse game data into displayable format"""
        games = []
        if not data or 'events' not in data:
            return games
            
        for event in data['events']:
            try:
                status = event.get('status', {})
                state = status.get('type', {}).get('state', '')
                detail = status.get('type', {}).get('shortDetail', '')
                
                if state == 'post':
                    continue
                    
                competitions = event.get('competitions', [{}])[0]
                competitors = competitions.get('competitors', [])
                
                if len(competitors) >= 2:
                    home = competitors[1]
                    away = competitors[0]
                    
                    home_team_name = home.get('team', {}).get('displayName', '')
                    away_team_name = away.get('team', {}).get('displayName', '')
                    
                    is_priority = (self.is_priority_team(home_team_name, league_key) or 
                                 self.is_priority_team(away_team_name, league_key))
                    
                    game_id = event.get('id', '')
                    
                    game = {
                        'id': game_id,
                        'league': league_name,
                        'league_key': league_key,
                        'away_team': away.get('team', {}).get('abbreviation', 'TBD')[:4],
                        'home_team': home.get('team', {}).get('abbreviation', 'TBD')[:4],
                        'away_score': away.get('score', '0'),
                        'home_score': home.get('score', '0'),
                        'status': detail,
                        'state': state,
                        'is_priority': is_priority,
                        'away_full_name': away_team_name,
                        'home_full_name': home_team_name
                    }
                    games.append(game)
            except Exception as e:
                print(f"Error parsing game: {e}")
                continue
                
        return games
    
    def get_all_games(self):
        """Fetch all sports scores"""
        all_games = []
        priority_games = []
        
        for sport_config in SPORTS_CONFIG:
            data = self.fetch_scores(sport_config['sport'], sport_config['league'])
            games = self.parse_game_data(data, sport_config['name'], sport_config['league'])
            
            for game in games:
                if game['is_priority']:
                    priority_games.append(game)
                else:
                    all_games.append(game)
        
        return priority_games, all_games
    
    def check_priority_score_changes(self):
        """Check if any priority game scores have changed"""
        if not self.priority_games:
            return False
        
        changed = False
        for game in self.priority_games:
            game_id = game['id']
            current_score = f"{game['away_score']}-{game['home_score']}"
            
            if game_id in self.last_priority_scores:
                if self.last_priority_scores[game_id] != current_score:
                    print(f"Score changed for {game['away_team']} @ {game['home_team']}: {current_score}")
                    changed = True
            
            self.last_priority_scores[game_id] = current_score
        
        return changed
    
    def draw_game(self, game, y_offset=0):
        """Draw a single game on the matrix"""
        self.canvas.Clear()
        
        league_color = self.priority_color if game['is_priority'] else self.blue
        graphics.DrawText(self.canvas, self.font_small, 2, 8 + y_offset, 
                         league_color, game['league'])
        
        if game['is_priority']:
            graphics.DrawText(self.canvas, self.font_small, 35, 8 + y_offset, 
                             self.yellow, "★")
        
        away_team_color = self.team_colors.get(game['away_team'], self.white)
        home_team_color = self.team_colors.get(game['home_team'], self.white)
        
        try:
            away_int = int(game['away_score'])
            home_int = int(game['home_score'])
        except:
            away_int = 0
            home_int = 0
        
        graphics.DrawText(self.canvas, self.font_large, 2, 17 + y_offset, 
                         away_team_color, game['away_team'])
        away_score_color = self.green if away_int > home_int else self.white
        graphics.DrawText(self.canvas, self.font_large, 32, 17 + y_offset, 
                         away_score_color, game['away_score'])
        
        graphics.DrawText(self.canvas, self.font_large, 2, 25 + y_offset, 
                         home_team_color, game['home_team'])
        home_score_color = self.green if home_int > away_int else self.white
        graphics.DrawText(self.canvas, self.font_large, 32, 25 + y_offset, 
                         home_score_color, game['home_score'])
        
        status_text = game['status'][:20]
        graphics.DrawText(self.canvas, self.font_small, 2, 32 + y_offset, 
                         self.yellow, status_text)
        
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
    
    def draw_no_games(self):
        """Display message when no games are active"""
        self.canvas.Clear()
        graphics.DrawText(self.canvas, self.font_large, 10, 16, 
                         self.blue, "NO LIVE GAMES")
        graphics.DrawText(self.canvas, self.font_small, 15, 28, 
                         self.white, datetime.now().strftime("%H:%M"))
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
    
    def run(self):
        """Main display loop with priority team monitoring"""
        print("Starting Sports Score Display v2.0...")
        print(f"Priority Teams configured: {len(PRIORITY_TEAMS)} leagues")
        game_index = 0
        update_counter = 0
        priority_check_counter = 0
        
        try:
            while True:
                if update_counter % FULL_UPDATE_INTERVAL == 0:
                    print(f"Full score refresh... {datetime.now()}")
                    self.priority_games, other_games = self.get_all_games()
                    self.current_games = self.priority_games + other_games
                    print(f"Found {len(self.priority_games)} priority games, {len(other_games)} other games")
                    game_index = 0
                    self.check_priority_score_changes()
                
                elif self.priority_games and priority_check_counter % PRIORITY_UPDATE_INTERVAL == 0:
                    print("Quick check of priority games...")
                    new_priority_games, _ = self.get_all_games()
                    
                    if new_priority_games:
                        for i, game in enumerate(self.current_games):
                            if game['is_priority']:
                                for new_game in new_priority_games:
                                    if new_game['id'] == game['id']:
                                        self.current_games[i] = new_game
                                        break
                        
                        self.priority_games = new_priority_games
                        
                        if self.check_priority_score_changes():
                            game_index = 0
                            print("Priority game score changed! Updating display...")
                
                if self.current_games:
                    game = self.current_games[game_index]
                    self.draw_game(game)
                    
                    display_time = PRIORITY_GAME_DISPLAY_TIME if game['is_priority'] else NON_PRIORITY_GAME_DISPLAY_TIME
                    time.sleep(display_time)
                    
                    game_index = (game_index + 1) % len(self.current_games)
                else:
                    self.draw_no_games()
                    time.sleep(5)
                
                update_counter += 1
                priority_check_counter += 1
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.canvas.Clear()
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

if __name__ == "__main__":
    display = SportsScoreDisplay()
    display.run()
