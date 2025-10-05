# Photo Enhancement Tool

A Python-based photo enhancement tool with both **Command Line Interface (CLI)** and **Desktop GUI** options. Apply professional edits with predefined profiles for quick and high-quality photo improvements.

## Features

- **Desktop GUI** - User-friendly graphical interface with drag-and-drop workflow
- **CLI-based tool** - Easy to use from the command line for automation
- **Profile-based enhancement system** - Apply consistent edits with a single command
- **Batch processing** - Process entire folders of images at once
- **EXIF orientation handling** - Automatically maintains correct photo orientation
- **EXIF metadata preservation** - Keeps important image metadata (camera info, date, location, etc.)
- **Multiple adjustment types** - HDR, brightness, contrast, saturation, warmth, shadows, and white point
- **Professional algorithms** - Advanced image processing for high-quality results
- **Easy to customize** - Create your own profiles or modify existing ones
- **Cross-platform** - Works on Windows, macOS, and Linux

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Linux/macOS):
```bash
chmod +x photo_enhancer.py
```

## Quick Start

### Easy Launcher (Recommended for First-Time Users)

```bash
python run.py
```

This will give you a simple menu to choose between GUI or CLI mode.

### Using the Desktop GUI (Easiest)

```bash
python photo_enhancer_gui.py
```

Then:
1. Choose "Single Image" or "Folder (Batch)" mode
2. Click "Browse..." to select your input
3. Choose where to save the output
4. Select an enhancement profile
5. Click "Start Processing"

### Using the Command Line

**List Available Profiles:**
```bash
python photo_enhancer.py --list-profiles
```

**Enhance a Single Photo:**
```bash
python photo_enhancer.py -i photo.jpg -o enhanced.jpg -p HDR_Boost
```

**Enhance All Photos in a Folder:**
```bash
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost
```

**Quiet Mode (Minimal Output):**
```bash
python photo_enhancer.py -f photos -o enhanced -p Vibrant --quiet
```

## Available Profiles

### HDR_Boost
Your specified high-impact profile for dramatic improvements:
- HDR: 100%
- Brightness: +10%
- Contrast: +10%
- White Point: +5%
- Shadows: +25%
- Saturation: +25%
- Warmth: +10%

**Best for:** Landscape photos, architectural shots, scenes with high dynamic range

### Natural_Enhance
Subtle improvements that maintain a natural look:
- HDR: 30%
- Brightness: +5%
- Contrast: +5%
- Saturation: +15%
- Warmth: +5%

**Best for:** Everyday photos, general purpose enhancement

### Vibrant
Bold and punchy colors with strong contrast:
- HDR: 50%
- Brightness: +8%
- Contrast: +15%
- Saturation: +40%

**Best for:** Product photography, social media content, eye-catching images

### Portrait
Optimized for people with flattering warmth:
- HDR: 20%
- Brightness: +12%
- Shadows: +30%
- Saturation: +10%
- Warmth: +15%

**Best for:** Portrait photography, headshots, people-focused images

## Desktop GUI

The GUI provides a user-friendly interface for those who prefer not to use the command line.

### Features

- **Visual profile selection** with detailed information display
- **Browse buttons** for easy file/folder selection
- **Progress tracking** with visual progress bar
- **Real-time status updates**
- **Profile preview** showing all adjustment values
- **Batch processing** with automatic output organization
- **Threaded processing** keeps the UI responsive during enhancement

### GUI Workflow

1. **Launch the GUI:**
   ```bash
   python photo_enhancer_gui.py
   ```

2. **Select Processing Mode:**
   - Single Image - Process one photo at a time
   - Folder (Batch) - Process all images in a folder

3. **Choose Input:**
   - Click "Browse..." to select your photo or folder
   - The output path will be auto-suggested

4. **Select Output:**
   - Click "Browse..." to choose where to save
   - For folders, you can choose to create subfolders per profile

5. **Pick Profile:**
   - Select from the dropdown menu
   - View profile details below the dropdown
   - Click "View All Profiles" for complete information

6. **Start Processing:**
   - Click "Start Processing" button
   - Watch the progress bar
   - Get notification when complete

### GUI Screenshot Description

The GUI includes:
- Mode selection (Single/Folder)
- Input and output browse buttons
- Profile dropdown with live preview
- Options checkbox for subfolder creation
- Progress bar and status indicator
- Action buttons (Start, Clear, Exit)

### Creating Desktop Shortcuts

