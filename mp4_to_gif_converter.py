#!/usr/bin/env python3
"""
MP4 to GIF Converter
This script converts all MP4 files in 480p15fps folders to GIF format.
It specifically targets the lower resolution files and ignores high-resolution ones.
"""

import os
import glob
from pathlib import Path
from moviepy import VideoFileClip
import argparse
from tqdm import tqdm

def find_480p_mp4_files(root_dir):
    """
    Find all MP4 files in 480p15 folders within the given root directory.
    
    Args:
        root_dir (str): Root directory to search for MP4 files
        
    Returns:
        list: List of paths to 480p15fps MP4 files
    """
    mp4_files = []
    
    # Search for all MP4 files in 480p15 folders
    pattern = os.path.join(root_dir, "**", "480p15", "*.mp4")
    mp4_files = glob.glob(pattern, recursive=True)
    
    return mp4_files

def convert_mp4_to_gif(mp4_path, output_dir=None, fps=10, resize_factor=1.0):
    """
    Convert a single MP4 file to GIF format.
    
    Args:
        mp4_path (str): Path to the input MP4 file
        output_dir (str): Directory to save the GIF file (optional)
        fps (int): Frames per second for the output GIF
        resize_factor (float): Factor to resize the video (1.0 = original size)
        
    Returns:
        str: Path to the created GIF file or None if conversion failed
    """
    try:
        # Create output directory structure
        if output_dir:
            # Extract the relative path structure from the MP4 path
            # Example: Arrays/480p15/Indexing.mp4 -> Arrays/Indexing.gif
            path_parts = Path(mp4_path).parts
            
            # Find the index of the category folder (Arrays, Trees, etc.)
            category_idx = -1
            for i, part in enumerate(path_parts):
                if part in ['Arrays', 'Trees', 'Graphs', 'LinkedList', 'SortingAlgoritms', 
                           'SearchingAlgorithms', 'Stack-Queue', 'AVLTree', 'BTrees', 
                           'DivideAndConquer', 'Greedy']:
                    category_idx = i
                    break
            
            if category_idx >= 0:
                # Create category subfolder in output directory
                category = path_parts[category_idx]
                category_output_dir = os.path.join(output_dir, category)
                os.makedirs(category_output_dir, exist_ok=True)
                gif_path = os.path.join(category_output_dir, Path(mp4_path).stem + ".gif")
            else:
                # Fallback: just put in main output directory
                os.makedirs(output_dir, exist_ok=True)
                gif_path = os.path.join(output_dir, Path(mp4_path).stem + ".gif")
        else:
            # Save GIF in the same directory as the MP4
            gif_path = Path(mp4_path).with_suffix(".gif")
        
        # Skip if GIF already exists
        if os.path.exists(gif_path):
            print(f"GIF already exists: {gif_path}")
            return gif_path
        
        # Load video clip
        clip = VideoFileClip(mp4_path)

        try:
            # Resize if needed
            if resize_factor != 1.0:
                clip = clip.resized(resize_factor)

            # Convert to GIF
            clip.write_gif(gif_path, fps=fps)
        finally:
            # Close the clip to free memory
            clip.close()
        
        print(f"Converted: {mp4_path} -> {gif_path}")
        return gif_path
        
    except Exception as e:
        print(f"Error converting {mp4_path}: {str(e)}")
        return None

def main():
    """Main function to convert all 480p15fps MP4 files to GIFs."""
    parser = argparse.ArgumentParser(description="Convert 480p15fps MP4 files to GIF format")
    parser.add_argument("--root-dir", default="Animations/media/videos", 
                       help="Root directory containing MP4 files (default: Animations/media/videos)")
    parser.add_argument("--output-dir", default="gifs",
                       help="Output directory for GIF files (default: gifs folder in current directory)")
    parser.add_argument("--fps", type=int, default=10,
                       help="Frames per second for output GIFs (default: 10)")
    parser.add_argument("--resize", type=float, default=1.0,
                       help="Resize factor for GIFs (default: 1.0 = original size)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what files would be converted without actually converting")
    
    args = parser.parse_args()
    
    # Get absolute path
    root_dir = os.path.abspath(args.root_dir)
    
    if not os.path.exists(root_dir):
        print(f"Error: Root directory '{root_dir}' does not exist!")
        return
    
    # Find all 480p15fps MP4 files
    print(f"Searching for 480p15fps MP4 files in: {root_dir}")
    mp4_files = find_480p_mp4_files(root_dir)
    
    if not mp4_files:
        print("No 480p15fps MP4 files found!")
        return
    
    print(f"Found {len(mp4_files)} MP4 files to convert:")
    for file in mp4_files:
        print(f"  - {file}")
    
    if args.dry_run:
        print("\nDry run mode - no files will be converted.")
        return
    
    # Convert each MP4 to GIF
    print(f"\nStarting conversion with {args.fps} FPS and {args.resize}x resize factor...")
    successful_conversions = 0
    
    for mp4_file in tqdm(mp4_files, desc="Converting MP4s to GIFs"):
        result = convert_mp4_to_gif(
            mp4_file, 
            output_dir=args.output_dir,
            fps=args.fps,
            resize_factor=args.resize
        )
        if result:
            successful_conversions += 1
    
    print(f"\nConversion complete!")
    print(f"Successfully converted: {successful_conversions}/{len(mp4_files)} files")

if __name__ == "__main__":
    main()