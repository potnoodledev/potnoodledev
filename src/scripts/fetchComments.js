#!/usr/bin/env node

/**
 * fetchComments.js
 * 
 * Command-line script to fetch and display the latest comments from an itch.io game page.
 * 
 * Usage:
 *   node fetchComments.js <username> <game-name> [limit]
 * 
 * Example:
 *   node fetchComments.js potnoodledev evolve 5
 */

const { fetchItchComments } = require('./itchCommentsFetcher');

// Parse command line arguments
const args = process.argv.slice(2);
const username = args[0];
const gameName = args[1];
const limit = args[2] ? parseInt(args[2], 10) : 10;

// Validate arguments
if (!username || !gameName) {
  console.error('Error: Missing required arguments.');
  console.log('\nUsage:');
  console.log('  node fetchComments.js <username> <game-name> [limit]');
  console.log('\nExample:');
  console.log('  node fetchComments.js potnoodledev evolve 5');
  process.exit(1);
}

// Display a nice header
console.log('\n==============================================');
console.log(`Fetching comments for ${username}/${gameName}`);
console.log('==============================================\n');

// Fetch and display comments
fetchItchComments(username, gameName, limit)
  .then(comments => {
    if (comments.length === 0) {
      console.log('No comments found.');
    } else {
      comments.forEach((comment, index) => {
        console.log(`\n--- Comment #${index + 1} ---`);
        console.log(`Author: ${comment.author}`);
        console.log(`Date: ${comment.date}`);
        console.log(`\n${comment.text}\n`);
        console.log('-'.repeat(30));
      });
    }
  })
  .catch(error => {
    console.error('Failed to fetch comments:', error.message);
    process.exit(1);
  }); 