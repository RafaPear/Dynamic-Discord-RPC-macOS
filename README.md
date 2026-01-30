# Dynamic DiscordRPC for macOS in Python

This app shows the **currently focused application** on Discord using Rich Presence.
It keeps track of **focused time**, meaning:

- If you spend **10 minutes** in Firefox
- Switch to another app for **5 minutes**
- Then focus Firefox again

Discord will still show **10 minutes**, not 15.

It also shows the **window title** of the focused app.
The application name shown on Discord is taken from the **`.app` file inside `/Applications`**, not from the process name.


## Quick start

1. Clone the repository

```bash
git clone https://github.com/RafaPear/Terminal-discord-presence.git
cd Terminal-discord-presence
```

2. Install the dependencies

```bash
python3 -m pip install -r requirements.txt
```

3. Create a Discord application
   - Go to the Discord Developer Portal
   - Create a new application and copy the **Application ID**
   - Put it in `config.py`

```python
DISCORD_CLIENT_ID = "YOUR_DISCORD_APP_ID"
```

4. Choose which apps to track (whitelist)

```python
WHITELIST = {
  "firefox",
  "spotify",
  "live",
  "iterm2",
}
```

⚠️ The whitelist uses **process names**, not app names.
Examples: Spotify → `spotify`, Ableton Live 12 Suite → `live`, iTerm → `iterm2`.
Images in your Discord Rich Presence app must match these process names.

5. First run (grants accessibility permissions)

```bash
python3 main.py
```

macOS will ask for Accessibility permissions to read window titles. Allow access for Terminal or the Python executable you are using.

6. Restart the app after granting permissions

```bash
python3 main.py
```

If the window title still does not appear, run it once more; macOS sometimes needs an extra run.


## Optional: override config via CLI

- Use a different config file:

```bash
python3 main.py --config my_config.py
```

- Override the app ID and whitelist without editing files:

```bash
python3 main.py --app-id 123456789012345678 --apps firefox spotify iterm2
```


## Notes

- Works only with the Discord desktop client
- Make sure “Display current activity as a status message” is enabled in Discord settings
- Discord aggressively caches Rich Presence — restart Discord if something does not update
- Buttons (e.g., GitHub) only appear on desktop
