import Phaser from 'phaser';

export default class UIScene extends Phaser.Scene {
  constructor() {
    super('UIScene');
    
    // Terminal display properties
    this.terminal = null;
    this.terminalLines = [];
    this.maxTerminalLines = 25;
    this.terminalWidth = 400;
    this.lineHeight = 20;
    this.terminalScrollPosition = 0;
    this.terminalScrollMax = 0;
    this.isTerminalVisible = false;
    this.totalCommits = 0;
    this.terminalHeight = 0;
    
    // Content area properties
    this.contentPadding = {
      top: 40,    // Space below header
      bottom: 30, // Space above help text
      left: 10,
      right: 10
    };

    // Item counter properties
    this.itemCounter = null;
    this.itemsCollected = 0;
    this.totalItems = 0;
  }

  create() {
    // Create terminal display (initially hidden)
    this.createTerminalDisplay();
    
    // Create the terminal toggle button
    this.createTerminalButton();

    // Create item counter
    this.createItemCounter();
    
    // Listen for resize events to adjust UI
    this.scale.on('resize', this.resize, this);
    
    // Listen for terminal messages from GameScene
    this.game.events.on('terminal-message', this.addTerminalLine, this);

    // Reset counter when game starts
    this.game.events.on('reset-counter', (total) => {
      this.itemsCollected = 0;
      this.totalItems = total;
      this.updateItemCounter();
    });

    // Increment counter when item is collected
    this.game.events.on('increment-counter', () => {
      this.itemsCollected++;
      this.updateItemCounter();
    });

    // Listen for commit count updates (just for the button)
    this.game.events.on('update-commit-count', (count) => {
      this.totalCommits = count;
      this.updateButtonText();
    });
    
    // Add keyboard event for scrolling terminal
    this.input.keyboard.on('keydown-UP', () => {
      if (this.isTerminalVisible) {
        this.scrollTerminal(-1);
      }
    });
    
    this.input.keyboard.on('keydown-DOWN', () => {
      if (this.isTerminalVisible) {
        this.scrollTerminal(1);
      }
    });

    // Add keyboard shortcut for toggling terminal (ESC key)
    this.input.keyboard.on('keydown-ESC', () => {
      this.toggleTerminal();
    });
  }

  createTerminalButton() {
    const padding = 10;
    const buttonStyle = {
      fontSize: '12px',
      color: '#ffffff',
      padding: { x: 12, y: 8 }
    };

    this.terminalButton = this.add.text(
      this.cameras.main.width - padding,
      padding,
      'PotNoodleDev commit | evolution history +',
      buttonStyle
    );
    this.terminalButton.setOrigin(1, 0);
    this.terminalButton.setInteractive({ useHandCursor: true });
    
    // Add hover effects
    this.terminalButton.on('pointerover', () => {
      this.terminalButton.setStyle({ color: '#aaaaaa' });
    });
    
    this.terminalButton.on('pointerout', () => {
      this.terminalButton.setStyle({ color: '#ffffff' });
    });
    
    // Add click handler
    this.terminalButton.on('pointerdown', () => {
      this.toggleTerminal();
    });

    // Remove background rectangle for button
    this.terminalButton.setDepth(1);
  }

  updateButtonText() {
    const commitText = this.totalCommits > 0 ? ` (${this.totalCommits})` : '';
    this.terminalButton.setText(
      this.isTerminalVisible ? 
        `PotNoodleDev commit${commitText} | evolution history -` : 
        `PotNoodleDev commit${commitText} | evolution history +`
    );
  }

  toggleTerminal() {
    this.isTerminalVisible = !this.isTerminalVisible;
    this.terminal.setVisible(this.isTerminalVisible);
    this.updateButtonText();
  }

  resize() {
    // Update terminal position on resize
    if (this.terminal) {
      const terminalX = this.cameras.main.width - this.terminalWidth - 20;
      this.terminal.setPosition(terminalX, 60); // Move down to account for button
    }

    // Update button position
    if (this.terminalButton) {
      const padding = 10;
      this.terminalButton.setPosition(
        this.cameras.main.width - padding,
        padding
      );
    }
  }

