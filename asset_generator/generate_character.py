#!/usr/bin/env python3
"""
Script to generate character assets for the Evolve game.
This script uses the game_asset_generator module to generate character sprites and animations.
"""

import os
import argparse
from game_asset_generator import (
    generate_character_set,
    generate_character_animation
)

def main():
    """Main function to parse command-line arguments and generate character assets."""
    parser = argparse.ArgumentParser(description="Generate character assets for the Evolve game")
    
    parser.add_argument("--description", "-d", required=True, help="Description of the character")
    parser.add_argument("--seed", type=int, help="Seed for the generation process")
    parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    parser.add_argument("--animation", "-a", action="store_true", help="Generate walk animation frames")
    
    args = parser.parse_args()
    
    # Get API token from parameter or environment variable
    api_token = args.token if args.token else os.getenv("PIXELLAB_API_TOKEN")
    if not api_token:
        raise ValueError("API token not found. Please provide an API token or set the PIXELLAB_API_TOKEN environment variable.")
    
    # Get the absolute path to the project root directory
    # This script is in asset_generator/, so we need to go up one level
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    assets_dir = os.path.join(project_root, "src", "assets", "images")
    
    print(f"Project root: {project_root}")
    print(f"Assets directory: {assets_dir}")
    print(f"Generating character: {args.description}")
    
    # Generate the main character sprite
    character_path = generate_character_set(
        character_description=args.description,
        output_dir=assets_dir,  # Use the absolute path
        seed=args.seed,
        api_token=api_token
    )
    
    print(f"Main sprite generated: {character_path}")
    
    # Generate the walk animation if requested
    if args.animation:
        print("Generating walk animation frames...")
        player_dir = os.path.join(assets_dir, "player")
        animation_path = generate_character_animation(
            character_description=args.description,
            action="walk",
            reference_image_path=character_path,
            output_dir=player_dir,  # Use the absolute path
            output_format="frames",
            seed=args.seed,
            api_token=api_token
        )
        
        print(f"Walk animation generated: {animation_path}")
    
    print(f"Character generation complete!")

if __name__ == "__main__":
    main() 