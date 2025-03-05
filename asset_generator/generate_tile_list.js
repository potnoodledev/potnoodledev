/**
 * Script to generate a JSON file listing all tiles in the tiles directory.
 * This file is used by the game to dynamically load all available tiles.
 */

const fs = require('fs');
const path = require('path');

// Path to the tiles directory
const tilesDir = path.join(__dirname, '..', 'src', 'assets', 'images', 'tiles');

// Path to the output JSON file - place it inside the tiles folder
const outputFile = path.join(tilesDir, 'tileFiles.json');

// Read the tiles directory
try {
  // Get all PNG files in the tiles directory
  const files = fs.readdirSync(tilesDir)
    .filter(file => file.endsWith('.png'));
  
  // Create the JSON object
  const tileFiles = {
    files: files
  };
  
  // Write the JSON file
  fs.writeFileSync(outputFile, JSON.stringify(tileFiles, null, 2));
  
  console.log(`Generated tile list with ${files.length} tiles`);
  console.log(`Saved to: ${outputFile}`);
} catch (error) {
  console.error('Error generating tile list:', error);
} 