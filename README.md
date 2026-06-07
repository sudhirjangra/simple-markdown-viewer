# Markdown Viewer

**Version:** 1.0.1  
**Author:** Sudhir Jangra  
**License:** MIT

Professional Markdown reader with live preview, GitHub-flavored styling, and outline navigation.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

## Features

- 📁 **File Browser** - Navigate markdown files with .md filtering
- 🎨 **GitHub CSS** - Beautiful rendering with dark/light themes
- 📑 **Outline Navigation** - Auto-generated table of contents
- 🔗 **Relative Links** - Full support for inter-document linking
- 🌓 **Theme Toggle** - Switch between dark and light modes
- ⚡ **Live Preview** - Instant rendering as you browse

## Installation

### Windows

Download `MarkdownViewer-Setup-1.0.1.exe` from [Releases](https://github.com/sudhirjangra/markdown-viewer/releases) and run installer.

Or use portable executable: `MarkdownViewer.exe`

### Arch Linux

```bash
# Download PKGBUILD or .pkg.tar.zst from releases
yay -S markdown-viewer
# Or install from package
sudo pacman -U markdown-viewer-1.0.1-1-any.pkg.tar.zst
```

### Debian/Ubuntu

```bash
# Download .deb from releases
sudo dpkg -i markdown-viewer_1.0.1_all.deb
sudo apt-get install -f  # Fix dependencies if needed
```

### From Source

```bash
git clone https://github.com/sudhirjangra/markdown-viewer.git
cd markdown-viewer
pip install PyQt6 PyQt6-WebEngine Markdown
python app.py
```

## Usage

Launch from application menu or run:
```bash
markdown-viewer
```

- Use **📁 Open Folder** to select markdown directory
- Click files in sidebar to preview
- Switch between **📁 Files** and **📑 Outline** tabs
- Toggle **🌓 Theme** for dark/light mode
- Click **ℹ️ About** for version info

## Development

Built with:
- Python 3.11+
- PyQt6
- PyQt6-WebEngine
- Python-Markdown

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Sudhir Jangra