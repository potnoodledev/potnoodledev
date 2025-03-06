#!/usr/bin/env node

/**
 * Reset Evolution History Script
 * 
 * This script resets the evolution history to start fresh with the initial character.
 * 
 * Run with: node reset-evolution.js
 */

const { resetEvolutionHistory } = require('./src/scripts/character-evolution');

console.log('Resetting evolution history...');

resetEvolutionHistory()
  .then(success => {
    if (success) {
      console.log('Evolution history reset successfully!');
      console.log('Character has been reset to "simple wanderer with plain clothes"');
      console.log('Ready to start fresh evolution sequence.');
    } else {
      console.error('Failed to reset evolution history.');
    }
  })
  .catch(error => {
    console.error('Error resetting evolution history:', error.message);
  }); 