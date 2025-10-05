#!/usr/bin/env python3
"""
Photo Enhancement CLI Tool
A command-line tool for batch photo enhancement with predefined profiles
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from pathlib import Path
import argparse
import sys


class PhotoProfile:
    """Define a photo enhancement profile"""

    def __init__(self, name, hdr=0, brightness=0, contrast=0, white_point=0,
                 shadows=0, saturation=0, warmth=0):
        self.name = name
        self.hdr = hdr  # 0-100
        self.brightness = brightness  # -100 to 100
        self.contrast = contrast  # -100 to 100
        self.white_point = white_point  # 0-100
        self.shadows = shadows  # -100 to 100
        self.saturation = saturation  # -100 to 100
        self.warmth = warmth  # -100 to 100


# Define your profiles
PROFILES = {
    "HDR_Boost": PhotoProfile(
        name="HDR Boost",
        hdr=100,
        brightness=10,
        contrast=10,
        white_point=5,
        shadows=25,
        saturation=25,
        warmth=10
    ),
    "Natural_Enhance": PhotoProfile(
        name="Natural Enhance",
        hdr=30,
        brightness=5,
        contrast=5,
        saturation=15,
        warmth=5
    ),
    "Vibrant": PhotoProfile(
        name="Vibrant",
        hdr=50,
        brightness=8,
        contrast=15,
        saturation=40,
        warmth=0
    ),
    "Portrait": PhotoProfile(
        name="Portrait",
        hdr=20,
        brightness=12,
        shadows=30,
        saturation=10,
        warmth=15
    )
}


def apply_brightness(img, value):
    """Apply brightness adjustment (-100 to 100)"""
    factor = 1 + (value / 100)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def apply_contrast(img, value):
    """Apply contrast adjustment (-100 to 100)"""
    factor = 1 + (value / 100)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def apply_saturation(img, value):
    """Apply saturation adjustment (-100 to 100)"""
    factor = 1 + (value / 100)
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)


def apply_warmth(img, value):
    """Apply warmth/temperature adjustment (-100 to 100)"""
    if value == 0:
        return img

    img_array = np.array(img, dtype=np.float32)

    # Positive value = warmer (more red/yellow), negative = cooler (more blue)
    factor = value / 100

    # Adjust red and blue channels
    img_array[:, :, 0] = np.clip(img_array[:, :, 0] * (1 + factor * 0.3), 0, 255)  # Red
    img_array[:, :, 2] = np.clip(img_array[:, :, 2] * (1 - factor * 0.3), 0, 255)  # Blue

    return Image.fromarray(img_array.astype(np.uint8))


def apply_shadows(img, value):
    """Lift shadows (-100 to 100)"""
    if value == 0:
        return img

    img_array = np.array(img, dtype=np.float32)

    # Create a mask for shadow areas (darker pixels)
    luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
    shadow_mask = np.clip(1 - (luminance / 128), 0, 1)

    # Apply shadow lift based on the mask
    adjustment = value * 0.5 * shadow_mask[:, :, np.newaxis]
    img_array = np.clip(img_array + adjustment, 0, 255)

    return Image.fromarray(img_array.astype(np.uint8))


def apply_white_point(img, value):
    """Adjust white point (0-100)"""
    if value == 0:
        return img

    img_array = np.array(img, dtype=np.float32)

    # Brighten highlights
    luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
    highlight_mask = np.clip((luminance - 128) / 128, 0, 1)

    adjustment = value * 0.5 * highlight_mask[:, :, np.newaxis]
    img_array = np.clip(img_array + adjustment, 0, 255)

    return Image.fromarray(img_array.astype(np.uint8))


def apply_hdr(img, value):
    """Apply HDR effect (0-100)"""
    if value == 0:
        return img

    # HDR simulation through tone mapping
    strength = value / 100

    # Apply detail enhancement
    img_detail = img.filter(ImageFilter.UnsharpMask(radius=2, percent=int(150 * strength)))

    # Reduce contrast slightly to compress dynamic range
    enhancer = ImageEnhance.Contrast(img_detail)
    img_compressed = enhancer.enhance(1 - 0.2 * strength)

    # Blend original with processed
    return Image.blend(img, img_compressed, strength)


def enhance_photo(input_path, output_path, profile_name, verbose=True):
    """Apply a profile to enhance a photo"""
    if profile_name not in PROFILES:
        raise ValueError(f"Profile '{profile_name}' not found. Available: {list(PROFILES.keys())}")

    profile = PROFILES[profile_name]

    # Load image
    img = Image.open(input_path)

    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')

    if verbose:
        print(f"Applying profile: {profile.name}")

    # Apply adjustments in order
    if profile.hdr != 0:
        img = apply_hdr(img, profile.hdr)
        if verbose:
            print(f"  - HDR: {profile.hdr}%")

    if profile.brightness != 0:
        img = apply_brightness(img, profile.brightness)
        if verbose:
            print(f"  - Brightness: {profile.brightness:+d}%")

    if profile.contrast != 0:
        img = apply_contrast(img, profile.contrast)
        if verbose:
            print(f"  - Contrast: {profile.contrast:+d}%")

    if profile.white_point != 0:
        img = apply_white_point(img, profile.white_point)
        if verbose:
            print(f"  - White Point: {profile.white_point}%")

    if profile.shadows != 0:
        img = apply_shadows(img, profile.shadows)
        if verbose:
            print(f"  - Shadows: {profile.shadows:+d}%")

    if profile.saturation != 0:
        img = apply_saturation(img, profile.saturation)
        if verbose:
            print(f"  - Saturation: {profile.saturation:+d}%")

    if profile.warmth != 0:
        img = apply_warmth(img, profile.warmth)
        if verbose:
            print(f"  - Warmth: {profile.warmth:+d}%")

    # Save the result
    img.save(output_path, quality=95)
    if verbose:
        print(f"\nSaved to: {output_path}")


def list_profiles():
    """Display all available profiles"""
    print("\nAvailable Profiles:")
    print("=" * 60)
    for name, profile in PROFILES.items():
        print(f"\n{name}: {profile.name}")
        print(f"  HDR: {profile.hdr}%, Brightness: {profile.brightness:+d}%")
        print(f"  Contrast: {profile.contrast:+d}%, Saturation: {profile.saturation:+d}%")
        print(f"  Shadows: {profile.shadows:+d}%, Warmth: {profile.warmth:+d}%")
        print(f"  White Point: {profile.white_point}%")
    print()


def enhance_folder(input_folder, output_folder, profile_name, create_subfolder=True, verbose=True):
    """
    Apply a profile to all images in a folder

    Args:
        input_folder: Path to folder containing images
        output_folder: Path to save enhanced images
        profile_name: Name of the profile to apply
        create_subfolder: If True, creates a subfolder named after the profile
        verbose: If True, prints detailed progress
    """
    if profile_name not in PROFILES:
        raise ValueError(f"Profile '{profile_name}' not found. Available: {list(PROFILES.keys())}")

    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        raise ValueError(f"Input folder '{input_folder}' does not exist")

    # Create output folder
    if create_subfolder:
        output_path = output_path / profile_name
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

    # Find all images in the folder
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))

    if not image_files:
        print(f"No images found in '{input_folder}'")
        return

    print(f"\nFound {len(image_files)} images to process")
    print(f"Profile: {PROFILES[profile_name].name}")
    print(f"Output folder: {output_path}")
    print("-" * 60)

    # Process each image
    success_count = 0
    for i, img_file in enumerate(image_files, 1):
        try:
            output_file = output_path / f"{img_file.stem}_enhanced{img_file.suffix}"
            print(f"\n[{i}/{len(image_files)}] Processing: {img_file.name}")

            enhance_photo(str(img_file), str(output_file), profile_name, verbose=verbose)
            success_count += 1

        except Exception as e:
            print(f"  ERROR: Failed to process {img_file.name}: {str(e)}")
            continue

    print("\n" + "=" * 60)
    print(f"Batch processing complete!")
    print(f"Successfully enhanced: {success_count}/{len(image_files)} images")
    print(f"Output location: {output_path}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Photo Enhancement CLI Tool - Enhance photos with predefined profiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # List all available profiles
  python photo_enhancer.py --list-profiles

  # Enhance a single photo
  python photo_enhancer.py -i photo.jpg -o enhanced.jpg -p HDR_Boost

  # Enhance all photos in a folder
  python photo_enhancer.py -f photos -o enhanced -p HDR_Boost

  # Enhance folder without creating subfolders
  python photo_enhancer.py -f photos -o enhanced -p Natural_Enhance --no-subfolder

  # Quiet mode (less output)
  python photo_enhancer.py -f photos -o enhanced -p Vibrant --quiet
        '''
    )

    parser.add_argument('-i', '--input',
                        help='Input image file')
    parser.add_argument('-o', '--output',
                        help='Output image file or folder')
    parser.add_argument('-f', '--folder',
                        help='Input folder containing images to process')
    parser.add_argument('-p', '--profile',
                        choices=list(PROFILES.keys()),
                        help='Enhancement profile to apply')
    parser.add_argument('--list-profiles',
                        action='store_true',
                        help='List all available profiles')
    parser.add_argument('--no-subfolder',
                        action='store_true',
                        help='Do not create profile subfolders when processing folders')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Quiet mode - minimal output')

    args = parser.parse_args()

    # Handle list profiles
    if args.list_profiles:
        list_profiles()
        return 0

    # Validate arguments
    if args.folder and args.input:
        print("Error: Cannot use both --input and --folder at the same time")
        return 1

    if not args.folder and not args.input:
        print("Error: Must specify either --input or --folder")
        parser.print_help()
        return 1

    if not args.profile:
        print("Error: Must specify --profile")
        parser.print_help()
        return 1

    if not args.output:
        print("Error: Must specify --output")
        return 1

    verbose = not args.quiet

    try:
        # Process folder
        if args.folder:
            enhance_folder(
                args.folder,
                args.output,
                args.profile,
                create_subfolder=not args.no_subfolder,
                verbose=verbose
            )
        # Process single file
        else:
            enhance_photo(args.input, args.output, args.profile, verbose=verbose)

        return 0

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())