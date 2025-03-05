#!/usr/bin/env python3
"""
Script to generate enemy assets for the Evolve game.
This script uses the game_asset_generator module to generate enemy sprites and animations.
"""

import os
import argparse
from game_asset_generator import (
    generate_enemy_set,
    generate_enemy_animation
)

def main():
    """Main function to parse command-line arguments and generate enemy assets."""
    parser = argparse.ArgumentParser(description="Generate enemy assets for the Evolve game")
    
    parser.add_argument("--type", "-t", required=True, help="Type of enemy to generate (e.g., zombie, skeleton)")
    parser.add_argument("--seed", type=int, help="Seed for the generation process")
    parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    parser.add_argument("--animation", "-a", action="store_true", help="Generate walk animation frames")
    parser.add_argument("--variations", "-v", type=int, default=1, help="Number of enemy variations to generate")
    
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
    print(f"Generating enemy: {args.type}")
    
    # Generate the main enemy sprite and variations
    enemy_assets = generate_enemy_set(
        enemy_type=args.type,
        output_dir=assets_dir,  # Use the absolute path
        count=args.variations,
        seed=args.seed,
        api_token=api_token
    )
    
    print(f"Main enemy sprite generated: {enemy_assets[0]}")
    if args.variations > 1:
        print(f"Generated {args.variations} enemy variations")
    
    # Generate the walk animation if requested
    if args.animation:
        print("Generating walk animation frames...")
        enemies_dir = os.path.join(assets_dir, "enemies")
        animation_path = generate_enemy_animation(
            enemy_type=args.type,
            action="walk",
            reference_image_path=enemy_assets[0],
            output_dir=enemies_dir,  # Use the absolute path
            output_format="frames",
            seed=args.seed,
            api_token=api_token
        )
        
        print(f"Walk animation generated: {animation_path}")
    
    print(f"Enemy generation complete!")

if __name__ == "__main__":
    main() 