**Windows:**
1. Right-click `photo_enhancer_gui.py`
2. Select "Create shortcut"
3. Right-click the shortcut → Properties
4. Change "Target" to: `python "C:\path\to\photo_enhancer_gui.py"`
5. Click "Change Icon" to customize (optional)

**macOS:**
1. Open Automator
2. Create new "Application"
3. Add "Run Shell Script" action
4. Enter: `cd /path/to/folder && python3 photo_enhancer_gui.py`
5. Save as "Photo Enhancer.app"

**Linux:**
Create a `.desktop` file:
```ini
[Desktop Entry]
Name=Photo Enhancer
Exec=python3 /path/to/photo_enhancer_gui.py
Icon=/path/to/icon.png
Type=Application
Categories=Graphics;
```

## Usage Examples

### Command Line Interface

**List all available profiles:**
```bash
python photo_enhancer.py --list-profiles
```

**Enhance a single image:**
```bash
python photo_enhancer.py -i vacation.jpg -o vacation_enhanced.jpg -p HDR_Boost
```

**Batch process a folder:**
```bash
# Creates enhanced/HDR_Boost/ subfolder
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost

# Without creating profile subfolder
python photo_enhancer.py -f photos -o enhanced -p Natural_Enhance --no-subfolder
```

**Process with different profiles:**
```bash
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost
python photo_enhancer.py -f photos -o enhanced -p Natural_Enhance
python photo_enhancer.py -f photos -o enhanced -p Vibrant
python photo_enhancer.py -f photos -o enhanced -p Portrait
```

**Quiet mode for scripts:**
```bash
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost --quiet
```

### Command Line Options

```
Options:
  -h, --help            Show help message and exit
  -i INPUT, --input INPUT
                        Input image file
  -o OUTPUT, --output OUTPUT
                        Output image file or folder
  -f FOLDER, --folder FOLDER
                        Input folder containing images to process
  -p PROFILE, --profile PROFILE
                        Enhancement profile to apply
                        Choices: HDR_Boost, Natural_Enhance, Vibrant, Portrait
  --list-profiles       List all available profiles
  --no-subfolder        Do not create profile subfolders when processing folders
  -q, --quiet           Quiet mode - minimal output
```

### Python API (Advanced Usage)

You can also import and use the functions directly in Python:

```python
from photo_enhancer import enhance_photo, enhance_folder, list_profiles

# List profiles
list_profiles()

# Single image
enhance_photo("input.jpg", "output.jpg", "HDR_Boost")

# Batch folder
enhance_folder("photos", "enhanced", "HDR_Boost")
```

## Creating Custom Profiles

To add your own profiles, edit the `PROFILES` dictionary in `photo_enhancer.py`:

```python
# Add this to the PROFILES dictionary in photo_enhancer.py
PROFILES["My_Sunset"] = PhotoProfile(
    name="Sunset Enhancement",
    hdr=60,
    brightness=5,
    contrast=15,
    saturation=35,
    warmth=25,  # Extra warm for golden hour
    shadows=20
)
```

Then use it from the command line:
```bash
python photo_enhancer.py -i photo.jpg -o enhanced.jpg -p My_Sunset
```

## Adjustment Parameters

All adjustment values and their ranges:

| Parameter | Range | Description |
|-----------|-------|-------------|
| HDR | 0-100 | Simulates HDR effect with detail enhancement |
| Brightness | -100 to +100 | Adjusts overall image brightness |
| Contrast | -100 to +100 | Adjusts difference between light and dark |
| White Point | 0-100 | Brightens highlights |
| Shadows | -100 to +100 | Lifts or deepens shadow areas |
| Saturation | -100 to +100 | Adjusts color intensity |
| Warmth | -100 to +100 | Negative = cooler (blue), Positive = warmer (orange/red) |

## Requirements

- Python 3.7+
- Pillow >= 10.0.0
- numpy >= 1.24.0
- tkinter (included with Python - needed for GUI only)

**Note:** tkinter comes pre-installed with most Python distributions. If you only use the CLI, tkinter is not required.

## Supported File Formats

The script supports the following image formats:
- JPEG (.jpg, .jpeg) - Full EXIF support
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

All formats are automatically detected when processing folders.

**EXIF Data Handling:**
- Automatically corrects orientation based on EXIF data (common with smartphone photos)
- Preserves camera metadata, timestamps, GPS location, and other EXIF information
- Removes orientation tag after applying the correction to prevent double-rotation

## File Structure

