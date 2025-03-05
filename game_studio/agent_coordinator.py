#!/usr/bin/env python3
"""
Agent Coordinator for Evolve Game Studio

This script coordinates between the Game Developer Agent and Artist Agent
to implement game changes based on user requests.

Usage:
    python game_studio/agent_coordinator.py "user request"
"""

import os
import sys
import argparse
import subprocess
import json
import time
import threading
from pathlib import Path
import anthropic
import re
import logging
from tqdm import tqdm

# Define the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AgentCoordinator")

class ProgressBar:
    """A simple progress bar for long-running operations."""
    
    def __init__(self, desc="Processing", total=100):
        """Initialize the progress bar."""
        self.pbar = tqdm(total=total, desc=desc, ncols=100)
        self.stop_event = threading.Event()
        self.thread = None
        self.current = 0
        self.total = total
    
    def start(self):
        """Start the progress bar."""
        self.thread = threading.Thread(target=self._update_progress)
        self.thread.daemon = True
        self.thread.start()
    
    def _update_progress(self):
        """Update the progress bar until stopped."""
        while not self.stop_event.is_set():
            if self.current < self.total:
                self.current += 1
                self.pbar.update(1)
                if self.current >= self.total:
                    self.current = 0
            time.sleep(0.1)
    
    def stop(self):
        """Stop the progress bar."""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1)
        self.pbar.close()


class GameDeveloperAgent:
    """Agent that makes changes to existing game code."""
    
    def __init__(self, api_key=None):
        """Initialize the Game Developer Agent with Claude API access."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable or api_key parameter is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-sonnet-20240229"
        self.logger = logging.getLogger("GameDeveloperAgent")
    
    def analyze_request(self, user_request, game_files=None):
        """
        Analyze the user request to determine what code changes are needed.
        
        Args:
            user_request: The user's request for a game change
            game_files: Optional list of relevant game files to consider
            
        Returns:
            A dictionary with the analysis results including:
            - files_to_modify: List of files that need to be modified
            - code_changes: Description of changes needed for each file
        """
        self.logger.info(f"Starting analysis of request: '{user_request}'")
        
        # If no game files provided, use a default set of important files
        if not game_files:
            game_files = self._get_default_game_files()
            self.logger.info(f"Using default game files: {', '.join(game_files)}")
        
        # Read the content of each file
        file_contents = {}
        for file_path in game_files:
            full_path = PROJECT_ROOT / file_path
            if full_path.exists():
                self.logger.info(f"Reading file: {file_path}")
                file_contents[file_path] = full_path.read_text()
            else:
                self.logger.warning(f"File not found: {file_path}")
        
        # Prepare the prompt for Claude
        prompt = f"""
You are a game developer agent for a Phaser 3 game. Your task is to analyze a user request and determine what code changes are needed.

USER REQUEST: "{user_request}"

Here are the relevant game files:

{self._format_files_for_prompt(file_contents)}

Based on the user request, please:
1. Identify which files need to be modified
2. For each file, describe the specific code changes needed
3. Provide the exact code modifications in a format that can be applied

First, think through your analysis step by step:
- What is the user asking for?
- Which game mechanics would need to be modified?
- Which files contain the relevant code?
- What specific changes are needed in each file?

