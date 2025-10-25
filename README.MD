# Sports Score LED Matrix Display v2.0

Real-time sports score display for Raspberry Pi with 32x128 RGB LED Matrix. Shows live scores from MLB, NFL, NBA, NCAA Football, NCAA Basketball, and NCAA Baseball with priority tracking for your favorite teams.

**New in v2.0:**
- ✨ Team colors for 100+ teams (MLB, NFL, NBA, College)
- 📊 One team per line layout for better readability
- 🎨 Cleaner, easier-to-read display

## Features

- 🏆 **Priority Team Tracking**: Houston Astros & Arkansas Razorbacks get extra screen time
- ⚡ **Real-Time Updates**: Priority games update every 5 seconds, others every 60 seconds
- 🎨 **Team Colors**: Authentic colors for 100+ teams across all leagues
- 🔄 **Auto-Rotation**: Cycles through all active games
- 🚀 **Auto-Start**: Runs automatically on boot
- 📱 **Multi-Sport Support**: MLB, NFL, NBA, NCAAF, NCAAB, NCAA Baseball

## Hardware Requirements

- Raspberry Pi 4 (3B+ also works)
- 32x128 RGB LED Matrix (HUB75 interface)
- 5V Power Supply (5A+ recommended)
- Adafruit RGB Matrix HAT or Bonnet (recommended)

## Quick Install

SSH into your Raspberry Pi and run:

```bash
bash <(curl -s https://raw.githubusercontent.com/jshaddo/sports-score-led-matrix/main/install.sh)
```

**⚠️ IMPORTANT:** Replace `YOUR_USERNAME` with your actual GitHub username!

The installer will:
- Install all dependencies
- Build RGB Matrix library from source
- Configure your Raspberry Pi
- Set up the display service
- Enable auto-start on boot

**Installation takes 15-20 minutes. Reboot required after installation.**

```bash
sudo reboot
```

## Usage

After rebooting, the display starts automatically. Control it with:

```bash
# Start the display
sudo systemctl start sports-display

# Stop the display
sudo systemctl stop sports-display

# Check status
sudo systemctl status sports-display

# View logs
sudo journalctl -u sports-display -f

# Enable auto-start on boot
sudo systemctl enable sports-display

# Disable auto-start
sudo systemctl disable sports-display
```

## Display Format

```
MLB ★           (League with priority star)
HOU  5          (Away team in orange + score)
NYY  3          (Home team in navy + score)
Top 7th         (Game status)
```

## Customization

### Change Priority Teams

Edit `config.py` after installation:

```bash
cd ~/sports-display
nano config.py
```

Modify the teams:
```python
PRIORITY_TEAMS = {
    'mlb': ['Your Team Name', 'ABBR'],
    'college-football': ['Your School', 'ABBR'],
    # ... etc
}
```

Then restart:
```bash
sudo systemctl restart sports-display
```

### Adjust Display Times

In `config.py`:
```python
PRIORITY_GAME_DISPLAY_TIME = 8  # seconds for priority games
NON_PRIORITY_GAME_DISPLAY_TIME = 3  # seconds for other games
```

### Hardware Configuration

If your display flickers or doesn't work, edit `config.py`:

```python
MATRIX_HARDWARE_MAPPING = 'regular'  # Try: 'adafruit-hat', 'adafruit-hat-pwm'
MATRIX_GPIO_SLOWDOWN = 4  # Try: 2, 3, 4, or 5 if flickering
```

After changes, restart:
```bash
sudo systemctl restart sports-display
```

## Team Colors Included

- **MLB**: All 30 teams
- **NFL**: All 32 teams  
- **NBA**: All 30 teams
- **College**: 40+ major programs including SEC, Big Ten, ACC

## Troubleshooting

### Display Issues

**Flickering Display:**
- Increase `MATRIX_GPIO_SLOWDOWN` in `config.py` (try 5)
- Try different `MATRIX_HARDWARE_MAPPING` options

**No Display:**
- Check power supply and connections
- Verify service is running: `sudo systemctl status sports-display`
- Check logs: `sudo journalctl -u sports-display -n 50`

**Wrong Colors:**
- Try different hardware mapping in `config.py`

### Network/API Issues

**No Games Showing:**
- Check internet: `ping espn.com`
- Games might not be in season
- Test API: `curl "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"`

**Service Won't Start:**
```bash
# Check for errors
sudo journalctl -u sports-display -n 50

# Try running manually
cd ~/sports-display
sudo python3 sports_display.py
```

## Update from GitHub

```bash
cd ~/sports-display
git pull
sudo systemctl restart sports-display
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

MIT License - See LICENSE file

## Credits

- Built with [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) by Henner Zeller
- Sports data from ESPN

---

⭐ **Star this repo if you find it useful!**
