"""
Check and report the status of VisionCraft assets
"""
import os
from pathlib import Path

# Define directories
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static'
IMAGES_DIR = STATIC_DIR / 'images'
MODELS_DIR = STATIC_DIR / 'models'
AVATARS_DIR = STATIC_DIR / 'avatars'

def format_size(bytes):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def check_directory(directory, extensions=None):
    """Check a directory and return file info"""
    if not directory.exists():
        return []
    
    files = []
    for file in directory.iterdir():
        if file.is_file():
            if extensions is None or file.suffix.lower() in extensions:
                size = file.stat().st_size
                files.append({
                    'name': file.name,
                    'size': size,
                    'size_formatted': format_size(size),
                    'path': str(file)
                })
    
    return sorted(files, key=lambda x: x['name'])

def print_section(title, files, total_size):
    """Print a section with files"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    
    if not files:
        print("  ⚠️  No files found")
        return
    
    print(f"  Total: {len(files)} files | Size: {format_size(total_size)}\n")
    
    for file in files:
        status = "✓" if file['size'] > 0 else "⚠"
        print(f"  {status} {file['name']:<40} {file['size_formatted']:>10}")

def main():
    """Main check function"""
    print("\n" + "="*70)
    print("  VisionCraft Asset Status Report")
    print("="*70)
    
    # Check Images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    images = check_directory(IMAGES_DIR, image_extensions)
    images_total = sum(f['size'] for f in images)
    print_section("📷 IMAGES (static/images/)", images, images_total)
    
    # Check Models
    model_extensions = {'.glb', '.gltf'}
    models = check_directory(MODELS_DIR, model_extensions)
    models_total = sum(f['size'] for f in models)
    print_section("🎨 3D MODELS (static/models/)", models, models_total)
    
    # Check Avatars
    avatar_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    avatars = check_directory(AVATARS_DIR, avatar_extensions)
    avatars_total = sum(f['size'] for f in avatars)
    print_section("👤 AVATARS (static/avatars/)", avatars, avatars_total)
    
    # Summary
    total_assets = len(images) + len(models) + len(avatars)
    total_size = images_total + models_total + avatars_total
    
    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")
    print(f"  Total Assets: {total_assets} files")
    print(f"  Total Size: {format_size(total_size)}")
    print(f"  Images: {len(images)} files ({format_size(images_total)})")
    print(f"  Models: {len(models)} files ({format_size(models_total)})")
    print(f"  Avatars: {len(avatars)} files ({format_size(avatars_total)})")
    print(f"{'='*70}\n")
    
    # Recommendations
    print("💡 RECOMMENDATIONS:")
    
    if len(images) < 10:
        print("  • Consider adding more product images for better user experience")
    
    if len(models) < len(images):
        print("  • Some products are missing 3D models for AR viewing")
    
    if models_total > 50 * 1024 * 1024:  # 50MB
        print("  • Consider optimizing 3D models - total size is quite large")
    
    print("\n📚 For more information, see ASSETS_GUIDE.md\n")

if __name__ == '__main__':
    main()
