#!/usr/bin/env python3
"""
Script to generate weapon assets with projectiles for the Evolve game.
This script uses the game_asset_generator module to generate weapon and projectile sprites.
"""

import os
import argparse
from game_asset_generator import (
    generate_weapon_with_projectile
)

def main():
    """Main function to parse command-line arguments and generate weapon assets with projectiles."""
    parser = argparse.ArgumentParser(description="Generate weapon assets with projectiles for the Evolve game")
    
    parser.add_argument("--weapon", "-w", required=True, help="Type of weapon to generate (e.g., bow, sword, wand)")
    parser.add_argument("--projectile", "-p", help="Type of projectile to generate (if not specified, will be determined automatically)")
    parser.add_argument("--weapon-name", "-wn", help="Filename to use for the weapon (if not specified, will be derived from weapon type)")
    parser.add_argument("--projectile-name", "-pn", help="Filename to use for the projectile (if not specified, will be derived from projectile type)")
    parser.add_argument("--seed", type=int, help="Seed for the generation process")
    parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    args = parser.parse_args()
    
    # Determine project root (assuming this script is in the asset_generator directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    print(f"Project root: {project_root}")
    
    # Determine weapons directory
    weapons_dir = os.path.join(project_root, "src", "assets", "images", "weapons")
    projectiles_dir = os.path.join(weapons_dir, "projectiles")
    print(f"Weapons directory: {weapons_dir}")
    print(f"Projectiles directory: {projectiles_dir}")
    
    # Generate weapon with projectile
    print(f"Generating weapon: {args.weapon}")
    if args.projectile:
        print(f"Generating projectile: {args.projectile}")
    
    weapon_path, projectile_path = generate_weapon_with_projectile(
        weapon_type=args.weapon,
        projectile_type=args.projectile,
        output_dir=weapons_dir,  # Explicitly set the output directory to the absolute path
        weapon_filename=args.weapon_name,
        projectile_filename=args.projectile_name,
        seed=args.seed,
        api_token=args.token
    )
    
    print(f"Weapon generated: {weapon_path}")
    print(f"Projectile generated: {projectile_path}")
    print("Weapon and projectile generation complete!")

if __name__ == "__main__":
    main() 