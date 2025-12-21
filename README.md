```
      ::::::::      :::     :::::::::  :::  
    :+:    :+:   :+: :+:   :+:    :+: :+:   
   +:+         +:+   +:+  +:+    +:+ +:+    
  +#+        +#++:++#++: +#+    +:+ +#+     
 +#+        +#+     +#+ +#+    +#+ +#+      
#+#    #+# #+#     #+# #+#    #+# #+#       
########  ###     ### #########  ########## 
```
# Ctrl + Alt + De-leash
The application which is gonna change your life (forever(no going back(no(meow))))

`
Like ctrl+alt+delete but way more brutal. This bot doesn't just end tasks—it jailbreaks them, screams into the void, and deploys chaos to prod with zero warnings. Half debugger, half catboy, all vibes. If your code's on fire? It's already roasting marshmallows.
`

## Installation on Debian

### Prerequisites
- Debian 11 (Bullseye) or newer
- `sudo` access for installing system packages
- A Discord Bot Token (get one from [Discord Developer Portal](https://discord.com/developers/applications))

### Step 1: Install Python 3.12

Debian's default repositories may not have Python 3.12. Here are the recommended methods:

#### Option A: Using deadsnakes PPA (Recommended for Ubuntu-based systems)
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev
```

#### Option B: Build from source
```bash
# Install build dependencies
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# Download and build Python 3.12
cd /tmp
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar -xf Python-3.12.0.tgz
cd Python-3.12.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

#### Option C: Using pyenv (Recommended for development)
```bash
# Install dependencies
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc or ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Install Python 3.12
pyenv install 3.12.0
pyenv global 3.12.0
```

### Step 2: Clone the Repository
```bash
git clone https://github.com/catpawzz/ctrl-alt-de-leash.git
cd ctrl-alt-de-leash
```

### Step 3: Install Dependencies

#### Option A: Using uv (Recommended - Fast)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

#### Option B: Using pip with venv
```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
- `BOT_TOKEN`: Your Discord bot token (required)
- `APPLICATION_ID`: Your Discord application ID (required)
- `BOT_NAME`: Display name for the bot (optional)
- `WAKATIME_KEY`: WakaTime API key (optional)
- `WAKATIME_URL`: WakaTime URL (optional)
- `GOOGLE_AI_API_KEY`: Google AI API key (optional)

### Step 5: Run the Bot
```bash
# If using uv
uv run mewo.py

# If using venv
source venv/bin/activate
python3.12 mewo.py
```

### Running as a Service (Optional)

To run the bot as a systemd service:

1. Create a service file:
```bash
sudo nano /etc/systemd/system/ctrl-alt-de-leash.service
```

2. Add the following content (adjust paths as needed):
```ini
[Unit]
Description=Ctrl Alt De-leash Discord Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/ctrl-alt-de-leash
Environment="PATH=/path/to/ctrl-alt-de-leash/venv/bin"
ExecStart=/path/to/ctrl-alt-de-leash/venv/bin/python3.12 mewo.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ctrl-alt-de-leash
sudo systemctl start ctrl-alt-de-leash
sudo systemctl status ctrl-alt-de-leash
```

### Troubleshooting

#### "No BOT_TOKEN found in environment variables"
Make sure you've created the `.env` file and added your Discord bot token:
```bash
cp .env.example .env
nano .env  # Add your BOT_TOKEN
```

#### Python version issues
Verify you're using Python 3.12 or newer:
```bash
python3.12 --version
```

#### Missing dependencies
If you get import errors, reinstall dependencies:
```bash
# With uv
uv sync --reinstall

# With pip
pip install --force-reinstall -r requirements.txt
```

#### Permission issues
Make sure the bot has write permissions for the `logs` directory and `reminders.json`:
```bash
mkdir -p logs
chmod 755 logs
```

### Getting a Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the bot's username, click "Reset Token" to get your bot token
6. Copy the token and paste it into your `.env` file as `BOT_TOKEN`
7. Enable "Message Content Intent" under Privileged Gateway Intents
8. Go to OAuth2 > URL Generator, select scopes: `bot`, `applications.commands`
9. Select required permissions and use the generated URL to invite the bot
