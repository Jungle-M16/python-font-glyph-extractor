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
from fontTools.pens.transformPen import TransformPen
import re

def sanitize_filename(name):
    # Remove invalid filename characters
    return re.sub(r'[<>:"/\\|?*]', '_', name)

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
        
        # Get glyph set and Unicode cmap
        glyph_set = font.getGlyphSet()
        cmap = font['cmap'].getBestCmap()
        unicode_to_glyph = {v: k for k, v in cmap.items()}
        
        # Keep track of used filenames to avoid duplicates
        used_filenames = set()
        
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
                
                # Generate SVG path data with Y-axis flipped
                pen = SVGPathPen(glyph_set)
                transform = (1, 0, 0, -1, 0, 0)  # Flip Y-axis
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                svg_path = pen.getCommands()
                
                # Adjust viewBox for flipped Y-axis
                new_min_y = -max_y
                
                # Construct a unique filename
                # Attempt to use Unicode code point if available
                unicode_values = [code for code, name in unicode_to_glyph.items() if name == glyph_name]
                if unicode_values:
                    # Use the first Unicode value if multiple are present
                    unicode_value = unicode_values[0]
                    # Format Unicode value as 'U+XXXX'
                    unicode_str = f"U+{unicode_value:04X}"
                    filename_base = f"{unicode_str}_{glyph_name}"
                else:
                    # If no Unicode mapping, use glyph name and index
                    filename_base = f"{glyph_name}"
                
                # Sanitize filename
                filename_base = sanitize_filename(filename_base)
                
                # Ensure filename is unique
                filename = filename_base
                counter = 1
                while filename.lower() in used_filenames:
                    filename = f"{filename_base}_{counter}"
                    counter += 1
                used_filenames.add(filename.lower())
                
                svg_filename = os.path.join(output_dir, f"{filename}.svg")
                
                # Create SVG content
                svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {new_min_y} {width} {height}" width="{width}" height="{height}">
<path d="{svg_path}"/>
</svg>'''
                
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
