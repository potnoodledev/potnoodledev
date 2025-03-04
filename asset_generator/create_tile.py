#!/usr/bin/env python3
"""
Universal Tile Generator - Creates 32x32 pixel seamless tiles for various terrain types.
This script uses the game_asset_generator module to create pixel art tiles with repeating patterns,
transitions between different terrain types, and proper square L-shaped corner tiles for terrain features.
"""

from game_asset_generator import generate_pixel_art
import os
from dotenv import load_dotenv
import time
import argparse

# Load environment variables from .env file
load_dotenv()

def generate_tile(tile_type, size=32, output_dir="tiles", seed=None, transition_to=None, 
                 transition_direction=None, corner_type=None):
    """
    Generate a pixel art tile with a repeating pattern, transition, or corner.
    
    Args:
        tile_type (str): Type of tile to generate (e.g., grass, sand, water, stone)
        size (int): Size of the tile in pixels (default: 32)
        output_dir (str): Directory to save the tile in
        seed (int, optional): Seed for reproducibility
        transition_to (str, optional): Second terrain type for transition tiles
        transition_direction (str, optional): Direction of transition ('left_to_right', 'right_to_left', 
                                             'top_to_bottom', 'bottom_to_top')
        corner_type (str, optional): Type of corner ('top_left', 'top_right', 'bottom_left', 'bottom_right')
        
    Returns:
        str: Path to the generated tile
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Base description for all tiles
    base_description = f"{size}x{size} pixel art {tile_type} tile with repeating pattern, top-down view, seamless tileable texture, pixel art style"
    
    # Customize description based on tile type
    tile_descriptions = {
        "grass": f"{base_description}, green grass texture, short grass blades",
        "sand": f"{base_description}, beige sand texture, fine grain sand",
        "water": f"{base_description}, blue water texture, small ripples",
        "stone": f"{base_description}, gray stone texture, small cracks",
        "dirt": f"{base_description}, brown dirt texture, small soil particles",
        "snow": f"{base_description}, white snow texture, small snowflakes",
        "lava": f"{base_description}, orange and red lava texture, small bubbles",
        "wood": f"{base_description}, brown wood texture, wood grain pattern",
        "ice": f"{base_description}, light blue ice texture, small cracks",
        "mud": f"{base_description}, dark brown mud texture, small puddles"
    }
    
    # Handle transition tiles
    if transition_to and transition_direction:
        # Get descriptions for both terrain types
        from_desc = tile_descriptions.get(tile_type.lower(), f"{base_description}")
        to_desc = tile_descriptions.get(transition_to.lower(), f"{size}x{size} pixel art {transition_to} tile with repeating pattern")
        
        # Create transition description based on direction
        direction_text = {
            "left_to_right": f"gradual transition from {tile_type} on the left to {transition_to} on the right",
            "right_to_left": f"gradual transition from {tile_type} on the right to {transition_to} on the left",
            "top_to_bottom": f"gradual transition from {tile_type} on the top to {transition_to} on the bottom",
            "bottom_to_top": f"gradual transition from {tile_type} on the bottom to {transition_to} on the top"
        }
        
        transition_text = direction_text.get(transition_direction, f"transition from {tile_type} to {transition_to}")
        description = f"{size}x{size} pixel art terrain transition tile, {transition_text}, seamless tileable texture, pixel art style"
        
        # Set output path for transition tile
        output_path = os.path.join(output_dir, f"{tile_type}_to_{transition_to}_{transition_direction}_{int(time.time())}.png")
        
        print(f"\nGenerating {size}x{size} pixel transition tile from {tile_type} to {transition_to} ({transition_direction})...")
    
    # Handle corner tiles
    elif corner_type:
        if not transition_to:
            raise ValueError("For corner tiles, you must specify a transition_to terrain type")
        
        # For these descriptions, we're assuming:
        # - tile_type is the main terrain (like grass/land)
        # - transition_to is the secondary terrain (like water for a pond)
        
        # Create specific descriptions for water-grass corners since they're common
        if (tile_type.lower() == "grass" and transition_to.lower() == "water"):
            corner_text = {
                "top_left": f"square corner of a pond or lake, with water forming a perfect right-angled L-shape in the top left corner and grass filling the rest, with a dark brown/purple border 1-2 pixels wide between grass and water, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "top_right": f"square corner of a pond or lake, with water forming a perfect right-angled L-shape in the top right corner and grass filling the rest, with a dark brown/purple border 1-2 pixels wide between grass and water, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "bottom_left": f"square corner of a pond or lake, with water forming a perfect right-angled L-shape in the bottom left corner and grass filling the rest, with a dark brown/purple border 1-2 pixels wide between grass and water, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "bottom_right": f"square corner of a pond or lake, with water forming a perfect right-angled L-shape in the bottom right corner and grass filling the rest, with a dark brown/purple border 1-2 pixels wide between grass and water, hard edge with NO diagonal transition, NO gradient, NO V-shape"
            }
            description = f"{size}x{size} pixel art terrain corner tile, {corner_text.get(corner_type, '')}, seamless tileable texture, pixel art style, clear distinct square corner boundary with hard edges"
        
        # For water-sand (beach) corners
        elif (tile_type.lower() == "sand" and transition_to.lower() == "water"):
            corner_text = {
                "top_left": f"square corner of a beach, with water forming a perfect right-angled L-shape in the top left corner and sand filling the rest, with a darker wet sand border 1-2 pixels wide between sand and water, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "top_right": f"square corner of a beach, with water forming a perfect right-angled L-shape in the top right corner and sand filling the rest, with a darker wet sand border 1-2 pixels wide between sand and water, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "bottom_left": f"square corner of a beach, with water forming a perfect right-angled L-shape in the bottom left corner and sand filling the rest, with a darker wet sand border 1-2 pixels wide between sand and water, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "bottom_right": f"square corner of a beach, with water forming a perfect right-angled L-shape in the bottom right corner and sand filling the rest, with a darker wet sand border 1-2 pixels wide between sand and water, hard edge with NO diagonal transition, NO gradient, NO V-shape"
            }
            description = f"{size}x{size} pixel art terrain corner tile, {corner_text.get(corner_type, '')}, seamless tileable texture, pixel art style, clear distinct square corner boundary with hard edges"
        
        # Generic corner description for other terrain combinations
        else:
            corner_text = {
                "top_left": f"square corner where {transition_to} meets {tile_type}, with {transition_to} forming a perfect right-angled L-shape in the top left corner and {tile_type} filling the rest, with a dark border 1-2 pixels wide between them, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "top_right": f"square corner where {transition_to} meets {tile_type}, with {transition_to} forming a perfect right-angled L-shape in the top right corner and {tile_type} filling the rest, with a dark border 1-2 pixels wide between them, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "bottom_left": f"square corner where {transition_to} meets {tile_type}, with {transition_to} forming a perfect right-angled L-shape in the bottom left corner and {tile_type} filling the rest, with a dark border 1-2 pixels wide between them, hard edge with NO diagonal transition, NO gradient, NO V-shape",
                "bottom_right": f"square corner where {transition_to} meets {tile_type}, with {transition_to} forming a perfect right-angled L-shape in the bottom right corner and {tile_type} filling the rest, with a dark border 1-2 pixels wide between them, hard edge with NO diagonal transition, NO gradient, NO V-shape"
            }
            description = f"{size}x{size} pixel art terrain corner tile, {corner_text.get(corner_type, '')}, seamless tileable texture, pixel art style, clear distinct square corner boundary with hard edges"
        
        # Set output path for corner tile
        output_path = os.path.join(output_dir, f"{tile_type}_with_{transition_to}_{corner_type}_{int(time.time())}.png")
        
        print(f"\nGenerating {size}x{size} pixel corner tile of {tile_type} with {transition_to} ({corner_type})...")
    
    # Handle regular tiles
    else:
        # Use the specific description if available, otherwise use the tile_type with the base description
        description = tile_descriptions.get(tile_type.lower(), base_description)
        
        # Set output path for regular tile
        output_path = os.path.join(output_dir, f"{tile_type.lower()}_tile_{int(time.time())}.png")
        
        print(f"\nGenerating {size}x{size} pixel {tile_type} tile...")
    
    # Negative prompt to avoid unwanted elements
    negative = "borders, edges, flowers, rocks, paths, animals, insects, people, text, signature, watermark"
    
    # Add specific negative prompts based on tile type
    if tile_type.lower() == "grass" and not (transition_to or corner_type):
        negative += ", dirt, soil"
    elif tile_type.lower() == "sand" and not (transition_to or corner_type):
        negative += ", shells, footprints, grass"
    elif tile_type.lower() == "water" and not (transition_to or corner_type):
        negative += ", fish, boats, land"
    
    # For corner tiles, we want a clear boundary but not diagonal
    if corner_type:
        negative += ", blurry edges, gradient transitions, fuzzy boundaries, diagonal split, V-shape, diagonal line, diagonal boundary, diagonal transition"
    
    # Generate the tile
    tile_path = generate_pixel_art(
        description=description,
        width=size,
        height=size,
        output_path=output_path,
        negative_description=negative,
        shading="basic shading",
        detail="low detail",
        view="high top-down",
        no_background=False,
        seed=seed
    )
    
    return tile_path

def main():
    """Generate a pixel art tile based on command line arguments."""
    parser = argparse.ArgumentParser(description="Generate a pixel art tile with a repeating pattern, transition, or corner.")
    parser.add_argument("tile_type", help="Type of tile to generate (e.g., grass, sand, water, stone)")
    parser.add_argument("--size", type=int, default=32, help="Size of the tile in pixels (default: 32)")
    parser.add_argument("--output-dir", default="tiles", help="Directory to save the tile in (default: tiles)")
    parser.add_argument("--seed", type=int, help="Seed for reproducibility")
    
    # Add transition and corner arguments
    parser.add_argument("--transition-to", help="Second terrain type for transition tiles")
    parser.add_argument("--transition-direction", choices=["left_to_right", "right_to_left", "top_to_bottom", "bottom_to_top"], 
                        help="Direction of transition")
    parser.add_argument("--corner-type", choices=["top_left", "top_right", "bottom_left", "bottom_right"],
                        help="Type of corner")
    
    args = parser.parse_args()
    
    print("\n===== UNIVERSAL TILE GENERATOR =====")
    
    # Validate arguments
    if args.corner_type and not args.transition_to:
        parser.error("For corner tiles, you must specify --transition-to")
    
    if args.transition_direction and not args.transition_to:
        parser.error("For transition tiles, you must specify --transition-to")
    
    try:
        tile_path = generate_tile(
            tile_type=args.tile_type,
            size=args.size,
            output_dir=args.output_dir,
            seed=args.seed,
            transition_to=args.transition_to,
            transition_direction=args.transition_direction,
            corner_type=args.corner_type
        )
        
        if tile_path:
            if args.transition_to and args.transition_direction:
                print(f"\nTransition tile generated successfully: {tile_path}")
                print(f"\nYou can use this tile to create a seamless transition from {args.tile_type} to {args.transition_to}.")
            elif args.corner_type:
                print(f"\nCorner tile generated successfully: {tile_path}")
                print(f"\nYou can use this tile to create a seamless square L-shaped corner where {args.tile_type} meets {args.transition_to}.")
            else:
                print(f"\n{args.tile_type.capitalize()} tile generated successfully: {tile_path}")
                print(f"\nYou can use this tile in your game by repeating it to create a seamless {args.tile_type} background.")
        else:
            print(f"\nFailed to generate tile.")
    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main() 