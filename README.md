
# Universal Browser Profile Migrator

A free, lightweight, and universal profile migrator for browsers based on the Chromium and Gecko engines. This tool allows you to easily backup and restore your browser profiles, including history, bookmarks, extensions, and settings, even across different installations or portable versions.

## Features

- **Multi-Browser Support:** Works with a wide range of browsers using Gecko (Firefox-based) and Chromium engines.
- **Backup & Restore:** Simple interface to create full backups of your browser data or restore them to a new installation.
- **Portable Version Support:** Specifically designed to handle portable/standalone browser folders.
- **Automatic Detection:** Automatically locates profile directories for standard installations on Windows.
- **Safety Checks:** Verifies if the browser is closed before performing operations to prevent data corruption.
- **User-Friendly GUI:** Built with Tkinter for a simple, responsive graphical experience.
- **Real-time Logging:** Provides detailed status updates and progress tracking during migration.

## Supported Browsers

### Gecko Engine
- Firefox
- Waterfox
- LibreWolf
- Pale Moon
- Tor Browser

### Chromium Engine
- Google Chrome
- Brave
- Microsoft Edge
- Opera
- Vivaldi
- Yandex Browser

## Requirements

- **Operating System:** Windows (uses Windows-specific environment variables and commands).
- **Python:** Python 3.x
- **Dependencies:** Uses standard library modules (`tkinter`, `shutil`, `os`, `threading`, etc.).

## How to Use

1. **Launch the Application:**
   ```bash
   python Universal-Browser-Profile-Migrator.py
   ```
2. **Select Your Browser:** Choose the browser you want to backup or restore from the dropdown menu.
3. **Toggle Portable Mode (Optional):** If you are using a portable version of the browser, check the "Portable Version" box and browse to its location.
4. **Choose Action:** Select either "Backup" or "Restore".
5. **Select Location:**
   - For **Backup**: Select the folder where you want to save your profile archive.
   - For **Restore**: Select the folder containing your previously created backup.
6. **Start Transfer:** Click the "Start Transfer" button and wait for the process to complete.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

Ensure your browser is completely closed before starting the migration. While this tool handles file copying, it is always recommended to have a separate backup of your important data.
