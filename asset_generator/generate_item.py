#!/usr/bin/env python3
"""
Script to generate item assets for the Evolve game.
This script uses the game_asset_generator module to generate item sprites.
"""

import os
import argparse
from game_asset_generator import (
    generate_item
)

def main():
    """Main function to parse command-line arguments and generate item assets."""
    parser = argparse.ArgumentParser(description="Generate item assets for the Evolve game")
    
    parser.add_argument("--description", "-d", required=True, help="Description of the item")
    parser.add_argument("--name", "-n", required=True, help="Name of the item (used for filename)")
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
    items_dir = os.path.join(project_root, "src", "assets", "images", "items")
    
    print(f"Project root: {project_root}")
    print(f"Items directory: {items_dir}")
    print(f"Generating item: {args.description}")
    
    # Generate the item
    item_path = generate_item(
        item_description=args.description,
        output_dir=items_dir,
        output_filename=f"{args.name}.png",
        seed=args.seed,
        api_token=api_token
    )
    
    print(f"Item generated: {item_path}")
    print(f"Item generation complete!")

if __name__ == "__main__":
    main() 