```
.
├── photo_enhancer.py        # Core enhancement functions & CLI
├── photo_enhancer_gui.py    # Desktop GUI application
├── run.py                   # Easy launcher (choose GUI or CLI)
├── requirements.txt         # Dependencies
├── README.md               # This file
├── photos/                 # Your input images
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
└── enhanced/               # Output folder (auto-created)
    ├── HDR_Boost/          # Subfolder per profile (auto-created)
    │   ├── photo1_enhanced.jpg
    │   ├── photo2_enhanced.jpg
    │   └── photo3_enhanced.jpg
    ├── Natural_Enhance/
    │   └── ...
    └── Vibrant/
        └── ...
```

## Tips for Best Results

1. **Start with good quality images** - Higher resolution input gives better output
2. **Use the GUI for beginners** - The desktop GUI is perfect if you're new to the tool
3. **Test profiles first** - Process a single image before batch processing entire folders
4. **Don't over-process** - Sometimes less is more; try Natural_Enhance profile first
5. **Save originals** - Always keep your original files
6. **Compare profiles** - Process the same folder with different profiles to see what works best
7. **Use CLI for automation** - The command line is perfect for scripts and automated workflows
8. **Use quiet mode for automation** - Add `--quiet` flag when using CLI in scripts
9. **Organize output** - The tool automatically creates subfolders for each profile (unless you use `--no-subfolder`)
10. **Create shortcuts** - Make desktop shortcuts for the GUI for quick access

## Troubleshooting

**GUI won't start / tkinter errors:**
- tkinter should come with Python, but on some Linux systems you may need to install it:
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
  - Arch: `sudo pacman -S tk`
- On macOS, ensure you're using the official Python from python.org (not Homebrew)

**Photos appear rotated incorrectly:**
- The script automatically handles EXIF orientation data from cameras and smartphones
- If issues persist, the original photo may have corrupted EXIF data
- Try opening and re-saving the original in a photo editor first

**"Error: Must specify either --input or --folder":**
- You need to provide either `-i` (single file) or `-f` (folder) argument

**"Error: Must specify --profile":**
- You must specify which profile to use with `-p` flag
- Run `--list-profiles` to see available options

**Image looks over-processed:**
- Try a more subtle profile like Natural_Enhance
- Create a custom profile with lower values

**Colors look unnatural:**
- Reduce saturation and warmth values in the profile
- Lower the HDR percentage

**"No images found in folder":**
- Ensure your folder contains supported image formats
- Check folder path is correct (use absolute paths if needed)

**Permission errors:**
- Ensure you have write permissions for the output folder
- On Linux/macOS, you might need to make the script executable: `chmod +x photo_enhancer.py`

## Shell Script Automation

Create a bash script to process with multiple profiles:

**process_all.sh (Linux/macOS):**
```bash
#!/bin/bash
for profile in HDR_Boost Natural_Enhance Vibrant Portrait
do
    echo "Processing with $profile..."
    python photo_enhancer.py -f photos -o enhanced -p $profile
done
echo "All profiles complete!"
```

**process_all.bat (Windows):**
```batch
@echo off
for %%p in (HDR_Boost Natural_Enhance Vibrant Portrait) do (
    echo Processing with %%p...
    python photo_enhancer.py -f photos -o enhanced -p %%p
)
echo All profiles complete!
```

Make executable and run:
```bash
chmod +x process_all.sh
./process_all.sh
```

## License

Free to use and modify for personal and commercial projects.

## Contributing

Feel free to create your own profiles and share them! To add a profile:
1. Edit the `PROFILES` dictionary in `photo_enhancer.py`
2. Create a new `PhotoProfile` with your desired settings
3. Test it on various images
4. Share your profile settings in the discussions!

## Quick Reference

### Easy Launcher
```bash
# Start with the launcher menu
python run.py

# Choose:
# 1 - GUI (visual interface)
# 2 - CLI (shows command examples)
# 3 - Exit
```

### GUI (Desktop Application)
```bash
# Launch the GUI
python photo_enhancer_gui.py

# Then use the visual interface to:
# 1. Select mode (Single/Folder)
# 2. Browse for input
# 3. Choose output location
# 4. Pick profile
# 5. Click "Start Processing"
```

### CLI (Command Line)
```bash
# Show all profiles
python photo_enhancer.py --list-profiles

# Single image
python photo_enhancer.py -i input.jpg -o output.jpg -p HDR_Boost

# Folder (with subfolders)
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost

# Folder (without subfolders)
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost --no-subfolder

# Quiet mode
python photo_enhancer.py -f photos -o enhanced -p Vibrant -q

# Help
python photo_enhancer.py --help
```

---

**Made with ❤️ for better photos**