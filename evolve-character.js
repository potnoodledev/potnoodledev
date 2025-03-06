#!/usr/bin/env node

/**
 * Character Evolution System
 * 
 * This script starts the character evolution system that:
 * 1. Immediately checks for any unprocessed commits
 * 2. Then continues to check periodically (default: every hour)
 * 
 * You can override the check interval with an environment variable:
 * COMMIT_CHECK_INTERVAL_MINUTES=30 node evolve-character.js
 * 
 * Run with: node evolve-character.js
 */

const { checkForEvolution } = require('./src/scripts/character-evolution');

// Get check interval from environment or use default (60 minutes)
const checkIntervalMinutes = process.env.COMMIT_CHECK_INTERVAL_MINUTES || 60;
const checkIntervalMs = checkIntervalMinutes * 60 * 1000;

console.log('Character Evolution System Starting...');
console.log('----------------------------------------');
console.log('1. Checking for unprocessed commits now...');

// First check immediately
checkForEvolution().then(() => {
  console.log('----------------------------------------');
  console.log(`2. Will check again every ${checkIntervalMinutes} minutes`);
  console.log('Press Ctrl+C to stop');
  
  // Then set up periodic checks
  setInterval(checkForEvolution, checkIntervalMs);
}); 