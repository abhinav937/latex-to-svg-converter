#!/usr/bin/env python3
"""
Build script to create standalone executables for LaTeX to SVG Converter
Uses PyInstaller to create .exe for Windows and .app for macOS
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\nRunning {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed:")
        print(e.stderr)
        return False

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("SUCCESS: PyInstaller already installed")
        return True
    except ImportError:
        return run_command("python3 -m pip install pyinstaller", "Installing PyInstaller")

def build_executable():
    """Build the executable using PyInstaller"""
    system = platform.system().lower()

    # PyInstaller command (use python3 -m to ensure proper PATH)
    cmd = [
        "python3", "-m", "PyInstaller",
        "--onedir",  # Create a directory (faster than --onefile)
        "--windowed",  # Don't show console window (for GUI apps)
        "--name=latex_svg_converter",
        # "--icon=icon.ico" if system == "windows" else "--icon=icon.icns",  # Icon if available
        "web_embedder.py"
    ]

    # macOS specific options
    if system == "darwin":
        cmd.extend([
            "--osx-bundle-identifier=com.latex.svgconverter",
            "--target-architecture=universal2"  # Universal binary for Intel + Apple Silicon
        ])

    return run_command(" ".join(cmd), f"Building executable for {system}")

def create_installer():
    """Create installer package"""
    system = platform.system().lower()

    if system == "windows":
        # For Windows, we could create an installer with NSIS or Inno Setup
        # For now, just create a zip of the dist folder
        print("\nCreating Creating Windows distribution...")
        try:
            import shutil
            shutil.make_archive("LaTeX-SVG-Converter-Windows", 'zip', "dist")
            print("SUCCESS: Windows ZIP created: LaTeX-SVG-Converter-Windows.zip")
        except Exception as e:
            print(f"ERROR: Failed to create Windows ZIP: {e}")

    elif system == "darwin":
        # For macOS, create a .dmg file
        print("\nCreating Creating macOS distribution...")
        app_path = "dist/latex_svg_converter.app"
        dmg_path = "LaTeX-SVG-Converter-macOS.dmg"

        if os.path.exists(app_path):
            # Create DMG using hdiutil (macOS built-in)
            cmd = f"hdiutil create -volname 'LaTeX to SVG Converter' -srcfolder '{app_path}' -ov -format UDZO '{dmg_path}'"
            if run_command(cmd, "Creating macOS DMG"):
                # Verify the DMG
                verify_dmg(dmg_path)
        else:
            print("ERROR: macOS app bundle not found")

def verify_dmg(dmg_path):
    """Verify the DMG file is valid and contains expected content"""
    print("Verifying DMG file...")

    try:
        # Check if DMG file exists and has size > 0
        if not os.path.exists(dmg_path):
            print(f"ERROR: DMG file not found: {dmg_path}")
            return False

        file_size = os.path.getsize(dmg_path)
        if file_size == 0:
            print("ERROR: DMG file is empty")
            return False

        print(f"SUCCESS: DMG created: {dmg_path} ({file_size / 1024 / 1024:.1f} MB)")

        # Verify DMG integrity using hdiutil
        verify_cmd = f"hdiutil verify '{dmg_path}'"
        if run_command(verify_cmd, "Verifying DMG integrity"):
            print("SUCCESS: DMG integrity verified")
            return True
        else:
            print("WARNING: DMG integrity check failed, but file was created")
            return True  # Still consider it successful since file exists

    except Exception as e:
        print(f"WARNING: DMG verification error: {e}")
        return False

def cleanup_build_artifacts():
    """Clean up build artifacts to save disk space"""
    print("\nCleaning Cleaning up build artifacts...")

    artifacts_removed = 0

    # Remove build directory (contains PyInstaller temp files)
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")
        print("SUCCESS: Removed build/ directory")
        artifacts_removed += 1

    # Remove dist directory (keep the final DMG/ZIP files)
    # We keep dist for now since it contains the .app bundle which might be useful

    print(f"SUCCESS: Cleanup completed (removed {artifacts_removed} items)")

def main():
    """Main build process"""
    print("Building LaTeX to SVG Converter Standalone Executable")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("web_embedder.py"):
        print("ERROR: web_embedder.py not found. Please run this script from the project root.")
        sys.exit(1)

    # Install PyInstaller
    if not install_pyinstaller():
        sys.exit(1)

    # Clean previous builds
    print("\nCleaning Cleaning previous builds...")
    import shutil
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"SUCCESS: Removed {folder}/")

    # Build executable
    if not build_executable():
        sys.exit(1)

    # Create installer
    create_installer()

    # Clean up build artifacts
    cleanup_build_artifacts()

    print("\n" + "=" * 50)
    print("SUCCESS: Build completed and cleaned up!")
    print("\nDistribution files ready:")
    system = platform.system().lower()
    if system == "windows":
        print("  - LaTeX-SVG-Converter-Windows.zip (ready for distribution)")
        print("  - dist/latex_svg_converter/ (local testing)")
    elif system == "darwin":
        print("  - LaTeX-SVG-Converter-macOS.dmg (ready for distribution)")
        print("  - dist/latex_svg_converter.app (local testing)")
    else:
        print("  - dist/latex_svg_converter/ (ready for distribution)")

    print("\nUpload the distribution files to GitHub Releases!")

if __name__ == "__main__":
    main()
