const axios = require('axios');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
require('dotenv').config(); // Load environment variables from .env file

// Configuration
const GITHUB_USERNAME = 'potnoodledev';
const COMMIT_CHECK_INTERVAL = 60 * 60 * 1000; // Check every hour (in milliseconds)
const COMMIT_HISTORY_FILE = path.join(__dirname, '../../commit-history.json');
const ASSETS_HISTORY_FILE = path.join(__dirname, '../../src/assets/commit-history.json');
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const COMMITS_PER_EVOLUTION = 1; // Changed from 3 to 1 - evolve at every commit

// Initialize commit history file if it doesn't exist
if (!fs.existsSync(COMMIT_HISTORY_FILE)) {
  fs.writeFileSync(COMMIT_HISTORY_FILE, JSON.stringify({
    lastCheckedCommit: '',
    currentCharacterDescription: 'Noodle scout facing right, explorer tunic, wooden spoon, steaming backpack',
    evolutionLevel: 0,
    totalCommits: 0,
    evolutionHistory: [] // Array to store evolution history
  }));
}

// Ensure assets directory exists
const assetsDir = path.dirname(ASSETS_HISTORY_FILE);
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir, { recursive: true });
}

// Copy commit history to assets directory
function copyCommitHistoryToAssets() {
  try {
    fs.copyFileSync(COMMIT_HISTORY_FILE, ASSETS_HISTORY_FILE);
    console.log('Copied commit history to assets directory');
  } catch (error) {
    console.error('Error copying commit history to assets:', error.message);
  }
}

// Initial copy
copyCommitHistoryToAssets();

/**
 * Get the latest commits by the specified GitHub user
 */
const getLatestCommitsByUser = async () => {
  try {
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
      return response.data.items;
    }
    return [];
  } catch (error) {
    console.error('Error fetching commits:', error.response?.data || error);
    return [];
  }
};

/**
 * Use Claude to generate an improved character description
 */
const generateImprovedCharacterDescription = async (currentDescription, evolutionLevel) => {
  try {
    if (!ANTHROPIC_API_KEY) {
      throw new Error('ANTHROPIC_API_KEY not found in environment variables');
    }

    console.log(`Asking Claude to improve character: "${currentDescription}" (Level ${evolutionLevel})`);

    const prompt = `You are a creative game character designer specializing in pot noodle-themed characters. I have a pixel art character in my game described as: "${currentDescription}".

This character is at evolution level ${evolutionLevel} and has just evolved to level ${evolutionLevel + 1}.

Please create an IMPROVED description that builds upon the current character. The improvement should be clear and drawable in pixel art style.

The character description MUST follow this structure:
1. Character type and basic pose (e.g., "Explorer facing right")
2. Main clothing/armor (maximum 2 items)
3. ONE primary tool or weapon
4. ONE special effect or aura (if any)

Keep in mind:
- Descriptions must be simple enough to draw in 32x32 pixel art
- Each element should be clearly visible from a top-down view
- Avoid overlapping or complex layered effects
- Limit particle effects and floating elements
- Keep color descriptions simple and clear

Examples of good elements:
- "Pot noodle backpack with steam vent"
- "Noodle-woven cloak"
- "Glowing wooden spoon"
- "Simple steam aura"

The description should:
1. Be very concise (20 words or less)
2. Use simple, clear visual elements
3. Add only ONE new feature compared to the previous form
4. Keep the character instantly recognizable
5. IMPORTANT: The character must be facing RIGHT
6. Focus on elements that work in pixel art

ONLY respond with the new character description text, nothing else. No explanations, no intro text, just the description.`;

    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      {
        model: 'claude-3-sonnet-20240229',
        max_tokens: 1000,
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01'
        }
      }
    );

    // Extract the improved description from Claude's response
    const improvedDescription = response.data.content[0].text.trim();
    console.log(`Claude generated improved description: "${improvedDescription}"`);
    
    // Return both the prompt and the response
    return {
      prompt: prompt,
      description: improvedDescription
    };
  } catch (error) {
    console.error('Error generating improved character description:', error.response?.data || error.message);
    
    // Fallback descriptions in case Claude API fails
    const fallbackDescriptions = [
      'explorer facing right, simple clothes, wooden spoon, pot noodle backpack',
      'explorer facing right, noodle-patterned clothes, glowing spoon, steaming backpack',
      'noodle scout facing right, light armor, spoon staff, steam aura',
      'noodle mage facing right, protective robes, magic ladle, floating noodles',
      'noodle master facing right, armored robes, golden spoon staff, glowing broth aura'
    ];
    
    // Use a fallback description based on the evolution level
    const fallbackIndex = Math.min(evolutionLevel, fallbackDescriptions.length - 1);
    console.log(`Using fallback description: "${fallbackDescriptions[fallbackIndex]}"`);
    
    // Return a fallback object
    return {
      prompt: "Fallback used due to API error",
      description: fallbackDescriptions[fallbackIndex]
    };
  }
};

