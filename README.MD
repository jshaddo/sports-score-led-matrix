# Sports Score LED Matrix Display

Real-time sports score display for Raspberry Pi with 32x128 RGB LED Matrix. Shows live scores from MLB, NFL, NBA, NCAA Football, NCAA Basketball, and NCAA Baseball with priority tracking for your favorite teams.

## Features

- 🏆 **Priority Team Tracking**: Houston Astros & Arkansas Razorbacks get extra screen time
- ⚡ **Real-Time Updates**: Priority games update every 5 seconds, others every 60 seconds
- 🎨 **Color-Coded Display**: Winning scores highlighted in green, priority teams in magenta
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
curl -sSL https://raw.githubusercontent.com/jshaddo/sports-score-led-matrix/main/install.sh | bash
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

Or clone and install manually:
```bash
git clone https://github.com/jshaddo/sports-score-led-matrix.git
cd sports-score-led-matrix
chmod +x install.sh
./install.sh
```

The installer will:
- Install all dependencies
- Configure your Raspberry Pi
- Set up the display service
- Enable auto-start on boot

**Reboot after installation:**
```bash
sudo reboot
```

## Usage

After rebooting, the display starts automatically. You can also control it manually:
```bash
# Start the display
sudo systemctl start sports-display

# Stop the display
sudo systemctl stop sports-display

# Check status
sudo systemctl status sports-display

# View logs
sudo journalctl -u sports-display -f

# Disable auto-start
sudo systemctl disable sports-display
```

## Customization

### Change Priority Teams

Edit `config.py`:
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

In `config.py`, modify:
```python
PRIORITY_GAME_DISPLAY_TIME = 8  # seconds
NON_PRIORITY_GAME_DISPLAY_TIME = 3  # seconds
```

### Hardware Mapping

If your display flickers or doesn't work, try different hardware mappings in `config.py`:
```python
MATRIX_HARDWARE_MAPPING = 'regular'  # Try: 'adafruit-hat', 'adafruit-hat-pwm'
MATRIX_GPIO_SLOWDOWN = 4  # Try: 2, 3, 4, or 5
```

## Troubleshooting

### Flickering Display
- Increase `MATRIX_GPIO_SLOWDOWN` in `config.py`
- Try different `MATRIX_HARDWARE_MAPPING` options

### No Display
- Check power supply and connections
- Verify service is running: `sudo systemctl status sports-display`
- Check logs: `sudo journalctl -u sports-display -n 50`

### No Games Showing
- Check internet connection
- Games might not be in season
- Test API: `curl "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"`

## API Data Source

Uses ESPN's public scoreboard API - no API key required!

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

MIT License - See LICENSE file

## Credits

- Built with [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) by Henner Zeller
- Sports data from ESPN

---

⭐ Star this repo if you find it useful!
