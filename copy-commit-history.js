#!/usr/bin/env node

/**
 * Copy Commit History Script
 * 
 * This script copies the commit-history.json file from the project root
 * to the assets directory so it can be loaded by the game.
 * 
 * Run with: node copy-commit-history.js
 */

const fs = require('fs');
const path = require('path');

// Paths
const sourceFile = path.join(__dirname, 'commit-history.json');
const targetDir = path.join(__dirname, 'src', 'assets');
const targetFile = path.join(targetDir, 'commit-history.json');

// Check if source file exists
if (!fs.existsSync(sourceFile)) {
  console.log('No commit-history.json file found in project root. Creating a default one...');
  
  // Create a default commit history file
  const defaultHistory = {
    lastCheckedCommit: '',
    currentCharacterDescription: 'simple wanderer with plain clothes',
    evolutionLevel: 0,
    totalCommits: 0
  };
  
  // Write to source location
  fs.writeFileSync(sourceFile, JSON.stringify(defaultHistory, null, 2));
  console.log(`Created default commit-history.json in project root.`);
}

// Ensure target directory exists
if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
  console.log(`Created directory: ${targetDir}`);
}

// Copy the file
try {
  fs.copyFileSync(sourceFile, targetFile);
  console.log(`Successfully copied commit-history.json to ${targetFile}`);
} catch (error) {
  console.error(`Error copying file: ${error.message}`);
} 