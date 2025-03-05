/**
 * itchCommentsFetcher.js
 * 
 * A script to fetch the latest comments from an itch.io game page.
 * This uses web scraping with axios and cheerio since itch.io doesn't provide a public API.
 */

const axios = require('axios');
const cheerio = require('cheerio');

/**
 * Fetches the latest comments from an itch.io game page
 * @param {string} username - The itch.io username of the game developer
 * @param {string} gameName - The name of the game as it appears in the URL
 * @param {number} limit - Maximum number of comments to retrieve (default: 10)
 * @returns {Promise<Array>} - Array of comment objects with author, date, and text
 */
async function fetchItchComments(username, gameName, limit = 10) {
  try {
    // Construct the URL for the game page
    const url = `https://${username}.itch.io/${gameName}`;
    
    console.log(`Fetching comments from: ${url}`);
    
    // Make the HTTP request to the game page
    const response = await axios.get(url);
    
    // Load the HTML into cheerio
    const $ = cheerio.load(response.data);
    
    // Find the comments section and extract comments
    const comments = [];
    
    // The comments are typically in elements with class 'post_grid'
    $('.post_grid').each((index, element) => {
      if (index >= limit) return false; // Stop after reaching the limit
      
      const $element = $(element);
      
      // Extract comment data
      const author = $element.find('.post_author a').text().trim();
      const date = $element.find('.post_date').text().trim();
      const text = $element.find('.post_body').text().trim();
      
      comments.push({
        author,
        date,
        text
      });
    });
    
    if (comments.length === 0) {
      console.log('No comments found or the page structure might have changed.');
    } else {
      console.log(`Found ${comments.length} comments.`);
    }
    
    return comments;
  } catch (error) {
    console.error('Error fetching comments:', error.message);
    throw error;
  }
}

/**
 * Example usage:
 * 
 * fetchItchComments('potnoodledev', 'evolve', 5)
 *   .then(comments => {
 *     console.log(JSON.stringify(comments, null, 2));
 *   })
 *   .catch(error => {
 *     console.error('Failed to fetch comments:', error);
 *   });
 */

module.exports = { fetchItchComments }; 