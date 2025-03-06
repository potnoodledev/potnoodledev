#!/usr/bin/env node

/**
 * Character Evolution Script
 * 
 * This script checks for new GitHub commits by potnoodledev and evolves
 * the game character when new commits are detected.
 * 
 * Run with: node evolve-character.js
 */

// Import the character evolution system
require('./src/scripts/character-evolution');

console.log('Character evolution system is running...');
console.log('Press Ctrl+C to stop'); 