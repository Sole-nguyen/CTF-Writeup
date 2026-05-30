// Simple test to verify the logic works
console.log("Testing anti-cheat logic after fix...\n");

let score = 0;
let previousScore = 0;

// Simulate killing aliens with FIXED code
for (let i = 0; i < 100000; i++) {
    // This is the FIXED order
    previousScore = score;  // Store old score first
    score += 10;            // Then increment
}

console.log(`Final score: ${score}`);
console.log(`Final previousScore: ${previousScore}`);
console.log(`Check: score > 999999 && score == (previousScore + 10)`);
console.log(`Result: ${score > 999999} && ${score == (previousScore + 10)}`);
console.log(`PASS: ${score > 999999 && score == (previousScore + 10)}`);
