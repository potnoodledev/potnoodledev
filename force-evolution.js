#!/usr/bin/env node

/**
 * Force Evolution Script
 * 
 * This script forces the system to process existing commits and generate
 * a series of evolutions, even if they've been processed before.
 * 
 * Run with: node force-evolution.js
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { generateImprovedCharacterDescription, generateCharacter } = require('./src/scripts/character-evolution');

// Configuration
const GITHUB_USERNAME = 'potnoodledev';
const COMMIT_HISTORY_FILE = path.join(__dirname, 'commit-history.json');
const ASSETS_HISTORY_FILE = path.join(__dirname, 'src/assets/commit-history.json');

// Copy commit history to assets directory
function copyCommitHistoryToAssets() {
  try {
    fs.copyFileSync(COMMIT_HISTORY_FILE, ASSETS_HISTORY_FILE);
    console.log('Copied commit history to assets directory');
  } catch (error) {
    console.error('Error copying commit history to assets:', error.message);
  }
}

// Get the latest commits by the specified GitHub user
const getLatestCommitsByUser = async () => {
  try {
    console.log(`Fetching commits for ${GITHUB_USERNAME}...`);
    const response = await axios.get(
      `https://api.github.com/search/commits`,
      {
        params: { q: `author:${GITHUB_USERNAME}` },
        headers: {
          Accept: 'application/vnd.github.cloak-preview',
        },
      }
    );

    if (response.data.items && response.data.items.length > 0) {
      console.log(`Found ${response.data.items.length} commits`);
      return response.data.items;
    }
    console.log('No commits found');
    return [];
  } catch (error) {
    console.error('Error fetching commits:', error.response?.data || error);
    return [];
  }
};

// Force evolution based on existing commits
const forceEvolution = async () => {
  try {
    // Get all commits
    const commits = await getLatestCommitsByUser();
    
    if (commits.length === 0) {
      console.log('No commits found. Cannot force evolution.');
      return;
    }
    
    // Sort commits by date (oldest first)
    commits.sort((a, b) => 
      new Date(a.commit.author.date) - new Date(b.commit.author.date)
    );
    
    // Take the first 6 commits (or all if less than 6)
    const commitsToProcess = commits.slice(0, 6);
    console.log(`Processing ${commitsToProcess.length} commits for evolution...`);
    
    // Initialize with default character
    let currentDescription = 'simple explorer facing right with basic pot noodle backpack and plain noodle-colored clothes';
    let currentLevel = 0;
    
    // Create a fresh history file
    const evolutionHistory = [];
    
    // Process each commit to create an evolution
    for (let i = 0; i < commitsToProcess.length; i++) {
      const commit = commitsToProcess[i];
      console.log(`\nProcessing commit ${i+1}/${commitsToProcess.length}: ${commit.commit.message.split('\n')[0]}`);
      
      // Generate improved description
      console.log(`Current character: "${currentDescription}"`);
      const evolutionResult = await generateImprovedCharacterDescription(
        currentDescription,
        currentLevel
      );
      
      // Update current description and level
      const newDescription = evolutionResult.description;
      currentLevel = i + 1;
      
      console.log(`New character: "${newDescription}"`);
      
      // Store evolution details
      evolutionHistory.push({
        level: currentLevel,
        commitSha: commit.sha,
        commitMessage: commit.commit.message.split('\n')[0], // First line of commit message
        commitDate: commit.commit.author.date,
        previousDescription: currentDescription,
        prompt: evolutionResult.prompt,
        newDescription: newDescription
      });
      
      // Update for next iteration
      currentDescription = newDescription;
    }
    
    // Generate the final character
    console.log('\nGenerating final character...');
    await generateCharacter(currentDescription);
    
    // Update history with new state
    const updatedHistory = {
      lastCheckedCommit: commitsToProcess[commitsToProcess.length - 1].sha,
      lastCheckedDate: new Date().toISOString(),
      currentCharacterDescription: currentDescription,
      evolutionLevel: commitsToProcess.length,
      totalCommits: commitsToProcess.length,
      evolutionHistory: evolutionHistory
    };
    
    fs.writeFileSync(COMMIT_HISTORY_FILE, JSON.stringify(updatedHistory, null, 2));
    
    // Copy to assets directory
    copyCommitHistoryToAssets();
    
    console.log(`\nEvolution complete! Generated ${evolutionHistory.length} character evolutions.`);
    console.log(`Final character: "${currentDescription}"`);
    
    return true;
  } catch (error) {
    console.error('Error in force evolution:', error);
    return false;
  }
};

// Run the force evolution
console.log('Starting forced evolution sequence...');
forceEvolution()
  .then(success => {
    if (success) {
      console.log('\nForced evolution completed successfully!');
      console.log('Start the game to see the results.');
    } else {
      console.error('Failed to complete forced evolution.');
    }
  })
  .catch(error => {
    console.error('Error during forced evolution:', error.message);
  }); 