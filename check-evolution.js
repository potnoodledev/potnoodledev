#!/usr/bin/env node

/**
 * Manual Character Evolution Check
 * 
 * This script manually triggers a check for new GitHub commits
 * and evolves the character if needed.
 * 
 * Run with: node check-evolution.js
 */

const { checkForEvolution } = require('./src/scripts/character-evolution');

console.log('Manually checking for character evolution...');

// Run the check and handle the promise
checkForEvolution()
  .then(() => {
    console.log('Evolution check completed.');
  })
  .catch(error => {
    console.error('Error during evolution check:', error);
  }); 