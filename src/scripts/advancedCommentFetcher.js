#!/usr/bin/env node

/**
 * advancedCommentFetcher.js
 * 
 * An advanced script to fetch comments from an itch.io game page,
 * save them to a file, and track new comments since the last check.
 * 
 * Usage:
 *   node advancedCommentFetcher.js <username> <game-name> [options]
 * 
 * Options:
 *   --limit=<number>       Maximum number of comments to retrieve (default: 20)
 *   --output=<file-path>   Path to save comments (default: ./comments.json)
 *   --notify-only-new      Only display new comments since last check
 *   --format=<json|text>   Output format (default: json)
 */

const fs = require('fs');
const path = require('path');
const { fetchItchComments } = require('./itchCommentsFetcher');

// Parse command line arguments
const args = process.argv.slice(2);
const options = {
  limit: 20,
  output: './comments.json',
  notifyOnlyNew: false,
  format: 'json'
};

// Extract username and game name
const username = args[0];
const gameName = args[1];

// Parse options
args.slice(2).forEach(arg => {
  if (arg.startsWith('--limit=')) {
    options.limit = parseInt(arg.split('=')[1], 10);
  } else if (arg.startsWith('--output=')) {
    options.output = arg.split('=')[1];
  } else if (arg === '--notify-only-new') {
    options.notifyOnlyNew = true;
  } else if (arg.startsWith('--format=')) {
    options.format = arg.split('=')[1];
  }
});

// Validate arguments
if (!username || !gameName) {
  console.error('Error: Missing required arguments.');
  console.log('\nUsage:');
  console.log('  node advancedCommentFetcher.js <username> <game-name> [options]');
  console.log('\nOptions:');
  console.log('  --limit=<number>       Maximum number of comments to retrieve (default: 20)');
  console.log('  --output=<file-path>   Path to save comments (default: ./comments.json)');
  console.log('  --notify-only-new      Only display new comments since last check');
  console.log('  --format=<json|text>   Output format (default: json)');
  console.log('\nExample:');
  console.log('  node advancedCommentFetcher.js potnoodledev evolve --limit=10 --output=./game-comments.json');
  process.exit(1);
}

/**
 * Reads previously saved comments from a file
 * @param {string} filePath - Path to the comments file
 * @returns {Array} - Array of previously saved comments or empty array if file doesn't exist
 */
function readPreviousComments(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.warn(`Warning: Could not read previous comments file: ${error.message}`);
  }
  return [];
}

/**
 * Saves comments to a file
 * @param {Array} comments - Array of comment objects
 * @param {string} filePath - Path to save the comments
 */
function saveComments(comments, filePath) {
  try {
    // Create directory if it doesn't exist
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(filePath, JSON.stringify(comments, null, 2), 'utf8');
    console.log(`Comments saved to ${filePath}`);
  } catch (error) {
    console.error(`Error saving comments: ${error.message}`);
  }
}

/**
 * Identifies new comments that weren't in the previous fetch
 * @param {Array} currentComments - Current comments
 * @param {Array} previousComments - Previously saved comments
 * @returns {Array} - Array of new comments
 */
function findNewComments(currentComments, previousComments) {
  if (!previousComments.length) return currentComments;
  
  // Create a simple hash for each previous comment for comparison
  const previousHashes = new Set();
  previousComments.forEach(comment => {
    const hash = `${comment.author}|${comment.text}`;
    previousHashes.add(hash);
  });
  
  // Filter out comments that already exist
  return currentComments.filter(comment => {
    const hash = `${comment.author}|${comment.text}`;
    return !previousHashes.has(hash);
  });
}

/**
 * Formats and displays comments
 * @param {Array} comments - Array of comment objects
 * @param {string} format - Output format ('json' or 'text')
 */
function displayComments(comments, format) {
  if (comments.length === 0) {
    console.log('No comments found.');
    return;
  }
  
  if (format === 'json') {
    console.log(JSON.stringify(comments, null, 2));
  } else {
    comments.forEach((comment, index) => {
      console.log(`\n--- Comment #${index + 1} ---`);
      console.log(`Author: ${comment.author}`);
      console.log(`Date: ${comment.date}`);
      console.log(`\n${comment.text}\n`);
      console.log('-'.repeat(30));
    });
  }
}

// Main execution
async function main() {
  try {
    console.log('\n==============================================');
    console.log(`Fetching comments for ${username}/${gameName}`);
    console.log('==============================================\n');
    
    // Fetch comments
    const comments = await fetchItchComments(username, gameName, options.limit);
    
    // Read previous comments
    const previousComments = readPreviousComments(options.output);
    
    // Find new comments
    const newComments = findNewComments(comments, previousComments);
    
    // Save all comments
    saveComments(comments, options.output);
    
    // Display comments based on options
    if (options.notifyOnlyNew) {
      console.log(`\nFound ${newComments.length} new comments since last check.`);
      displayComments(newComments, options.format);
    } else {
      console.log(`\nDisplaying all ${comments.length} comments:`);
      displayComments(comments, options.format);
    }
    
  } catch (error) {
    console.error('Failed to fetch comments:', error.message);
    process.exit(1);
  }
}

main(); 