  createTerminalDisplay() {
    // Create terminal background
    const terminalX = this.cameras.main.width - this.terminalWidth - 20;
    const terminalY = 60; // Move down to account for button
    this.terminalHeight = this.cameras.main.height - 80; // Store height in class property
    
    // Create terminal container
    this.terminal = this.add.container(terminalX, terminalY);
    this.terminal.setVisible(false); // Initially hidden
    
    // Create terminal background with close button
    const terminalBg = this.add.rectangle(0, 0, this.terminalWidth, this.terminalHeight, 0x000000, 0.9);
    terminalBg.setOrigin(0, 0);
    terminalBg.setStrokeStyle(2, 0xffffff);
    this.terminal.add(terminalBg);
    
    // Create content container
    this.contentContainer = this.add.container(this.contentPadding.left, this.contentPadding.top);
    this.terminal.add(this.contentContainer);
    
    // Create content bounds for clipping
    const bounds = new Phaser.Geom.Rectangle(
      this.contentPadding.left,
      this.contentPadding.top,
      this.terminalWidth - (this.contentPadding.left + this.contentPadding.right),
      this.terminalHeight - (this.contentPadding.top + this.contentPadding.bottom)
    );
    
    // Add content container to terminal
    this.terminal.add(this.contentContainer);
    
    // Create terminal header
    const headerText = this.add.text(
      this.terminalWidth / 2, 
      10, 
      "EVOLUTION TERMINAL", 
      {
        fontFamily: 'Arial',
        fontSize: '16px',
        color: '#ffffff',
        align: 'center',
        fontStyle: 'bold'
      }
    );
    headerText.setOrigin(0.5, 0);
    this.terminal.add(headerText);
    
    // Create divider line
    const divider = this.add.graphics();
    divider.lineStyle(1, 0xffffff, 1);
    divider.lineBetween(10, 30, this.terminalWidth - 10, 30);
    this.terminal.add(divider);
    
    // Create scroll indicators
    this.scrollUpIndicator = this.add.text(
      this.terminalWidth - 20,
      35,
      "▲",
      {
        fontFamily: 'Arial',
        fontSize: '14px',
        color: '#ffffff',
        align: 'center'
      }
    );
    this.scrollUpIndicator.setOrigin(0.5, 0);
    this.scrollUpIndicator.setAlpha(0.5);
    this.terminal.add(this.scrollUpIndicator);
    
    this.scrollDownIndicator = this.add.text(
      this.terminalWidth - 20,
      this.terminalHeight - 20,
      "▼",
      {
        fontFamily: 'Arial',
        fontSize: '14px',
        color: '#ffffff',
        align: 'center'
      }
    );
    this.scrollDownIndicator.setOrigin(0.5, 1);
    this.scrollDownIndicator.setAlpha(0.5);
    this.terminal.add(this.scrollDownIndicator);
    
    // Add help text
    const helpText = this.add.text(
      10,
      this.terminalHeight - 20,
      "UP/DOWN: Scroll | ESC: Toggle",
      {
        fontFamily: 'Arial',
        fontSize: '10px',
        color: '#ffffff',
        align: 'left'
      }
    );
    helpText.setOrigin(0, 1);
    this.terminal.add(helpText);
  }

  addTerminalLine(text) {
    // Create text style for terminal
    const textStyle = {
      fontSize: '12px',
      color: '#ffffff',
      align: 'left',
      wordWrap: { 
        width: this.terminalWidth - (this.contentPadding.left + this.contentPadding.right + 20),
        useAdvancedWrap: true
      }
    };
    
    // Create text object
    const textObject = this.add.text(0, 0, text, textStyle);
    textObject.setOrigin(0, 0);
    
    // Calculate y position for new line
    let yPosition = 0;
    if (this.terminalLines.length > 0) {
      const lastLine = this.terminalLines[this.terminalLines.length - 1];
      yPosition = lastLine.y + lastLine.height + 5; // 5px spacing between lines
    }
    textObject.setY(yPosition);
    
    // Add to content container
    this.contentContainer.add(textObject);
    this.terminalLines.push(textObject);
    
    // Calculate total content height and visible area
    const contentHeight = yPosition + textObject.height;
    const visibleHeight = this.terminalHeight - (this.contentPadding.top + this.contentPadding.bottom);
    
    // Update max scroll position
    this.terminalScrollMax = Math.max(0, Math.floor((contentHeight - visibleHeight) / this.lineHeight));
    
    // Auto-scroll to bottom when new content is added
    if (this.terminalScrollMax > 0) {
      this.terminalScrollPosition = this.terminalScrollMax;
      this.updateTerminalScroll();
    }
    
    return textObject;
  }
  
  scrollTerminal(direction) {
    // Update scroll position
    this.terminalScrollPosition = Phaser.Math.Clamp(
      this.terminalScrollPosition + direction,
      0,
      this.terminalScrollMax
    );
    
    // Update terminal display
    this.updateTerminalScroll();
  }
  
  updateTerminalScroll() {
    // Calculate scroll offset
    const scrollOffset = this.terminalScrollPosition * this.lineHeight;
    
    // Update content container position
    this.contentContainer.setY(this.contentPadding.top - scrollOffset);
    
    // Hide lines that are outside the visible area
    const visibleHeight = this.cameras.main.height - 80 - (this.contentPadding.top + this.contentPadding.bottom);
    const startY = scrollOffset;
    const endY = startY + visibleHeight;
    
    this.terminalLines.forEach(line => {
      const lineY = line.y + this.contentContainer.y;
      line.setVisible(lineY >= this.contentPadding.top - line.height && lineY <= visibleHeight);
    });
    
    // Update scroll indicators
    this.scrollUpIndicator.setAlpha(this.terminalScrollPosition > 0 ? 1 : 0.3);
    this.scrollDownIndicator.setAlpha(this.terminalScrollPosition < this.terminalScrollMax ? 1 : 0.3);
  }
  
  clearTerminal() {
    // Remove all terminal lines
    this.terminalLines.forEach(line => {
      line.destroy();
    });
    this.terminalLines = [];
    
    // Reset scroll position
    this.terminalScrollPosition = 0;
    this.terminalScrollMax = 0;
  }

  createItemCounter() {
    // Create counter text only, no background
    const padding = 10;
    const bgWidth = 150;
    const bgHeight = 40;
    
    this.itemCounter = this.add.text(
      padding + bgWidth/2,
      padding + bgHeight/2,
      'Pot Noodles: 0/0',
      {
        fontSize: '12px',
        color: '#ffffff',
        align: 'center'
      }
    );
    this.itemCounter.setOrigin(0.5);
  }

  updateItemCounter() {
    if (this.itemCounter) {
      this.itemCounter.setText(`Pot Noodles: ${this.itemsCollected}/${this.totalItems}`);
    }
  }
} 