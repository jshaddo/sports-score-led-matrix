#!/usr/bin/env python3
"""
Real-time Sports Score Display for 32x128 RGB LED Matrix
Displays scores from MLB, NFL, NBA, NCAA Football, NCAA Basketball, and NCAA Baseball
Prioritizes Houston Astros and Arkansas Razorbacks with live score tracking
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
        
        self.scroll_pos = 0
        self.current_games = []
        self.priority_games = []
        self.last_priority_scores = {}  # Track scores to detect changes
        
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
                # Get game status
                status = event.get('status', {})
                state = status.get('type', {}).get('state', '')
                detail = status.get('type', {}).get('shortDetail', '')
                
                # Skip completed games unless recent
                if state == 'post':
                    continue
                    
                competitions = event.get('competitions', [{}])[0]
                competitors = competitions.get('competitors', [])
                
                if len(competitors) >= 2:
                    # Typically [1] is home, [0] is away
                    home = competitors[1]
                    away = competitors[0]
                    
                    home_team_name = home.get('team', {}).get('displayName', '')
                    away_team_name = away.get('team', {}).get('displayName', '')
                    
                    # Check if this is a priority game
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
        
        # Priority games come first
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
        
        # League header with priority indicator
        league_color = self.priority_color if game['is_priority'] else self.blue
        graphics.DrawText(self.canvas, self.font_small, 2, 8 + y_offset, 
                         league_color, game['league'])
        
        if game['is_priority']:
            # Add star indicator for priority games
            graphics.DrawText(self.canvas, self.font_small, 35, 8 + y_offset, 
                             self.yellow, "★")
        
        # Away team
        graphics.DrawText(self.canvas, self.font_large, 2, 20 + y_offset, 
                         self.white, game['away_team'])
        
        # Away score
        try:
            away_int = int(game['away_score'])
            home_int = int(game['home_score'])
            score_color = self.green if away_int > home_int else self.white
        except:
            score_color = self.white
            
        graphics.DrawText(self.canvas, self.font_large, 50, 20 + y_offset, 
                         score_color, game['away_score'])
        
        # @ symbol
        graphics.DrawText(self.canvas, self.font_small, 70, 20 + y_offset, 
                         self.white, "@")
        
        # Home team
        graphics.DrawText(self.canvas, self.font_large, 80, 20 + y_offset, 
                         self.white, game['home_team'])
        
        # Home score
        try:
            score_color = self.green if home_int > away_int else self.white
        except:
            score_color = self.white
            
        graphics.DrawText(self.canvas, self.font_large, 2, 30 + y_offset, 
                         score_color, game['home_score'])
        
        # Status (quarter, inning, etc.)
        status_text = game['status'][:20]  # Truncate if too long
        graphics.DrawText(self.canvas, self.font_small, 30, 30 + y_offset, 
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
        print("Starting Sports Score Display...")
        print(f"Priority Teams configured: {len(PRIORITY_TEAMS)} leagues")
        game_index = 0
        update_counter = 0
        priority_check_counter = 0
        
        try:
            while True:
                # Full refresh based on config
                if update_counter % FULL_UPDATE_INTERVAL == 0:
                    print(f"Full score refresh... {datetime.now()}")
                    self.priority_games, other_games = self.get_all_games()
                    self.current_games = self.priority_games + other_games
                    print(f"Found {len(self.priority_games)} priority games, {len(other_games)} other games")
                    game_index = 0
                    self.check_priority_score_changes()  # Initialize tracking
                
                # Quick check for priority game score changes
                elif self.priority_games and priority_check_counter % PRIORITY_UPDATE_INTERVAL == 0:
                    print("Quick check of priority games...")
                    new_priority_games, _ = self.get_all_games()
                    
                    if new_priority_games:
                        # Update priority games in the current list
                        for i, game in enumerate(self.current_games):
                            if game['is_priority']:
                                # Find matching game in new data
                                for new_game in new_priority_games:
                                    if new_game['id'] == game['id']:
                                        self.current_games[i] = new_game
                                        break
                        
                        self.priority_games = new_priority_games
                        
                        # Check if scores changed
                        if self.check_priority_score_changes():
                            # Reset to show priority games immediately
                            game_index = 0
                            print("Priority game score changed! Updating display...")
                
                if self.current_games:
                    # Display each game based on priority from config
                    game = self.current_games[game_index]
                    self.draw_game(game)
                    
                    display_time = PRIORITY_GAME_DISPLAY_TIME if game['is_priority'] else NON_PRIORITY_GAME_DISPLAY_TIME
                    time.sleep(display_time)
                    
                    # Move to next game
                    game_index = (game_index + 1) % len(self.current_games)
                else:
                    self.draw_no_games()
                    time.sleep(5)
                
                update_counter += 1
                priority_check_counter += 1
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.canvas.Clear()
            self.canvas = self.canvas = self.matrix.SwapOnVSync(self.canvas)

if __name__ == "__main__":
    display = SportsScoreDisplay()
    display.run()