After your analysis, provide your response in JSON format with the following structure:
{{
    "reasoning": "Detailed explanation of your thought process and analysis",
    "files_to_modify": [
        {{
            "file_path": "path/to/file.js",
            "reason": "Why this file needs to be modified",
            "changes": [
                {{
                    "description": "Description of the change",
                    "original_code": "Code to be replaced",
                    "new_code": "New code to insert"
                }}
            ]
        }}
    ],
    "explanation": "Explanation of how these changes fulfill the user request"
}}
"""
        
        self.logger.info("Sending request to Claude API for code analysis")
        progress = ProgressBar(desc="Analyzing code", total=100)
        progress.start()
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0,
                system="You are a game developer agent that analyzes user requests and determines what code changes are needed. Provide detailed reasoning before your JSON response.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and parse the JSON response
            content = response.content[0].text
            self.logger.debug(f"Received response from Claude API: {content[:200]}...")
            
            # Extract JSON from the response (in case there's markdown or other text)
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                self.logger.debug("Extracted JSON from code block")
            else:
                json_str = content
                self.logger.debug("Using full response as JSON")
                
            try:
                analysis = json.loads(json_str)
                self.logger.info("Successfully parsed analysis JSON")
                
                # Log the reasoning
                if "reasoning" in analysis:
                    self.logger.info("Developer Agent Reasoning:")
                    for line in analysis["reasoning"].split('\n'):
                        if line.strip():
                            self.logger.info(f"  {line.strip()}")
                
                # Log files to modify
                if "files_to_modify" in analysis:
                    self.logger.info(f"Files to modify: {len(analysis['files_to_modify'])}")
                    for file_info in analysis["files_to_modify"]:
                        self.logger.info(f"  - {file_info['file_path']}: {file_info.get('reason', 'No reason provided')}")
                
                return analysis
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON: {e}")
                self.logger.debug(f"JSON string: {json_str[:200]}...")
                # If JSON parsing fails, return a simplified response
                return {
                    "reasoning": "Failed to parse the analysis JSON",
                    "files_to_modify": [],
                    "explanation": "Failed to parse the analysis. Please check the API response format."
                }
        finally:
            progress.stop()
    
    def implement_changes(self, analysis):
        """
        Implement the code changes based on the analysis.
        
        Args:
            analysis: The analysis dictionary from analyze_request()
            
        Returns:
            A dictionary with the results of the implementation
        """
        self.logger.info("Starting implementation of code changes")
        
        results = {
            "success": True,
            "modified_files": [],
            "errors": []
        }
        
        for file_info in analysis.get("files_to_modify", []):
            file_path = file_info["file_path"]
            full_path = PROJECT_ROOT / file_path
            
            self.logger.info(f"Processing file: {file_path}")
            
            if not full_path.exists():
                error_msg = f"File not found: {file_path}"
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["success"] = False
                continue
            
            try:
                # Read the current file content
                current_content = full_path.read_text()
                new_content = current_content
                
                # Apply each change
                for i, change in enumerate(file_info.get("changes", [])):
                    original = change.get("original_code", "")
                    new = change.get("new_code", "")
                    description = change.get("description", f"Change #{i+1}")
                    
                    self.logger.info(f"  - Applying change: {description}")
                    
                    if original in new_content:
                        self.logger.debug(f"    Found original code: {original[:50]}...")
                        new_content = new_content.replace(original, new)
                        self.logger.debug(f"    Replaced with: {new[:50]}...")
                    else:
                        error_msg = f"Could not find the original code in {file_path}"
                        self.logger.error(error_msg)
                        self.logger.debug(f"    Original code not found: {original[:50]}...")
                        results["errors"].append(error_msg)
                        results["success"] = False
                
                # Write the modified content back to the file
                full_path.write_text(new_content)
                self.logger.info(f"Successfully modified file: {file_path}")
                results["modified_files"].append(file_path)
                
            except Exception as e:
                error_msg = f"Error modifying {file_path}: {str(e)}"
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["success"] = False
        
        if results["success"]:
            self.logger.info("All code changes implemented successfully")
        else:
            self.logger.warning("Some code changes failed to implement")
            
        return results
    
    def _get_default_game_files(self):
        """Get a default list of important game files to consider."""
        return [
            "src/scenes/GameScene.js",
            "src/objects/Player.js",
            "src/objects/Enemy.js",
            "src/objects/Weapon.js",
            "src/objects/Item.js",
            "src/config/weapons.js",
            "src/config/items.js"
        ]
    
    def _format_files_for_prompt(self, file_contents):
        """Format the file contents for inclusion in the prompt."""
        formatted = ""
        for file_path, content in file_contents.items():
            formatted += f"--- {file_path} ---\n{content}\n\n"
        return formatted


class ArtistAgent:
    """Agent that generates game assets using evolve.py commands."""
    
    def __init__(self, api_key=None):
        """Initialize the Artist Agent with Claude API access."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable or api_key parameter is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-sonnet-20240229"
        self.logger = logging.getLogger("ArtistAgent")
    
    def analyze_request(self, user_request):
        """
        Analyze the user request to determine what assets need to be generated.
        
        Args:
            user_request: The user's request for a game change
            
        Returns:
            A dictionary with the analysis results including:
            - assets_to_generate: List of assets that need to be generated
            - generation_commands: List of evolve.py commands to generate each asset
        """
        self.logger.info(f"Starting analysis of request: '{user_request}'")
        
        # Prepare the prompt for Claude
        prompt = f"""
You are an artist agent for a pixel art game. Your task is to analyze a user request and determine what assets need to be generated.

USER REQUEST: "{user_request}"

You can generate assets using the following commands from evolve.py:

1. generate-character: Generate a character sprite
   - Required: --description (character description)
   - Optional: --animation (boolean), --width (default: 64), --height (default: 64)

2. generate-enemy: Generate an enemy sprite
   - Required: --type (enemy type)
   - Optional: --animation (boolean), --variations (number), --width (default: 64), --height (default: 64)

3. generate-weapon: Generate a weapon sprite
   - Required: --weapon (weapon description), --weapon-name (name for file)
   - Optional: --projectile (projectile description), --weapon-width (default: 48), --weapon-height (default: 48)

4. generate-item: Generate an item sprite
   - Required: --item (item description), --item-name (name for file)
   - Optional: --width (default: 32), --height (default: 32)

5. generate-terrain: Generate terrain tiles
   - Required: --terrain (terrain description)
   - Optional: --variations (number), --width (default: 64), --height (default: 64)

First, think through your analysis step by step:
- What is the user asking for?
- What type of game asset would be needed?
- What specific details should be included in the asset?
- Which command is most appropriate for generating this asset?
- What parameters should be used with the command?

Based on the user request, determine what assets need to be generated and provide the exact commands to generate them.

After your analysis, provide your response in JSON format with the following structure:
{{
    "reasoning": "Detailed explanation of your thought process and analysis",
    "assets_to_generate": [
        {{
            "asset_type": "weapon",
            "description": "A flaming battle axe with ornate handle",
            "reason": "The user wants a flaming axe, which requires a weapon asset",
            "command": "python game_studio/evolve.py generate-weapon --weapon 'flaming battle axe with ornate handle' --weapon-name 'flaming_axe' --projectile 'fire particles'"
        }}
    ],
    "explanation": "Explanation of how these assets fulfill the user request"
}}
"""
        
        self.logger.info("Sending request to Claude API for asset analysis")
        progress = ProgressBar(desc="Analyzing assets", total=100)
        progress.start()
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0,
                system="You are an artist agent that analyzes user requests and determines what assets need to be generated. Provide detailed reasoning before your JSON response.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and parse the JSON response
            content = response.content[0].text
            self.logger.debug(f"Received response from Claude API: {content[:200]}...")
            
            # Extract JSON from the response (in case there's markdown or other text)
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                self.logger.debug("Extracted JSON from code block")
            else:
                json_str = content
                self.logger.debug("Using full response as JSON")
                
            try:
                analysis = json.loads(json_str)
                self.logger.info("Successfully parsed analysis JSON")
                
                # Log the reasoning
                if "reasoning" in analysis:
                    self.logger.info("Artist Agent Reasoning:")
                    for line in analysis["reasoning"].split('\n'):
                        if line.strip():
                            self.logger.info(f"  {line.strip()}")
                
                # Log assets to generate
                if "assets_to_generate" in analysis:
                    self.logger.info(f"Assets to generate: {len(analysis['assets_to_generate'])}")
                    for asset_info in analysis["assets_to_generate"]:
                        self.logger.info(f"  - {asset_info['asset_type']}: {asset_info['description']}")
                        self.logger.info(f"    Reason: {asset_info.get('reason', 'No reason provided')}")
                        self.logger.info(f"    Command: {asset_info['command']}")
                
                return analysis
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON: {e}")
                self.logger.debug(f"JSON string: {json_str[:200]}...")
                # If JSON parsing fails, return a simplified response
                return {
                    "reasoning": "Failed to parse the analysis JSON",
                    "assets_to_generate": [],
                    "explanation": "Failed to parse the analysis. Please check the API response format."
                }
        finally:
            progress.stop()
    
    def generate_assets(self, analysis):
        """
        Generate the assets based on the analysis.
        
        Args:
            analysis: The analysis dictionary from analyze_request()
            
        Returns:
            A dictionary with the results of the asset generation
        """
        self.logger.info("Starting generation of assets")
        
        results = {
            "success": True,
            "generated_assets": [],
            "errors": []
        }
        
        for asset_info in analysis.get("assets_to_generate", []):
            asset_type = asset_info.get("asset_type", "unknown")
            description = asset_info.get("description", "")
            command = asset_info.get("command", "")
            
            self.logger.info(f"Generating {asset_type} asset: {description}")
            self.logger.info(f"Command: {command}")
            
            if not command:
                error_msg = "Missing command for asset generation"
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["success"] = False
                continue
            
            try:
                # Create a progress bar for the command execution
                progress = ProgressBar(desc=f"Generating {asset_type}", total=100)
                progress.start()
                
                try:
                    # Execute the command
                    process = subprocess.run(
                        command,
                        shell=True,
                        cwd=str(PROJECT_ROOT),
                        capture_output=True,
                        text=True
                    )
                    
                    if process.returncode == 0:
                        self.logger.info(f"Successfully generated {asset_type} asset")
                        self.logger.debug(f"Command output: {process.stdout[:200]}...")
                        
                        results["generated_assets"].append({
                            "asset_type": asset_type,
                            "description": description,
                            "command": command,
                            "output": process.stdout
                        })
                    else:
                        error_msg = f"Command failed: {command}\nError: {process.stderr}"
                        self.logger.error(error_msg)
                        results["errors"].append(error_msg)
                        results["success"] = False
                finally:
                    progress.stop()
                    
            except Exception as e:
                error_msg = f"Error executing command: {command}\nError: {str(e)}"
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["success"] = False
        
        if results["success"]:
            self.logger.info("All assets generated successfully")
        else:
            self.logger.warning("Some asset generation failed")
            
        return results


