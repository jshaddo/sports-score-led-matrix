"""
Configuration file for Sports Score Display
Edit this file to customize your display
"""

# Matrix Configuration
MATRIX_WIDTH = 128
MATRIX_HEIGHT = 32
MATRIX_HARDWARE_MAPPING = 'regular'  # Options: 'regular', 'adafruit-hat', 'adafruit-hat-pwm'
MATRIX_GPIO_SLOWDOWN = 4  # Increase if flickering (try 2, 3, 4, or 5)

# Priority teams - these will be checked more frequently and displayed first
PRIORITY_TEAMS = {
    'mlb': ['Houston Astros', 'Astros', 'HOU'],
    'college-football': ['Arkansas Razorbacks', 'Razorbacks', 'Arkansas', 'ARK'],
    'mens-college-basketball': ['Arkansas Razorbacks', 'Razorbacks', 'Arkansas', 'ARK'],
    'college-baseball': ['Arkansas Razorbacks', 'Razorbacks', 'Arkansas', 'ARK']
}

# Display timing (in seconds)
PRIORITY_GAME_DISPLAY_TIME = 8
NON_PRIORITY_GAME_DISPLAY_TIME = 3
PRIORITY_UPDATE_INTERVAL = 5  # How often to check priority games for score changes
FULL_UPDATE_INTERVAL = 60  # How often to refresh all games

# Sports to track
SPORTS_CONFIG = [
    {'name': 'MLB', 'sport': 'baseball', 'league': 'mlb'},
    {'name': 'NFL', 'sport': 'football', 'league': 'nfl'},
    {'name': 'NBA', 'sport': 'basketball', 'league': 'nba'},
    {'name': 'NCAAF', 'sport': 'football', 'league': 'college-football'},
    {'name': 'NCAAB', 'sport': 'basketball', 'league': 'mens-college-basketball'},
    {'name': 'NCAABB', 'sport': 'baseball', 'league': 'college-baseball'}
]

# Font paths
FONT_LARGE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SMALL = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
