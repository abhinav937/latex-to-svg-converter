# LaTeX to SVG Converter

Convert LaTeX mathematical equations to SVG format.

![LaTeX to SVG Icon](icon.svg)

## Installation

### Standalone Application (Recommended)
Download pre-built executables from the [Releases](https://github.com/abhinav937/latex-to-svg-converter/releases) page.

#### Windows
1. Download `LaTeX-SVG-Converter-Windows.zip`
2. Extract the ZIP file
3. Run `Latex_to_SVG.exe`

#### macOS
1. Download `LaTeX-SVG-Converter-macOS.dmg`
2. Double-click the DMG file to mount it
3. **Important**: macOS may show a security warning. Go to **System Settings** → **Privacy & Security** and click **"Open Anyway"** next to the blocked application
4. Drag the `Latex_to_SVG` app to your **Applications** folder
5. Launch the app from Applications

#### Linux
1. Download `Latex_to_SVG-linux.tar.gz`
2. Extract the tar.gz file: `tar -xzf Latex_to_SVG-linux.tar.gz`
3. Run the executable: `./Latex_to_SVG`

## Usage

Run the downloaded executable or use Python:

```bash
python3 web_embedder.py
```

## Requirements

- Python 3.8+ (if running from source)
- PySide6: `pip install PySide6`

## License

Built with PySide6 (LGPL) and Qt WebEngine (Chromium-based).