class AgentCoordinator:
    """Coordinates between the Game Developer Agent and Artist Agent."""
    
    def __init__(self, api_key=None, verbose=False):
        """Initialize the Agent Coordinator with the developer and artist agents."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable or api_key parameter is required")
        
        # Set logging level based on verbosity
        if verbose:
            logger.setLevel(logging.DEBUG)
        
        self.developer = GameDeveloperAgent(api_key=self.api_key)
        self.artist = ArtistAgent(api_key=self.api_key)
        self.logger = logging.getLogger("AgentCoordinator")
    
    def process_request(self, user_request):
        """
        Process a user request by coordinating between the developer and artist agents.
        
        Args:
            user_request: The user's request for a game change
            
        Returns:
            A dictionary with the results of the processing
        """
        results = {
            "user_request": user_request,
            "developer_analysis": None,
            "artist_analysis": None,
            "code_changes": None,
            "asset_generation": None,
            "success": False,
            "summary": ""
        }
        
        self.logger.info(f"Processing request: {user_request}")
        self.logger.info("=" * 80)
        self.logger.info("STEP 1: ANALYZING REQUEST")
        self.logger.info("=" * 80)
        
        # Step 1: Analyze the request with both agents
        self.logger.info("Analyzing request with Game Developer Agent...")
        developer_analysis = self.developer.analyze_request(user_request)
        results["developer_analysis"] = developer_analysis
        
        self.logger.info("\nAnalyzing request with Artist Agent...")
        artist_analysis = self.artist.analyze_request(user_request)
        results["artist_analysis"] = artist_analysis
        
        self.logger.info("=" * 80)
        self.logger.info("STEP 2: IMPLEMENTING CHANGES")
        self.logger.info("=" * 80)
        
        # Step 2: Implement code changes
        if developer_analysis.get("files_to_modify"):
            self.logger.info("Implementing code changes...")
            code_changes = self.developer.implement_changes(developer_analysis)
            results["code_changes"] = code_changes
        else:
            self.logger.info("No code changes needed.")
            results["code_changes"] = {"success": True, "modified_files": [], "errors": []}
        
        self.logger.info("=" * 80)
        self.logger.info("STEP 3: GENERATING ASSETS")
        self.logger.info("=" * 80)
        
        # Step 3: Generate assets
        if artist_analysis.get("assets_to_generate"):
            self.logger.info("Generating assets...")
            asset_generation = self.artist.generate_assets(artist_analysis)
            results["asset_generation"] = asset_generation
        else:
            self.logger.info("No assets to generate.")
            results["asset_generation"] = {"success": True, "generated_assets": [], "errors": []}
        
        self.logger.info("=" * 80)
        self.logger.info("STEP 4: FINALIZING RESULTS")
        self.logger.info("=" * 80)
        
        # Step 4: Determine overall success
        code_success = results["code_changes"]["success"]
        asset_success = results["asset_generation"]["success"]
        results["success"] = code_success and asset_success
        
        # Step 5: Generate summary
        summary = []
        
        if results["code_changes"]["modified_files"]:
            summary.append(f"Modified {len(results['code_changes']['modified_files'])} files: {', '.join(results['code_changes']['modified_files'])}")
        
        if results["asset_generation"]["generated_assets"]:
            asset_types = [asset["asset_type"] for asset in results["asset_generation"]["generated_assets"]]
            summary.append(f"Generated {len(asset_types)} assets: {', '.join(asset_types)}")
        
        if results["code_changes"]["errors"]:
            summary.append(f"Code errors: {', '.join(results['code_changes']['errors'])}")
        
        if results["asset_generation"]["errors"]:
            summary.append(f"Asset errors: {', '.join(results['asset_generation']['errors'])}")
        
        if not summary:
            summary.append("No changes were made.")
        
        results["summary"] = " ".join(summary)
        
        self.logger.info(f"Request processing complete: {results['summary']}")
        return results


def main():
    """Main entry point for the Agent Coordinator."""
    parser = argparse.ArgumentParser(
        description="Agent Coordinator for Evolve Game Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("request", help="The user request to process")
    parser.add_argument("--api-key", help="Anthropic API key (defaults to ANTHROPIC_API_KEY environment variable)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    try:
        # Print a fancy header
        print("\n" + "=" * 80)
        print(" " * 30 + "EVOLVE GAME STUDIO")
        print(" " * 25 + "AI AGENT COORDINATOR SYSTEM")
        print("=" * 80 + "\n")
        
        coordinator = AgentCoordinator(api_key=args.api_key, verbose=args.verbose)
        results = coordinator.process_request(args.request)
        
        # Print a summary of the results
        print("\n" + "=" * 80)
        print(" " * 35 + "RESULTS")
        print("=" * 80)
        print(f"Success: {'✅ YES' if results['success'] else '❌ NO'}")
        print(f"Summary: {results['summary']}")
        
        # Save the results to a JSON file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        results_file = PROJECT_ROOT / "game_studio" / f"request_results_{timestamp}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\nDetailed results saved to: {results_file}")
        print("=" * 80 + "\n")
        
        return 0 if results["success"] else 1
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 