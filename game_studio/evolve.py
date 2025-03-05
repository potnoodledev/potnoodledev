#!/usr/bin/env python3
"""
Evolve Game Studio - Central command hub for AI agents to modify the Evolve game.

This module provides a unified interface for AI agents to:
1. Generate game assets (characters, enemies, items, weapons, terrain)
2. Modify game code and configuration
3. Run the game and development server
4. Deploy the game

Usage:
    python game_studio/evolve.py <command> [options]
"""

import os
import sys
import argparse
import subprocess
import json
import shutil
from pathlib import Path

# Define the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Define paths to key directories
ASSET_GENERATOR_DIR = PROJECT_ROOT / "asset_generator"
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = SRC_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"

# Ensure the script can import from asset_generator
sys.path.append(str(PROJECT_ROOT))

# Import asset generator modules if available
try:
    from asset_generator import game_asset_generator
    from asset_generator.generate_tiles import generate_terrain_tiles
    ASSET_GENERATOR_AVAILABLE = True
except ImportError:
    ASSET_GENERATOR_AVAILABLE = False
    print("Warning: Asset generator modules not found. Asset generation commands will be executed as subprocesses.")

class EvolveGameStudio:
    """Central command hub for AI agents to modify the Evolve game."""
    
    def __init__(self):
        """Initialize the Evolve Game Studio."""
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(
            description="Evolve Game Studio - Central command hub for AI agents to modify the Evolve game.",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Command to execute")
        
        # Asset generation commands
        self._add_character_parser(subparsers)
        self._add_enemy_parser(subparsers)
        self._add_item_parser(subparsers)
        self._add_weapon_parser(subparsers)
        self._add_terrain_parser(subparsers)
        self._add_tile_list_parser(subparsers)
        
        # Game management commands
        self._add_run_parser(subparsers)
        self._add_build_parser(subparsers)
        self._add_deploy_parser(subparsers)
        
        # Comment fetching commands
        self._add_fetch_comments_parser(subparsers)
        
        return parser
    
    def _add_character_parser(self, subparsers):
        """Add character generation command."""
        parser = subparsers.add_parser("generate-character", help="Generate a player character")
        parser.add_argument("--description", required=True, help="Text description of the character")
        parser.add_argument("--animation", action="store_true", help="Generate walk animation frames")
        parser.add_argument("--width", type=int, default=64, help="Width of the sprite in pixels (default: 64)")
        parser.add_argument("--height", type=int, default=64, help="Height of the sprite in pixels (default: 64)")
        parser.add_argument("--seed", type=int, help="Seed for reproducible generation")
        parser.add_argument("--output-dir", help="Custom output directory")
        parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    def _add_enemy_parser(self, subparsers):
        """Add enemy generation command."""
        parser = subparsers.add_parser("generate-enemy", help="Generate an enemy")
        parser.add_argument("--type", required=True, help="Type of enemy to generate")
        parser.add_argument("--animation", action="store_true", help="Generate walk animation frames")
        parser.add_argument("--variations", type=int, default=1, help="Number of variations to generate (default: 1)")
        parser.add_argument("--width", type=int, default=64, help="Width of the sprite in pixels (default: 64)")
        parser.add_argument("--height", type=int, default=64, help="Height of the sprite in pixels (default: 64)")
        parser.add_argument("--seed", type=int, help="Seed for reproducible generation")
        parser.add_argument("--output-dir", help="Custom output directory")
        parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    def _add_item_parser(self, subparsers):
        """Add item generation command."""
        parser = subparsers.add_parser("generate-item", help="Generate an item")
        parser.add_argument("--description", required=True, help="Text description of the item")
        parser.add_argument("--name", required=True, help="Name of the item (used for filename)")
        parser.add_argument("--variations", type=int, default=1, help="Number of variations to generate (default: 1)")
        parser.add_argument("--width", type=int, default=32, help="Width of the sprite in pixels (default: 32)")
        parser.add_argument("--height", type=int, default=32, help="Height of the sprite in pixels (default: 32)")
        parser.add_argument("--seed", type=int, help="Seed for reproducible generation")
        parser.add_argument("--output-dir", help="Custom output directory")
        parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    def _add_weapon_parser(self, subparsers):
        """Add weapon generation command."""
        parser = subparsers.add_parser("generate-weapon", help="Generate a weapon with projectile")
        parser.add_argument("--weapon", required=True, help="Text description of the weapon")
        parser.add_argument("--weapon-name", required=True, help="Name of the weapon (used for filename)")
        parser.add_argument("--projectile", help="Text description of the projectile")
        parser.add_argument("--weapon-width", type=int, default=48, help="Width of the weapon sprite in pixels (default: 48)")
        parser.add_argument("--weapon-height", type=int, default=48, help="Height of the weapon sprite in pixels (default: 48)")
        parser.add_argument("--projectile-width", type=int, default=24, help="Width of the projectile sprite in pixels (default: 24)")
        parser.add_argument("--projectile-height", type=int, default=24, help="Height of the projectile sprite in pixels (default: 24)")
        parser.add_argument("--seed", type=int, help="Seed for reproducible generation")
        parser.add_argument("--output-dir", help="Custom output directory")
        parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    def _add_terrain_parser(self, subparsers):
        """Add terrain generation command."""
        parser = subparsers.add_parser("generate-terrain", help="Generate terrain tiles")
        parser.add_argument("--terrain", required=True, help="Type of terrain to generate")
        parser.add_argument("--variations", type=int, default=3, help="Number of variations to generate (default: 3)")
        parser.add_argument("--width", type=int, default=64, help="Width of the tile in pixels (default: 64)")
        parser.add_argument("--height", type=int, default=64, help="Height of the tile in pixels (default: 64)")
        parser.add_argument("--seed", type=int, help="Seed for reproducible generation")
        parser.add_argument("--output-dir", default=str(IMAGES_DIR / "tiles"), help="Custom output directory")
        parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
        parser.add_argument("--anthropic-token", help="Anthropic API token (overrides environment variable)")
    
    def _add_tile_list_parser(self, subparsers):
        """Add tile list generation command."""
        parser = subparsers.add_parser("generate-tile-list", help="Generate tile list JavaScript file")
        parser.add_argument("--input-dir", default=str(IMAGES_DIR / "tiles"), help="Directory containing tile images")
        parser.add_argument("--output-file", default=str(ASSETS_DIR / "tileList.js"), help="Output JavaScript file path")
    
    def _add_run_parser(self, subparsers):
        """Add run game command."""
        parser = subparsers.add_parser("run", help="Run the game development server")
        parser.add_argument("--port", type=int, default=8080, help="Port to run the server on (default: 8080)")
        parser.add_argument("--open", action="store_true", help="Open the game in a browser")
    
    def _add_build_parser(self, subparsers):
        """Add build game command."""
        parser = subparsers.add_parser("build", help="Build the game for production")
        parser.add_argument("--mode", default="production", choices=["production", "development"], help="Build mode")
    
    def _add_deploy_parser(self, subparsers):
        """Add deploy game command."""
        parser = subparsers.add_parser("deploy", help="Deploy the game to itch.io")
        parser.add_argument("--skip-build", action="store_true", help="Skip building the game before deployment")
    
    def _add_fetch_comments_parser(self, subparsers):
        """Add fetch comments command."""
        parser = subparsers.add_parser("fetch-comments", help="Fetch comments from itch.io")
        parser.add_argument("--username", default="potnoodledev", help="itch.io username")
        parser.add_argument("--game-name", default="evolve", help="Game name on itch.io")
        parser.add_argument("--limit", type=int, default=10, help="Maximum number of comments to retrieve")
        parser.add_argument("--advanced", action="store_true", help="Use advanced comment fetcher")
        parser.add_argument("--output", help="Path to save comments (for advanced fetcher)")
        parser.add_argument("--notify-only-new", action="store_true", help="Only display new comments (for advanced fetcher)")
        parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format (for advanced fetcher)")
    
    def run(self, args=None):
        """Run the Evolve Game Studio with the given arguments."""
        args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return
        
        # Call the appropriate method based on the command
        method_name = args.command.replace("-", "_")
        method = getattr(self, method_name, None)
        
        if method:
            return method(args)
        else:
            print(f"Error: Unknown command '{args.command}'")
            return 1
    
    def generate_character(self, args):
        """Generate a player character."""
        print(f"Generating character: {args.description}")
        
        if ASSET_GENERATOR_AVAILABLE:
            # Use direct module import
            game_asset_generator.generate_character_set(
                description=args.description,
                animation=args.animation,
                width=args.width,
                height=args.height,
                seed=args.seed,
                output_dir=args.output_dir,
                api_token=args.token
            )
        else:
            # Use subprocess
            cmd = [
                "python", str(ASSET_GENERATOR_DIR / "generate_character.py"),
                "--description", args.description
            ]
            
            if args.animation:
                cmd.append("--animation")
            if args.width:
                cmd.extend(["--width", str(args.width)])
            if args.height:
                cmd.extend(["--height", str(args.height)])
            if args.seed:
                cmd.extend(["--seed", str(args.seed)])
            if args.output_dir:
                cmd.extend(["--output-dir", args.output_dir])
            if args.token:
                cmd.extend(["--token", args.token])
            
            subprocess.run(cmd, check=True)
        
        print("Character generation complete.")
        return 0
    
    def generate_enemy(self, args):
        """Generate an enemy."""
        print(f"Generating enemy: {args.type}")
        
        if ASSET_GENERATOR_AVAILABLE:
            # Use direct module import
            game_asset_generator.generate_enemy_set(
                enemy_type=args.type,
                animation=args.animation,
                variations=args.variations,
                width=args.width,
                height=args.height,
                seed=args.seed,
                output_dir=args.output_dir,
                api_token=args.token
            )
        else:
            # Use subprocess
            cmd = [
                "python", str(ASSET_GENERATOR_DIR / "generate_enemy.py"),
                "--type", args.type
            ]
            
            if args.animation:
                cmd.append("--animation")
            if args.variations:
                cmd.extend(["--variations", str(args.variations)])
            if args.width:
                cmd.extend(["--width", str(args.width)])
            if args.height:
                cmd.extend(["--height", str(args.height)])
            if args.seed:
                cmd.extend(["--seed", str(args.seed)])
            if args.output_dir:
                cmd.extend(["--output-dir", args.output_dir])
            if args.token:
                cmd.extend(["--token", args.token])
            
            subprocess.run(cmd, check=True)
        
        print("Enemy generation complete.")
        return 0
    
    def generate_item(self, args):
        """Generate an item."""
        print(f"Generating item: {args.description} (name: {args.name})")
        
        if ASSET_GENERATOR_AVAILABLE:
            # Use direct module import
            game_asset_generator.generate_item(
                description=args.description,
                name=args.name,
                variations=args.variations,
                width=args.width,
                height=args.height,
                seed=args.seed,
                output_dir=args.output_dir,
                api_token=args.token
            )
        else:
            # Use subprocess
            cmd = [
                "python", str(ASSET_GENERATOR_DIR / "generate_item.py"),
                "--description", args.description,
                "--name", args.name
            ]
            
            if args.variations:
                cmd.extend(["--variations", str(args.variations)])
            if args.width:
                cmd.extend(["--width", str(args.width)])
            if args.height:
                cmd.extend(["--height", str(args.height)])
            if args.seed:
                cmd.extend(["--seed", str(args.seed)])
            if args.output_dir:
                cmd.extend(["--output-dir", args.output_dir])
            if args.token:
                cmd.extend(["--token", args.token])
            
            subprocess.run(cmd, check=True)
        
        print("Item generation complete.")
        return 0
    
    def generate_weapon(self, args):
        """Generate a weapon with projectile."""
        print(f"Generating weapon: {args.weapon} (name: {args.weapon_name})")
        
        if ASSET_GENERATOR_AVAILABLE:
            # Use direct module import
            game_asset_generator.generate_weapon_with_projectile(
                weapon_description=args.weapon,
                projectile_description=args.projectile,
                weapon_name=args.weapon_name,
                weapon_width=args.weapon_width,
                weapon_height=args.weapon_height,
                projectile_width=args.projectile_width,
                projectile_height=args.projectile_height,
                seed=args.seed,
                output_dir=args.output_dir,
                api_token=args.token
            )
        else:
            # Use subprocess
            cmd = [
                "python", str(ASSET_GENERATOR_DIR / "generate_weapon_with_projectile.py"),
                "--weapon", args.weapon,
                "--weapon-name", args.weapon_name
            ]
            
            if args.projectile:
                cmd.extend(["--projectile", args.projectile])
            if args.weapon_width:
                cmd.extend(["--weapon-width", str(args.weapon_width)])
            if args.weapon_height:
                cmd.extend(["--weapon-height", str(args.weapon_height)])
            if args.projectile_width:
                cmd.extend(["--projectile-width", str(args.projectile_width)])
            if args.projectile_height:
                cmd.extend(["--projectile-height", str(args.projectile_height)])
            if args.seed:
                cmd.extend(["--seed", str(args.seed)])
            if args.output_dir:
                cmd.extend(["--output-dir", args.output_dir])
            if args.token:
                cmd.extend(["--token", args.token])
            
            subprocess.run(cmd, check=True)
        
        print("Weapon generation complete.")
        return 0
    
    def generate_terrain(self, args):
        """Generate terrain tiles."""
        print(f"Generating terrain: {args.terrain}")
        
        if ASSET_GENERATOR_AVAILABLE:
            # Use direct module import
            generate_terrain_tiles(
                terrain_type=args.terrain,
                variations=args.variations,
                width=args.width,
                height=args.height,
                seed=args.seed,
                output_dir=args.output_dir,
                pixellab_token=args.token,
                anthropic_token=args.anthropic_token
            )
        else:
            # Use subprocess
            cmd = [
                "python", str(ASSET_GENERATOR_DIR / "generate_tiles.py"),
                "--terrain", args.terrain
            ]
            
            if args.variations:
                cmd.extend(["--variations", str(args.variations)])
            if args.width:
                cmd.extend(["--width", str(args.width)])
            if args.height:
                cmd.extend(["--height", str(args.height)])
            if args.seed:
                cmd.extend(["--seed", str(args.seed)])
            if args.output_dir:
                cmd.extend(["--output-dir", args.output_dir])
            if args.token:
                cmd.extend(["--token", args.token])
            if args.anthropic_token:
                cmd.extend(["--anthropic-token", args.anthropic_token])
            
            subprocess.run(cmd, check=True)
        
        print("Terrain generation complete.")
        return 0
    
    def generate_tile_list(self, args):
        """Generate tile list JavaScript file."""
        print("Generating tile list JavaScript file")
        
        cmd = [
            "node", str(ASSET_GENERATOR_DIR / "generate_tile_list.js")
        ]
        
        if args.input_dir:
            cmd.extend(["--input-dir", args.input_dir])
        if args.output_file:
            cmd.extend(["--output-file", args.output_file])
        
        subprocess.run(cmd, check=True)
        
        print("Tile list generation complete.")
        return 0
    
    def run(self, args):
        """Run the game development server."""
        print(f"Running game development server on port {args.port}")
        
        cmd = ["npm", "start"]
        
        if args.port != 8080:
            # Set custom port if different from default
            os.environ["PORT"] = str(args.port)
        
        if args.open:
            cmd.append("--open")
        
        subprocess.run(cmd, cwd=str(PROJECT_ROOT), check=True)
        return 0
    
    def build(self, args):
        """Build the game for production."""
        print(f"Building game in {args.mode} mode")
        
        cmd = ["npm", "run", "build"]
        
        if args.mode == "development":
            cmd.append("--mode=development")
        
        subprocess.run(cmd, cwd=str(PROJECT_ROOT), check=True)
        print("Build complete. Files are in the dist directory.")
        return 0
    
    def deploy(self, args):
        """Deploy the game to itch.io."""
        print("Deploying game to itch.io")
        
        if not args.skip_build:
            print("Building game before deployment...")
            self.build(argparse.Namespace(mode="production"))
        
        cmd = ["npm", "run", "deploy"]
        subprocess.run(cmd, cwd=str(PROJECT_ROOT), check=True)
        
        print("Deployment complete.")
        return 0
    
    def fetch_comments(self, args):
        """Fetch comments from itch.io."""
        print(f"Fetching comments for {args.username}/{args.game_name}")
        
        if args.advanced:
            cmd = ["npm", "run", "fetch-comments-advanced", "--"]
            cmd.extend([args.username, args.game_name])
            
            if args.limit:
                cmd.extend([f"--limit={args.limit}"])
            if args.output:
                cmd.extend([f"--output={args.output}"])
            if args.notify_only_new:
                cmd.append("--notify-only-new")
            if args.format:
                cmd.extend([f"--format={args.format}"])
        else:
            cmd = ["npm", "run", "fetch-comments", "--"]
            cmd.extend([args.username, args.game_name, str(args.limit)])
        
        subprocess.run(cmd, cwd=str(PROJECT_ROOT), check=True)
        return 0

def main():
    """Main entry point for the Evolve Game Studio."""
    studio = EvolveGameStudio()
    return studio.run()

if __name__ == "__main__":
    sys.exit(main()) 