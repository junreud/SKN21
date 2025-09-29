# Solitaire Game

A beautiful, cross-platform Solitaire game built with Python and Pygame.

## 🎮 Features

- **Classic Solitaire gameplay** - Traditional Klondike Solitaire rules
- **Beautiful graphics** - Clean, colorful interface
- **Cross-platform** - Works on Windows, macOS, and Linux
- **No installation required** - Standalone executable files
- **Easy controls** - Point and click interface

## 🎯 How to Play

1. **Objective**: Move all cards to the four foundation piles, sorted by suit from Ace to King
2. **Tableau**: Build down in alternating colors (red on black, black on red)
3. **Foundations**: Build up by suit starting with Ace
4. **Stock**: Click to draw cards from the deck
5. **Empty columns**: Only Kings can be placed on empty tableau columns

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)
- **Windows**: Download `Solitaire.exe` and double-click to play
- **macOS**: Download `Solitaire.dmg`, mount it, and drag the app to Applications

### Option 2: Run from Source
```bash
# Install Python 3.7+ and pip
pip install pygame
python solitaire_pygame.py
```

## 🛠️ Building from Source

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Build Steps
1. Clone or download the source code
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build executable:
   - **Windows**: Run `build_windows.bat`
   - **macOS/Linux**: Run `chmod +x build.sh && ./build.sh`

4. Find your executable in the `dist/` folder

### Manual Build Commands
```bash
# Install PyInstaller
pip install pyinstaller

# Windows
pyinstaller --onefile --windowed --name "Solitaire" solitaire_pygame.py

# macOS (creates .app bundle)
pyinstaller --onefile --windowed --name "Solitaire" solitaire_pygame.py
```

## 📦 Distribution

The built executables are completely standalone and can be distributed to users without requiring Python installation.

### File Sizes (approximate)
- Windows .exe: ~15-20 MB
- macOS .app: ~20-25 MB
- DMG package: ~10-15 MB

## 🎨 Controls

- **Left Click**: Select cards and move them
- **Click Deck**: Draw new cards
- **New Game Button**: Start a fresh game
- **Close Window**: Exit game

## 🔧 Technical Details

- **Engine**: Pygame 2.5+
- **Python**: 3.7+
- **Packaging**: PyInstaller
- **Platforms**: Windows 7+, macOS 10.12+, Linux

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests!

---

**Enjoy playing Solitaire! 🃏**