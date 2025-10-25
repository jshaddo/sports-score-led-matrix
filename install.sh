#!/bin/bash
# Sports Score LED Matrix Display - Automated Installer
# For Raspberry Pi 4 with 32x128 RGB LED Matrix

set -e  # Exit on any error

REPO_URL="https://github.com/jshaddo/sports-score-led-matrix.git"
INSTALL_DIR="$HOME/sports-display"

echo "========================================"
echo "Sports Score Display Installer"
echo "Houston Astros & Arkansas Razorbacks"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run as root. Run as regular user (pi)."
    echo "The script will prompt for sudo when needed."
    exit 1
fi

# Update system
echo "Step 1: Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
echo "Step 2: Installing dependencies..."
sudo apt-get install -y git python3-dev python3-pillow python3-pip
sudo apt-get install -y libgraphicsmagick++-dev libwebp-dev
sudo apt-get install -y fonts-dejavu-core

# Install RGB Matrix Library
echo "Step 3: Installing RGB LED Matrix library..."
cd ~
if [ -d "rpi-rgb-led-matrix" ]; then
    echo "RGB Matrix library already exists, updating..."
    cd rpi-rgb-led-matrix
    git pull
else
    echo "Cloning RGB Matrix library..."
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
    cd rpi-rgb-led-matrix
fi

echo "Building RGB Matrix library..."
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

# Install Python packages
echo "Step 4: Installing Python packages..."
sudo pip3 install requests

# Disable audio (conflicts with PWM for LED matrix)
echo "Step 5: Configuring Raspberry Pi..."
CONFIG_FILE="/boot/config.txt"
FIRMWARE_CONFIG="/boot/firmware/config.txt"

# Check which config file exists (newer Pi OS uses /boot/firmware/)
if [ -f "$FIRMWARE_CONFIG" ]; then
    CONFIG_FILE="$FIRMWARE_CONFIG"
fi

echo "Using config file: $CONFIG_FILE"

# Backup config
sudo cp $CONFIG_FILE ${CONFIG_FILE}.backup

# Disable audio
if ! grep -q "dtparam=audio=off" $CONFIG_FILE; then
    echo "Disabling audio (required for LED matrix)..."
    echo "" | sudo tee -a $CONFIG_FILE
    echo "# Disable audio for LED matrix" | sudo tee -a $CONFIG_FILE
    echo "dtparam=audio=off" | sudo tee -a $CONFIG_FILE
fi

# Set GPU memory
if ! grep -q "gpu_mem=16" $CONFIG_FILE; then
    echo "Setting GPU memory..."
    echo "gpu_mem=16" | sudo tee -a $CONFIG_FILE
fi

# Clone or update repository
echo "Step 6: Installing sports display software..."
if [ -d "$INSTALL_DIR" ]; then
    echo "Installation directory exists, updating..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Make script executable
chmod +x sports_display.py

# Create systemd service
echo "Step 7: Creating systemd service..."
sudo tee /etc/systemd/system/sports-display.service > /dev/null << EOF
[Unit]
Description=Sports Score LED Display
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/sports_display.py
WorkingDirectory=$INSTALL_DIR
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Configuration file: $INSTALL_DIR/config.py"
echo "Edit this file to customize your display and priority teams."
echo ""
echo "IMPORTANT: You must reboot for the audio disable to take effect."
echo ""
echo "After rebooting, use these commands:"
echo ""
echo "Start the display:"
echo "  sudo systemctl start sports-display"
echo ""
echo "Enable auto-start on boot:"
echo "  sudo systemctl enable sports-display"
echo ""
echo "Check status:"
echo "  sudo systemctl status sports-display"
echo ""
echo "View logs:"
echo "  sudo journalctl -u sports-display -f"
echo ""
echo "Stop the display:"
echo "  sudo systemctl stop sports-display"
echo ""
echo "Test manually (without service):"
echo "  cd $INSTALL_DIR"
echo "  sudo python3 sports_display.py"
echo ""
echo "Customize priority teams:"
echo "  nano $INSTALL_DIR/config.py"
echo "  sudo systemctl restart sports-display"
echo ""
echo "========================================"
echo "Reboot now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    sudo reboot
fi
