# Photo Enhancement CLI Tool

A command-line tool for photo enhancement with predefined profiles for quick and professional photo improvements.

## Features

- **CLI-based tool** - Easy to use from the command line
- **Profile-based enhancement system** - Apply consistent edits with a single command
- **Batch processing** - Process entire folders of images at once
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

### List Available Profiles
```bash
python photo_enhancer.py --list-profiles
```

### Enhance a Single Photo
```bash
python photo_enhancer.py -i photo.jpg -o enhanced.jpg -p HDR_Boost
```

### Enhance All Photos in a Folder
```bash
python photo_enhancer.py -f photos -o enhanced -p HDR_Boost
```

### Quiet Mode (Minimal Output)
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

## Supported File Formats

The script supports the following image formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

All formats are automatically detected when processing folders.

## File Structure

```
.
├── photo_enhancer.py    # Main CLI script
├── requirements.txt     # Dependencies
├── README.md           # This file
├── photos/             # Your input images
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
└── enhanced/           # Output folder (auto-created by CLI)
    ├── HDR_Boost/      # Subfolder per profile (auto-created)
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
2. **Test profiles first** - Process a single image before batch processing entire folders
3. **Don't over-process** - Sometimes less is more; try Natural_Enhance profile first
4. **Save originals** - Always keep your original files
5. **Compare profiles** - Process the same folder with different profiles to see what works best
6. **Use quiet mode for automation** - Add `--quiet` flag when using in scripts
7. **Organize output** - The script automatically creates subfolders for each profile (unless you use `--no-subfolder`)
8. **Shell scripts** - Create bash/batch scripts to process with multiple profiles automatically

## Troubleshooting

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