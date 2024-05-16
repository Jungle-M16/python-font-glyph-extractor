"""
This script extracts glyphs from a WOFF2 font file and saves them as individual SVG files.

Usage:
    python extract_glyphs.py <path_to_woff_file> <output_directory>

Arguments:
    <path_to_woff_file>   Path to the input WOFF2 font file.
    <output_directory>    Path to the directory where the SVG files will be saved.

Dependencies:
    - fontTools (install with `pip install fonttools`)
    - brotli (install with `pip install brotli`)

Description:
    This script loads a WOFF2 font file and extracts each glyph from the 'glyf' table.
    For each glyph, it calculates the bounding box to properly adjust the SVG canvas size
    and avoids clipping. The glyphs are then saved as individual SVG files in the specified
    output directory.

Functions:
    extract_glyphs_to_svg(woff_path, output_dir)
        Loads the WOFF2 file, extracts glyphs, and saves them as SVG files.

Example:
    python extract_glyphs.py path/to/your/font.woff2 path/to/output/directory

Author:
    Ari Björn Ólafsson

Date:
    May 16th 2024 
"""

import sys
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen


def extract_glyphs_to_svg(woff_path, output_dir):
    try:
        # Load the font
        font = TTFont(woff_path)
        
        # Ensure 'glyf' table is present
        if 'glyf' not in font:
            print("No 'glyf' table found in the WOFF file.")
            return
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Get glyph set
        glyph_set = font.getGlyphSet()
        
        # Extract each glyph and save as SVG
        for glyph_name in glyph_set.keys():
            glyph = glyph_set[glyph_name]
            
            # Calculate bounding box
            bounds_pen = BoundsPen(glyph_set)
            glyph.draw(bounds_pen)
            bounds = bounds_pen.bounds
            
            if bounds:
                min_x, min_y, max_x, max_y = bounds
                width = max_x - min_x
                height = max_y - min_y
                
                # Generate SVG path data
                pen = SVGPathPen(glyph_set)
                glyph.draw(pen)
                svg_path = pen.getCommands()
                
                # Create SVG content
                svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="{width}" height="{height}">\n<path d="{svg_path}"/>\n</svg>'
                svg_filename = os.path.join(output_dir, f"{glyph_name}.svg")
                
                # Save SVG file
                with open(svg_filename, 'w') as svg_file:
                    svg_file.write(svg_content)
                
                print(f"Extracted glyph '{glyph_name}' to '{svg_filename}'")
    
    except Exception as e:
        print(f"Error reading WOFF file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_glyphs.py <path_to_woff_file> <output_directory>")
    else:
        woff_path = sys.argv[1]
        output_dir = sys.argv[2]
        extract_glyphs_to_svg(woff_path, output_dir)
