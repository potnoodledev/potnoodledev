#!/usr/bin/env node

/**
 * Test Evolution Script
 * 
 * This script simulates receiving a new commit by manipulating the commit history
 * and forcing a character evolution.
 */

const fs = require('fs');
const path = require('path');
const { checkForEvolution, generateImprovedCharacterDescription, generateCharacter } = require('./src/scripts/character-evolution');

// Configuration
const COMMIT_HISTORY_FILE = path.join(__dirname, 'commit-history.json');

async function simulateNewCommit() {
  try {
    // Read current history
    const historyData = JSON.parse(fs.readFileSync(COMMIT_HISTORY_FILE, 'utf8'));
    
    // Simulate one new commit by incrementing total commits
    historyData.totalCommits += 1;
    
    // Generate new character description
    const evolutionResult = await generateImprovedCharacterDescription(
      historyData.currentCharacterDescription,
      historyData.evolutionLevel
    );
    
    // Update character description and level
    historyData.currentCharacterDescription = evolutionResult.description;
    historyData.evolutionLevel += 1;
    
    // Add to evolution history
    historyData.evolutionHistory.push({
      level: historyData.evolutionLevel,
      commitSha: 'test-commit-' + Date.now(),
      commitMessage: 'Test evolution',
      commitDate: new Date().toISOString(),
      previousDescription: historyData.currentCharacterDescription,
      prompt: evolutionResult.prompt,
      newDescription: evolutionResult.description
    });
    
    // Write back to file
    fs.writeFileSync(COMMIT_HISTORY_FILE, JSON.stringify(historyData, null, 2));
    
    // Generate the character sprite
    await generateCharacter(evolutionResult.description);
    
    console.log('\nEvolution complete!');
    console.log(`Level ${historyData.evolutionLevel - 1} → ${historyData.evolutionLevel}`);
    console.log(`New description: "${evolutionResult.description}"`);
  } catch (error) {
    console.error('Error in test evolution:', error);
  }
}

// Run the simulation
console.log('Starting single evolution test...');
simulateNewCommit()
  .then(() => console.log('\nTest complete!'))
  .catch(error => console.error('Test failed:', error)); 