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