/**
 * Generate a new character based on the description
 */
const generateCharacter = (characterDescription) => {
  return new Promise((resolve, reject) => {
    console.log(`Generating character: ${characterDescription}`);
    
    // Ensure the description includes "facing right" if not already present
    const finalDescription = characterDescription.toLowerCase().includes('facing right') 
      ? characterDescription 
      : `${characterDescription} facing right`;
    
    // First generate the animation frames
    const animationCommand = `python asset_generator/generate_character.py --description "${finalDescription}" --animation`;
    
    exec(animationCommand, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error generating character animation: ${error.message}`);
        reject(error);
        return;
      }
      
      if (stderr) {
        console.error(`Character animation generation stderr: ${stderr}`);
      }
      
      console.log(`Character animation generation output: ${stdout}`);
      
      // Now copy the first frame of the walk animation to be the idle character
      const projectRoot = path.resolve(__dirname, '../..');
      const walkFramePath = path.join(projectRoot, 'src/assets/images/player/walk/frame_1.png');
      const playerPath = path.join(projectRoot, 'src/assets/images/player.png');
      
      // Check if the walk frame exists
      if (fs.existsSync(walkFramePath)) {
        try {
          // Copy the first frame to be the idle character
          fs.copyFileSync(walkFramePath, playerPath);
          console.log(`Successfully copied walk frame_1.png to player.png`);
          resolve();
        } catch (copyError) {
          console.error(`Error copying walk frame to player.png: ${copyError.message}`);
          reject(copyError);
        }
      } else {
        console.error(`Walk frame does not exist at path: ${walkFramePath}`);
        reject(new Error(`Walk frame does not exist at path: ${walkFramePath}`));
      }
    });
  });
};

/**
 * Reset the evolution history to start fresh
 */
const resetEvolutionHistory = async () => {
  try {
    // Create a fresh history file
    const freshHistory = {
      lastCheckedCommit: '',
      currentCharacterDescription: 'Noodle scout facing right, explorer tunic, wooden spoon, steaming backpack',
      evolutionLevel: 0,
      totalCommits: 0,
      evolutionHistory: []
    };
    
    // Write to file
    fs.writeFileSync(COMMIT_HISTORY_FILE, JSON.stringify(freshHistory, null, 2));
    
    // Copy to assets
    copyCommitHistoryToAssets();
    
    console.log('Evolution history reset successfully');
    
    // Generate the initial character
    await generateCharacter('Noodle scout facing right, explorer tunic, wooden spoon, steaming backpack');
    
    return true;
  } catch (error) {
    console.error('Error resetting evolution history:', error);
    return false;
  }
};

/**
 * Check for new commits and evolve the character if needed
 */
const checkForEvolution = async () => {
  try {
    // Load current state
    const historyData = JSON.parse(fs.readFileSync(COMMIT_HISTORY_FILE, 'utf8'));
    const { 
      lastCheckedCommit, 
      currentCharacterDescription, 
      evolutionLevel, 
      totalCommits,
      evolutionHistory = [] // Default to empty array if not present
    } = historyData;
    
    // Get latest commits
    const commits = await getLatestCommitsByUser();
    
    if (commits.length === 0) {
      console.log('No commits found or error fetching commits');
      return;
    }
    
    // Get the latest commit SHA
    const latestCommitSha = commits[0].sha;
    
    // If this is the first check or we have a new commit
    if (!lastCheckedCommit || latestCommitSha !== lastCheckedCommit) {
      // Count new commits
      const newCommits = commits.filter(commit => 
        !lastCheckedCommit || 
        new Date(commit.commit.author.date) > new Date(historyData.lastCheckedDate || 0)
      );
      
      const updatedTotalCommits = totalCommits + newCommits.length;
      
      // Calculate new evolution level (one level per commit)
      const newEvolutionLevel = Math.floor(updatedTotalCommits / COMMITS_PER_EVOLUTION);
      
      // If we've reached a new evolution level, generate a new character
      if (newEvolutionLevel > evolutionLevel) {
        console.log(`Evolution triggered! Level ${evolutionLevel} -> ${newEvolutionLevel}`);
        
        // Process each new evolution level
        let currentDesc = currentCharacterDescription;
        let currentLevel = evolutionLevel;
        
        // Store new evolutions
        const newEvolutions = [];
        
        // For each new level, generate a character evolution
        for (let level = evolutionLevel + 1; level <= newEvolutionLevel; level++) {
          // Get the commit that triggered this evolution
          const commitIndex = level - evolutionLevel - 1;
          const commit = newCommits[commitIndex];
          
          // Use Claude to generate an improved character description
          const evolutionResult = await generateImprovedCharacterDescription(
            currentDesc,
            currentLevel
          );
          
          // Update current description and level for next iteration
          currentDesc = evolutionResult.description;
          currentLevel = level;
          
          // Store evolution details
          newEvolutions.push({
            level: level,
            commitSha: commit.sha,
            commitMessage: commit.commit.message.split('\n')[0], // First line of commit message
            commitDate: commit.commit.author.date,
            previousDescription: level === evolutionLevel + 1 ? currentCharacterDescription : newEvolutions[newEvolutions.length - 1].newDescription,
            prompt: evolutionResult.prompt,
            newDescription: evolutionResult.description
          });
        }
        
        // Generate the final character
        await generateCharacter(currentDesc);
        
        // Update history with new state
        const updatedHistory = {
          lastCheckedCommit: latestCommitSha,
          lastCheckedDate: new Date().toISOString(),
          currentCharacterDescription: currentDesc,
          evolutionLevel: newEvolutionLevel,
          totalCommits: updatedTotalCommits,
          evolutionHistory: [...evolutionHistory, ...newEvolutions]
        };
        
        fs.writeFileSync(COMMIT_HISTORY_FILE, JSON.stringify(updatedHistory, null, 2));
        
        // Copy to assets directory
        copyCommitHistoryToAssets();
        
        console.log(`Character evolved successfully to: "${currentDesc}"`);
      } else {
        // Just update the last checked commit
        const updatedHistory = {
          ...historyData,
          lastCheckedCommit: latestCommitSha,
          lastCheckedDate: new Date().toISOString(),
          totalCommits: updatedTotalCommits
        };
        
        fs.writeFileSync(COMMIT_HISTORY_FILE, JSON.stringify(updatedHistory, null, 2));
        
        // Copy to assets directory
        copyCommitHistoryToAssets();
        
        console.log(`New commits found, but not enough for evolution. ` +
                   `Current progress: ${updatedTotalCommits % COMMITS_PER_EVOLUTION}/${COMMITS_PER_EVOLUTION} commits toward next level.`);
      }
    } else {
      console.log('No new commits found');
    }
  } catch (error) {
    console.error('Error in evolution check:', error);
  }
};

// Run the check immediately on startup
checkForEvolution();

// Then set up interval to check periodically
setInterval(checkForEvolution, COMMIT_CHECK_INTERVAL);

console.log(`Character evolution system started. Checking for commits by ${GITHUB_USERNAME} every ${COMMIT_CHECK_INTERVAL/1000/60} minutes.`);

module.exports = {
  checkForEvolution,
  getLatestCommitsByUser,
  generateImprovedCharacterDescription,
  generateCharacter,
  resetEvolutionHistory
}; 