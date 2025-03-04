#!/usr/bin/env python3
"""
Script to generate various game assets using the game_asset_generator module.
This script creates:
1. A character
2. A character animation
3. An enemy
4. An enemy animation
5. An item
6. A weapon

The script prompts the user for descriptions of each asset.
"""

from game_asset_generator import (
    generate_character_set,
    generate_character_animation,
    generate_enemy_set,
    generate_enemy_animation,
    generate_item,
    generate_weapon_set
)
import os
import random
import time
import requests

def get_user_input(prompt):
    """Get input from the user with the given prompt."""
    return input(f"\n{prompt}: ")

def get_valid_choice(prompt, valid_options):
    """Get a valid choice from the user."""
    while True:
        choice = get_user_input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid choice. Please choose from: {', '.join(valid_options)}")

def generate_with_retry(generate_func, max_retries=3, **kwargs):
    """
    Attempt to generate an asset with retries on failure.
    
    Args:
        generate_func: The generation function to call
        max_retries: Maximum number of retry attempts
        **kwargs: Arguments to pass to the generation function
        
    Returns:
        The result of the generation function or None if all attempts fail
    """
    for attempt in range(max_retries):
        try:
            return generate_func(**kwargs)
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4 seconds
                print(f"\nAPI error: {e}")
                print(f"Retrying in {wait_time} seconds (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"\nFailed after {max_retries} attempts: {e}")
                return None
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            return None

def main():
    """Generate all the requested game assets based on user input."""
    print("\n===== GAME ASSET GENERATOR =====")
    print("This script will help you create a set of game assets.")
    print("You'll be prompted to describe each asset, and then all assets will be generated at once.")
    print("All assets will be created with transparent backgrounds for game use.")
    
    # Create output directories if they don't exist
    os.makedirs("characters", exist_ok=True)
    os.makedirs("enemies", exist_ok=True)
    os.makedirs("items", exist_ok=True)
    os.makedirs("weapons", exist_ok=True)
    
    # Collect all user inputs first
    print("\n----- COLLECTING ASSET DESCRIPTIONS -----")
    
    # Ask if user wants to use a specific seed for reproducibility
    use_seed = get_user_input("Do you want to use a specific seed for reproducibility? (yes/no)").lower().startswith('y')
    if use_seed:
        try:
            seed = int(get_user_input("Enter a seed number (integer)"))
        except ValueError:
            print("Invalid seed. Using a random seed instead.")
            seed = random.randint(1, 100000)
    else:
        seed = random.randint(1, 100000)
    
    print(f"\nUsing seed: {seed}")
    
    # 1. Character description
    print("\n1. CHARACTER")
    character_desc = get_user_input("Describe your character (e.g., 'wizard with blue robes and a magical staff')")
    
    # 2. Character Animation details
    print("\n2. CHARACTER ANIMATION")
    char_action = get_user_input("What action should the character perform? (e.g., walk, run, attack, cast, idle)")
    char_direction = get_user_input("In which direction? (e.g., north, east, south, west)").lower()
    
    # Ask for animation output format
    format_options = ["spritesheet", "gif", "frames"]
    char_output_format = get_valid_choice(f"Choose animation output format ({'/'.join(format_options)})", format_options)
    
    # 3. Enemy description
    print("\n3. ENEMY")
    enemy_desc = get_user_input("Describe your enemy (e.g., 'goblin with a small dagger, green skin')")
    
    # 4. Enemy Animation details
    print("\n4. ENEMY ANIMATION")
    enemy_action = get_user_input("What action should the enemy perform? (e.g., idle, attack, walk)")
    enemy_direction = get_user_input("In which direction? (e.g., north, east, south, west)").lower()
    
    # Ask for animation output format
    enemy_output_format = get_valid_choice(f"Choose animation output format ({'/'.join(format_options)})", format_options)
    
    # 5. Item description
    print("\n5. ITEM")
    item_desc = get_user_input("Describe your item (e.g., 'ancient magic scroll with glowing runes')")
    
    # 6. Weapon description
    print("\n6. WEAPON")
    weapon_desc = get_user_input("Describe your weapon (e.g., 'enchanted sword with blue glowing runes on the blade')")
    
    # Now generate all assets
    print("\n----- GENERATING ASSETS -----")
    
    # Track successful generations
    successful_generations = []
    
    # 1. Generate character
    print("\n1. Generating character...")
    character_path = generate_with_retry(
        generate_character_set,
        character_description=f"{character_desc}, pixel art style, isolated character with no background or floor, floating, for game asset",
        output_dir="characters",
        seed=seed
    )
    
    if character_path:
        print(f"Character generated: {character_path}")
        successful_generations.append(f"1. Character: {character_path}")
    else:
        print("Failed to generate character.")
    
    # 2. Generate character animation (only if character was generated)
    if character_path:
        print("\n2. Generating character animation...")
        char_animation_path = generate_with_retry(
            generate_character_animation,
            character_description=f"{character_desc}, isolated with no background or floor",
            action=char_action,
            direction=char_direction,
            n_frames=4,  # 4 frames for the animation
            reference_image_path=character_path,  # Use the previously generated character as reference
            output_format=char_output_format,  # Use the user-selected format
            output_dir="characters",
            seed=seed
        )
        
        if char_animation_path:
            print(f"Character animation generated: {char_animation_path}")
            successful_generations.append(f"2. Character Animation: {char_animation_path}")
        else:
            print("Failed to generate character animation.")
    else:
        print("\n2. Skipping character animation (character generation failed).")
    
    # 3. Generate enemy
    print("\n3. Generating enemy...")
    enemy_path = generate_with_retry(
        generate_enemy_set,
        enemy_type=f"{enemy_desc}, pixel art style, isolated character with no background or floor, floating, for game asset",
        output_dir="enemies",
        count=1,  # Just one enemy
        seed=seed + 1  # Using a slightly different seed for variety
    )
    
    if enemy_path:
        # If enemy_path is a list (which it often is), get the first item
        if isinstance(enemy_path, list) and len(enemy_path) > 0:
            enemy_reference_path = enemy_path[0]
        else:
            enemy_reference_path = enemy_path
            
        print(f"Enemy generated: {enemy_path}")
        successful_generations.append(f"3. Enemy: {enemy_path}")
        
        # 4. Generate enemy animation
        print("\n4. Generating enemy animation...")
        enemy_animation_path = generate_with_retry(
            generate_enemy_animation,
            enemy_type=f"{enemy_desc}, isolated with no background or floor",
            action=enemy_action,
            direction=enemy_direction,
            n_frames=4,  # 4 frames for the animation
            reference_image_path=enemy_reference_path,  # Use the previously generated enemy as reference
            output_format=enemy_output_format,  # Use the user-selected format
            output_dir="enemies",
            seed=seed + 1
        )
        
        if enemy_animation_path:
            print(f"Enemy animation generated: {enemy_animation_path}")
            successful_generations.append(f"4. Enemy Animation: {enemy_animation_path}")
        else:
            print("Failed to generate enemy animation.")
    else:
        print("Failed to generate enemy.")
        print("\n4. Skipping enemy animation (enemy generation failed).")
    
    # 5. Generate item
    print("\n5. Generating item...")
    item_path = generate_with_retry(
        generate_item,
        item_description=f"{item_desc}, pixel art style, isolated item with no background, floating, for game asset",
        output_dir="items",
        seed=seed + 2  # Using a slightly different seed for variety
    )
    
    if item_path:
        print(f"Item generated: {item_path}")
        successful_generations.append(f"5. Item: {item_path}")
    else:
        print("Failed to generate item.")
    
    # 6. Generate weapon
    print("\n6. Generating weapon...")
    weapon_path = generate_with_retry(
        generate_weapon_set,
        weapon_type=f"{weapon_desc}, pixel art style, isolated weapon with no background, floating, for game asset",
        output_dir="weapons",
        seed=seed + 3  # Using a slightly different seed for variety
    )
    
    if weapon_path:
        print(f"Weapon generated: {weapon_path}")
        successful_generations.append(f"6. Weapon: {weapon_path}")
    else:
        print("Failed to generate weapon.")
    
    # Summary
    if successful_generations:
        print("\n===== GENERATION SUMMARY =====")
        print(f"Successfully generated {len(successful_generations)} out of 6 assets:")
        for item in successful_generations:
            print(item)
    else:
        print("\n===== GENERATION FAILED =====")
        print("Failed to generate any assets. Please try again later or with different descriptions.")
    
    print("\nIf any generations failed, it might be due to temporary API issues or issues with the specific descriptions.")
    print("You can try again with different descriptions or wait a while and try again.")

if __name__ == "__main__":
    main() 