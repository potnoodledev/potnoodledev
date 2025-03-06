#!/usr/bin/env node

/**
 * Manual Character Generation Script
 * 
 * This script allows you to manually generate a character with animation
 * without checking for commits.
 * 
 * Usage: node generate-character.js "character description"
 * Example: node generate-character.js "wizard with blue robe and glowing staff facing right"
 */

const { generateImprovedCharacterDescription, generateCharacter } = require('./src/scripts/character-evolution');
const fs = require('fs');
const path = require('path');

// Get the character description from command line arguments
const args = process.argv.slice(2);
let characterDescription = args.join(' ');

// If no description is provided, use a default one
if (!characterDescription) {
  characterDescription = "mystical wanderer with glowing staff and flowing robes facing right";
  console.log(`No description provided. Using default: "${characterDescription}"`);
}

// Ensure the description includes "facing right"
if (!characterDescription.toLowerCase().includes('facing right')) {
  characterDescription += ' facing right';
  console.log(`Added "facing right" to description: "${characterDescription}"`);
}

// Generate the character
console.log(`Generating character: "${characterDescription}"`);
generateCharacter(characterDescription)
  .then(() => {
    console.log('Character generation completed successfully!');
    
    // Update the commit history file with the new description
    const historyFilePath = path.join(__dirname, 'commit-history.json');
    const assetsHistoryPath = path.join(__dirname, 'src', 'assets', 'commit-history.json');
    
    if (fs.existsSync(historyFilePath)) {
      try {
        const historyData = JSON.parse(fs.readFileSync(historyFilePath, 'utf8'));
        historyData.currentCharacterDescription = characterDescription;
        fs.writeFileSync(historyFilePath, JSON.stringify(historyData, null, 2));
        console.log(`Updated commit history with new character description.`);
        
        // Copy to assets directory
        const assetsDir = path.dirname(assetsHistoryPath);
        if (!fs.existsSync(assetsDir)) {
          fs.mkdirSync(assetsDir, { recursive: true });
        }
        fs.copyFileSync(historyFilePath, assetsHistoryPath);
        console.log(`Copied commit history to assets directory.`);
      } catch (error) {
        console.error(`Error updating commit history: ${error.message}`);
      }
    }
  })
  .catch(error => {
    console.error(`Error generating character: ${error.message}`);
  }); 