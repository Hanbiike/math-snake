class MathSnakeGame {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Constants
        this.GRID_SIZE = 20;
        this.GRID_WIDTH = this.canvas.width / this.GRID_SIZE;
        this.GRID_HEIGHT = this.canvas.height / this.GRID_SIZE;
        
        // Game state
        this.gameState = 'menu'; // menu, game, game_over
        this.operation = 'addition';
        this.difficulty = 'level1';
        this.colorMode = 'different';
        this.score = 0;
        
        // Snake
        this.snake = [{ x: Math.floor(this.GRID_WIDTH / 2), y: Math.floor(this.GRID_HEIGHT / 2) }];
        this.direction = { x: 1, y: 0 };
        
        // Math
        this.currentExpression = '';
        this.correctAnswer = 0;
        this.numbersOnField = [];
        
        this.setupEventListeners();
        this.setupUI();
        this.generateNewExpression();
        this.generateNumbers();
        this.gameLoop();
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // Menu option clicks
        document.querySelectorAll('.option').forEach(option => {
            option.addEventListener('click', () => {
                const key = option.dataset.key;
                this.handleMenuSelection(key);
            });
        });
    }
    
    setupUI() {
        this.updateMenuSelections();
    }
    
    updateMenuSelections() {
        // Clear all selections
        document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
        
        // Set current selections
        const operationMap = { 'addition': '1', 'subtraction': '2', 'multiplication': '3', 'division': '4', 'modulo': '5' };
        const difficultyMap = { 'level1': 'q', 'level2': 'w', 'level3': 'e', 'level4': 'r', 'level5': 't' };
        
        document.querySelector(`[data-key="${operationMap[this.operation]}"]`)?.classList.add('selected');
        document.querySelector(`[data-key="${difficultyMap[this.difficulty]}"]`)?.classList.add('selected');
        document.querySelector('[data-key="c"]')?.classList.add('selected');
        
        // Update color mode text
        const colorModeText = this.colorMode === 'different' ? 'C. Разные цвета (синий/красный)' : 'C. Одинаковый цвет';
        document.getElementById('color-mode-option').textContent = colorModeText;
    }
    
    handleKeyPress(e) {
        // Prevent default behavior for arrow keys and space to avoid page scrolling
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
            e.preventDefault();
        }
        
        if (this.gameState === 'menu') {
            this.handleMenuKey(e.key.toLowerCase());
        } else if (this.gameState === 'game') {
            this.handleGameKey(e.key);
        } else if (this.gameState === 'game_over') {
            if (e.key !== 'F5') {
                this.gameState = 'menu';
                this.showScreen('menu');
            }
        }
    }
    
    handleMenuKey(key) {
        this.handleMenuSelection(key);
    }
    
    handleMenuSelection(key) {
        switch (key) {
            case '1': this.operation = 'addition'; break;
            case '2': this.operation = 'subtraction'; break;
            case '3': this.operation = 'multiplication'; break;
            case '4': this.operation = 'division'; break;
            case '5': this.operation = 'modulo'; break;
            case 'q': this.difficulty = 'level1'; break;
            case 'w': this.difficulty = 'level2'; break;
            case 'e': this.difficulty = 'level3'; break;
            case 'r': this.difficulty = 'level4'; break;
            case 't': this.difficulty = 'level5'; break;
            case 'c': 
                this.colorMode = this.colorMode === 'different' ? 'same' : 'different';
                break;
            case ' ':
                this.startGame();
                return;
        }
        this.updateMenuSelections();
    }
    
    handleGameKey(key) {
        switch (key) {
            case 'ArrowUp':
                if (this.direction.y !== 1) this.direction = { x: 0, y: -1 };
                break;
            case 'ArrowDown':
                if (this.direction.y !== -1) this.direction = { x: 0, y: 1 };
                break;
            case 'ArrowLeft':
                if (this.direction.x !== 1) this.direction = { x: -1, y: 0 };
                break;
            case 'ArrowRight':
                if (this.direction.x !== -1) this.direction = { x: 1, y: 0 };
                break;
            case 'Escape':
                this.gameState = 'menu';
                this.showScreen('menu');
                break;
        }
    }
    
    startGame() {
        this.gameState = 'game';
        this.score = 0;
        this.snake = [{ x: Math.floor(this.GRID_WIDTH / 2), y: Math.floor(this.GRID_HEIGHT / 2) }];
        this.direction = { x: 1, y: 0 };
        this.generateNewExpression();
        this.generateNumbers();
        this.showScreen('game');
        this.updateGameUI();
    }
    
    generateNewExpression() {
        let num1, num2;
        
        switch (this.difficulty) {
            case 'level1':
                num1 = Math.floor(Math.random() * 9) + 1;
                num2 = Math.floor(Math.random() * 9) + 1;
                break;
            case 'level2':
                num1 = Math.floor(Math.random() * 90) + 10;
                num2 = Math.floor(Math.random() * 90) + 10;
                break;
            case 'level3':
                num1 = Math.floor(Math.random() * 900) + 100;
                num2 = Math.floor(Math.random() * 900) + 100;
                break;
            case 'level4':
                num1 = Math.floor(Math.random() * 9000) + 1000;
                num2 = Math.floor(Math.random() * 9000) + 1000;
                break;
            case 'level5':
                num1 = Math.floor(Math.random() * 9999) + 1;
                num2 = Math.floor(Math.random() * 9999) + 1;
                break;
        }
        
        let operatorSymbol;
        switch (this.operation) {
            case 'addition':
                this.correctAnswer = num1 + num2;
                operatorSymbol = '+';
                break;
            case 'subtraction':
                if (num1 < num2) [num1, num2] = [num2, num1];
                this.correctAnswer = num1 - num2;
                operatorSymbol = '-';
                break;
            case 'multiplication':
                this.correctAnswer = num1 * num2;
                operatorSymbol = '*';
                break;
            case 'division':
                num1 = num2 * Math.floor(Math.random() * 10 + 1);
                this.correctAnswer = Math.floor(num1 / num2);
                operatorSymbol = '/';
                break;
            case 'modulo':
                if (num2 === 1) num2 = 2;
                this.correctAnswer = num1 % num2;
                operatorSymbol = '%';
                break;
        }
        
        this.currentExpression = `${num1} ${operatorSymbol} ${num2} = ?`;
    }
    
    generateNumbers() {
        this.numbersOnField = [];
        
        // Add correct answer
        const correctPos = {
            x: Math.floor(Math.random() * (this.GRID_WIDTH - 4)) + 2,
            y: Math.floor(Math.random() * (this.GRID_HEIGHT - 6)) + 3
        };
        this.numbersOnField.push({ pos: correctPos, number: this.correctAnswer, isCorrect: true });
        
        // Add wrong answers
        const usedPositions = new Set([`${correctPos.x},${correctPos.y}`]);
        for (let i = 0; i < 8; i++) {
            let pos;
            do {
                pos = {
                    x: Math.floor(Math.random() * (this.GRID_WIDTH - 4)) + 2,
                    y: Math.floor(Math.random() * (this.GRID_HEIGHT - 6)) + 3
                };
            } while (usedPositions.has(`${pos.x},${pos.y}`) || this.isSnakePosition(pos));
            
            usedPositions.add(`${pos.x},${pos.y}`);
            const wrongAnswer = this.generateWrongAnswer();
            this.numbersOnField.push({ pos, number: wrongAnswer, isCorrect: false });
        }
    }
    
    generateWrongAnswer() {
        let variation = Math.floor(Math.random() * 21) - 10;
        if (variation === 0) variation = Math.random() < 0.5 ? -1 : 1;
        return Math.max(0, this.correctAnswer + variation);
    }
    
    isSnakePosition(pos) {
        return this.snake.some(segment => segment.x === pos.x && segment.y === pos.y);
    }
    
    updateGame() {
        if (this.gameState !== 'game') return;
        
        // Move snake
        const head = { x: this.snake[0].x + this.direction.x, y: this.snake[0].y + this.direction.y };
        
        // Check wall collision
        if (head.x < 0 || head.x >= this.GRID_WIDTH || head.y < 0 || head.y >= this.GRID_HEIGHT) {
            this.gameOver();
            return;
        }
        
        // Check self collision
        if (this.snake.some(segment => segment.x === head.x && segment.y === head.y)) {
            this.gameOver();
            return;
        }
        
        this.snake.unshift(head);
        
        // Check number collision
        const eatenNumber = this.numbersOnField.find(num => num.pos.x === head.x && num.pos.y === head.y);
        if (eatenNumber) {
            if (eatenNumber.isCorrect) {
                this.score += 10;
                this.generateNewExpression();
                this.generateNumbers();
                this.updateGameUI();
            } else {
                this.gameOver();
                return;
            }
        } else {
            this.snake.pop();
        }
    }
    
    gameOver() {
        this.gameState = 'game_over';
        document.getElementById('final-score').textContent = `Ваш счёт: ${this.score}`;
        this.showScreen('game-over');
    }
    
    updateGameUI() {
        document.getElementById('expression').textContent = this.currentExpression;
        document.getElementById('score').textContent = `Счёт: ${this.score}`;
    }
    
    showScreen(screenName) {
        document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
        document.getElementById(screenName).classList.remove('hidden');
    }
    
    draw() {
        if (this.gameState !== 'game') return;
        
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw snake
        this.ctx.fillStyle = '#0f0';
        this.snake.forEach(segment => {
            this.ctx.fillRect(
                segment.x * this.GRID_SIZE,
                segment.y * this.GRID_SIZE,
                this.GRID_SIZE,
                this.GRID_SIZE
            );
        });
        
        // Draw numbers
        this.numbersOnField.forEach(numObj => {
            const color = this.colorMode === 'different' 
                ? (numObj.isCorrect ? '#00f' : '#f00')
                : '#00f';
            
            this.ctx.fillStyle = color;
            this.ctx.fillRect(
                numObj.pos.x * this.GRID_SIZE,
                numObj.pos.y * this.GRID_SIZE,
                this.GRID_SIZE,
                this.GRID_SIZE
            );
            
            // Draw number text
            this.ctx.fillStyle = '#000';
            this.ctx.font = '12px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(
                numObj.number.toString(),
                numObj.pos.x * this.GRID_SIZE + this.GRID_SIZE / 2,
                numObj.pos.y * this.GRID_SIZE + this.GRID_SIZE / 2
            );
        });
    }
    
    gameLoop() {
        this.updateGame();
        this.draw();
        setTimeout(() => this.gameLoop(), 200); // 5 FPS
    }
}

// Start the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MathSnakeGame();
});
