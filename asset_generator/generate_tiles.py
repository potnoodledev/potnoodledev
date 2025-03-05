#!/usr/bin/env python3
"""
Script to generate seamless terrain tiles for the Evolve game.
This script uses simple procedural patterns to generate seamless terrain tiles
with 3 variations per terrain type.
"""

import os
import argparse
import random
import numpy as np
from PIL import Image, ImageDraw

# Define terrain types and their base colors
TERRAIN_TYPES = {
    "grass": {
        "base_colors": [(34, 139, 34), (50, 205, 50), (60, 179, 113)],  # Dark green, lime green, medium sea green
        "detail_colors": [(255, 255, 0), (255, 192, 203), (255, 255, 255)],  # Yellow, pink, white for flowers
        "detail_chance": 0.05  # 5% chance of a detail (flower) per pixel
    },
    "desert": {
        "base_colors": [(210, 180, 140), (244, 164, 96), (222, 184, 135)],  # Tan, sandy brown, burlywood
        "detail_colors": [(139, 69, 19), (160, 82, 45)],  # Brown, sienna for rocks
        "detail_chance": 0.03  # 3% chance of a detail (rock) per pixel
    },
    "snow": {
        "base_colors": [(220, 220, 255), (240, 248, 255), (248, 248, 255)],  # Light blue-white, alice blue, ghost white
        "detail_colors": [(200, 200, 255), (180, 180, 255)],  # Slightly darker blue-white for shadows
        "detail_chance": 0.04  # 4% chance of a detail (shadow) per pixel
    },
    "water": {
        "base_colors": [(0, 105, 148), (65, 105, 225), (30, 144, 255)],  # Deep blue, royal blue, dodger blue
        "detail_colors": [(240, 248, 255), (173, 216, 230)],  # Alice blue, light blue for foam
        "detail_chance": 0.03  # 3% chance of a detail (foam) per pixel
    },
    "lava": {
        "base_colors": [(255, 69, 0), (255, 140, 0), (255, 165, 0)],  # Red-orange, dark orange, orange
        "detail_colors": [(255, 215, 0), (255, 255, 0)],  # Gold, yellow for embers
        "detail_chance": 0.06  # 6% chance of a detail (ember) per pixel
    },
    "stone": {
        "base_colors": [(112, 128, 144), (119, 136, 153), (105, 105, 105)],  # Slate gray, light slate gray, dim gray
        "detail_colors": [(169, 169, 169), (192, 192, 192)],  # Dark gray, silver for highlights
        "detail_chance": 0.04  # 4% chance of a detail (highlight) per pixel
    },
    "dirt": {
        "base_colors": [(139, 69, 19), (160, 82, 45), (165, 42, 42)],  # Saddle brown, sienna, brown
        "detail_colors": [(101, 67, 33), (85, 45, 10)],  # Darker browns for variation
        "detail_chance": 0.05  # 5% chance of a detail per pixel
    }
}

def generate_simple_flower(draw, x, y, color):
    """Draw a simple flower at the given position."""
    # Draw center
    draw.point((x, y), fill=color)
    
    # Draw petals
    if random.random() < 0.7:  # 70% chance to draw petals
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            if 0 <= x + dx < 32 and 0 <= y + dy < 32:  # Ensure we're within bounds
                draw.point((x + dx, y + dy), fill=color)

def generate_terrain_tile(terrain_type, variation, size=32, seed=None):
    """
    Generate a single terrain tile using simple procedural patterns.
    
    Args:
        terrain_type (str): Type of terrain to generate.
        variation (int): Variation number (1-3).
        size (int): Size of the tile in pixels.
        seed (int): Random seed for reproducibility.
        
    Returns:
        PIL.Image.Image: The generated tile image.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        
    # Get terrain configuration
    if terrain_type not in TERRAIN_TYPES:
        print(f"Warning: Unknown terrain type '{terrain_type}'. Using grass as default.")
        terrain_type = "grass"
        
    terrain_config = TERRAIN_TYPES[terrain_type]
    
    # Create a new image
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # Generate a simple noise pattern
    noise = np.random.rand(size, size)
    
    # Fill the image with terrain
    for y in range(size):
        for x in range(size):
            # Determine base color based on noise
            noise_val = noise[y, x]
            
            # Choose base color
            if noise_val < 0.33:
                base_color = terrain_config["base_colors"][0]
            elif noise_val < 0.66:
                base_color = terrain_config["base_colors"][1]
            else:
                base_color = terrain_config["base_colors"][2]
                
            # Apply the base color
            draw.point((x, y), fill=base_color)
    
    # Add details (like flowers) with a small probability
    for y in range(size):
        for x in range(size):
            if random.random() < terrain_config["detail_chance"]:
                detail_color = random.choice(terrain_config["detail_colors"])
                
                if terrain_type == "grass":
                    # For grass, draw flowers
                    generate_simple_flower(draw, x, y, detail_color)
                else:
                    # For other terrains, just add detail pixels
                    draw.point((x, y), fill=detail_color)
    
    return image

def generate_terrain_tiles(terrain_type, output_dir="src/assets/images/tiles", seed=None, api_token=None):
    """
    Generate a set of seamless terrain tiles for a specific terrain type.
    
    Args:
        terrain_type (str): Type of terrain to generate (e.g., "grass", "desert", "snow").
        output_dir (str, optional): Directory to save the tiles to. Defaults to "src/assets/images/tiles".
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): Not used in this version, kept for compatibility.
        
    Returns:
        list: List of file paths to the generated tiles.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    terrain_dir = os.path.join(output_dir, terrain_type)
    os.makedirs(terrain_dir, exist_ok=True)
    
    # Generate 3 variations of the terrain
    tile_paths = []
    for i in range(3):
        # Use a different seed for each variation but related to the main seed
        variation_seed = seed + i * 1000
        
        # Generate the tile
        output_filename = f"{terrain_type}_{i+1}.png"
        output_path = os.path.join(terrain_dir, output_filename)
        
        print(f"Generating {terrain_type} tile variation {i+1}...")
        
        # Generate the tile using procedural patterns
        tile_image = generate_terrain_tile(
            terrain_type=terrain_type,
            variation=i+1,
            size=32,
            seed=variation_seed
        )
        
        # Save the tile
        tile_image.save(output_path)
        
        print(f"Generated tile: {output_path}")
        tile_paths.append(output_path)
    
    return tile_paths

def main():
    """Main function to parse command-line arguments and generate terrain tiles."""
    parser = argparse.ArgumentParser(description="Generate seamless terrain tiles for the Evolve game")
    
    parser.add_argument("--terrain", "-t", required=True, help=f"Type of terrain to generate. Options: {', '.join(TERRAIN_TYPES.keys())}")
    parser.add_argument("--seed", type=int, help="Seed for the generation process")
    parser.add_argument("--token", help="PixelLab API token (not used in this version)")
    
    args = parser.parse_args()
    
    # Determine project root (assuming this script is in the asset_generator directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    print(f"Project root: {project_root}")
    
    # Determine tiles directory
    tiles_dir = os.path.join(project_root, "src", "assets", "images", "tiles")
    print(f"Tiles directory: {tiles_dir}")
    
    # Generate terrain tiles
    print(f"Generating {args.terrain} terrain tiles...")
    
    tile_paths = generate_terrain_tiles(
        terrain_type=args.terrain,
        output_dir=tiles_dir,
        seed=args.seed,
        api_token=args.token
    )
    
    print(f"Generated {len(tile_paths)} terrain tiles:")
    for path in tile_paths:
        print(f"  - {path}")
    print("Terrain tile generation complete!")

if __name__ == "__main__":
    main() 