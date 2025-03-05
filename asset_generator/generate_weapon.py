#!/usr/bin/env python3
"""
Script to generate weapon assets for the Evolve game.
This script uses the game_asset_generator module to generate weapon sprites.
"""

import os
import argparse
from game_asset_generator import (
    generate_weapon_set
)

def main():
    """Main function to parse command-line arguments and generate weapon assets."""
    parser = argparse.ArgumentParser(description="Generate weapon assets for the Evolve game")
    
    parser.add_argument("--type", "-t", required=True, help="Type of weapon to generate (e.g., sword, bow)")
    parser.add_argument("--name", "-n", required=True, help="Name of the weapon (used for filename)")
    parser.add_argument("--seed", type=int, help="Seed for the generation process")
    parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    args = parser.parse_args()
    
    # Get API token from parameter or environment variable
    api_token = args.token if args.token else os.getenv("PIXELLAB_API_TOKEN")
    if not api_token:
        raise ValueError("API token not found. Please provide an API token or set the PIXELLAB_API_TOKEN environment variable.")
    
    # Get the absolute path to the project root directory
    # This script is in asset_generator/, so we need to go up one level
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    weapons_dir = os.path.join(project_root, "src", "assets", "images", "weapons")
    
    print(f"Project root: {project_root}")
    print(f"Weapons directory: {weapons_dir}")
    print(f"Generating weapon: {args.type}")
    
    # Generate the weapon
    weapon_path = generate_weapon_set(
        weapon_type=args.type,
        output_dir=weapons_dir,
        output_filename=f"{args.name}.png",
        seed=args.seed,
        api_token=api_token
    )
    
    print(f"Weapon generated: {weapon_path}")
    print(f"Weapon generation complete!")

if __name__ == "__main__":
    main() 