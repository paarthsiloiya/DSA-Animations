# MP4 to GIF Converter

This Python script converts all MP4 files in 480p15fps folders to GIF format, specifically targeting the lower resolution files and ignoring high-resolution ones.

## Features

- Automatically finds all MP4 files in `480p15` folders
- Converts MP4 files to optimized GIF format
- Customizable frame rate and resize options
- Progress bar during conversion
- Dry-run mode to preview what will be converted
- Skip files that are already converted

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_converter.txt
```

## Usage

### Basic Usage
Convert all 480p15fps MP4 files to GIFs and save them in organized folders within the `gifs` directory:
```bash
python mp4_to_gif_converter.py
```

This will create a folder structure like:
```
gifs/
├── Arrays/
│   ├── Indexing.gif
│   ├── MemoryAllocation.gif
│   └── ...
├── Trees/
│   ├── BinarySearchTreeDeletion.gif
│   ├── TreeExplanation.gif
│   └── ...
├── Graphs/
│   ├── Dijkstra.gif
│   ├── BellmanFord.gif
│   └── ...
└── ...

### Advanced Usage

**Specify a different root directory:**
```bash
python mp4_to_gif_converter.py --root-dir "path/to/your/videos"
```

**Save GIFs to a specific output directory:**
```bash
python mp4_to_gif_converter.py --output-dir "my_custom_gifs"
```

**Save GIFs in the same directories as the MP4 files:**
```bash
python mp4_to_gif_converter.py --output-dir ""
```

**Adjust frame rate (default is 10 FPS):**
```bash
python mp4_to_gif_converter.py --fps 15
```

**Resize GIFs (0.5 = half size, 2.0 = double size):**
```bash
python mp4_to_gif_converter.py --resize 0.8
```

**Dry run to see what files would be converted:**
```bash
python mp4_to_gif_converter.py --dry-run
```

**Combine multiple options:**
```bash
python mp4_to_gif_converter.py --fps 12 --resize 0.7 --output-dir "gifs"
```

### Windows Batch Script

For Windows users, you can simply double-click `convert_mp4_to_gif.bat` to install dependencies and run the conversion with default settings.

## Command Line Options

- `--root-dir`: Root directory containing MP4 files (default: `Animations/media/videos`)
- `--output-dir`: Output directory for GIF files (default: `gifs` folder in current directory)
- `--fps`: Frames per second for output GIFs (default: 10)
- `--resize`: Resize factor for GIFs (default: 1.0 = original size)
- `--dry-run`: Show what files would be converted without actually converting

## Example Output

```
Searching for 480p15fps MP4 files in: D:\Git-Projects\DSA-Animations\Animations\media\videos
Found 73 MP4 files to convert:
  - D:\Git-Projects\DSA-Animations\Animations\media\videos\Arrays\480p15\Indexing.mp4
  - D:\Git-Projects\DSA-Animations\Animations\media\videos\Trees\480p15\BinarySearchTreeDeletion.mp4
  ...

Starting conversion with 10 FPS and 1.0x resize factor...
Converting MP4s to GIFs: 100%|████████████| 73/73 [05:42<00:00,  4.69s/it]

Conversion complete!
Successfully converted: 73/73 files
```

## Notes

- The script only processes MP4 files in folders named `480p15` to avoid converting high-resolution files
- If a GIF already exists, it will be skipped to avoid unnecessary re-conversion
- The default frame rate of 10 FPS provides a good balance between file size and quality
- You can adjust the resize factor to make smaller GIFs if needed for web usage