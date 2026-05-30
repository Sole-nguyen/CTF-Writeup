#!/usr/bin/env python3
"""
Auto-play Galactic Invaders and extract the flag
"""
import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("[*] Launching browser...")
        browser = await p.chromium.launch(headless=False)  # Set to False to see what's happening
        page = await browser.new_page()
        
        # Navigate to the game
        print("[*] Loading game...")
        await page.goto('http://127.0.0.1:8080/aliens.html')
        
        # Wait for game to initialize
        await page.wait_for_timeout(2000)
        
        print("[*] Injecting auto-win exploit...")
        
        # Inject the exploit script
        exploit_result = await page.evaluate('''
            () => {
                return new Promise((resolve) => {
                    console.log("=== AUTO WIN EXPLOIT STARTING ===");
                    
                    // Check if game variables are available
                    if (typeof score === 'undefined' || typeof previousScore === 'undefined') {
                        resolve({success: false, error: "Game variables not found"});
                        return;
                    }
                    
                    console.log("Initial score:", score);
                    console.log("Initial previousScore:", previousScore);
                    
                    let targetScore = 1000000;
                    let count = 0;
                    let resolved = false;
                    
                    const winInterval = setInterval(() => {
                        if (score >= targetScore) {
                            clearInterval(winInterval);
                            
                            if (!resolved) {
                                resolved = true;
                                console.log("=== REACHED 1 MILLION ===");
                                console.log("Final score:", score);
                                console.log("Final previousScore:", previousScore);
                                console.log("Anti-cheat check:", score > 999999 && score == (previousScore + 10));
                                
                                // Wait a bit for flag to display
                                setTimeout(() => {
                                    // Try to find flag in console or page
                                    const bodyText = document.body.innerText;
                                    const flag = bodyText.match(/flag\\{[^}]+\\}|FLAG\\{[^}]+\\}|jdh\\{[^}]+\\}/i);
                                    
                                    resolve({
                                        success: true,
                                        score: score,
                                        previousScore: previousScore,
                                        antiCheatPass: score > 999999 && score == (previousScore + 10),
                                        flag: flag ? flag[0] : "Flag not found in body",
                                        bodySnippet: bodyText.substring(0, 500)
                                    });
                                }, 2000);
                            }
                            return;
                        }
                        
                        // Critical: Set previousScore BEFORE incrementing score
                        previousScore = score;
                        score += 10;
                        count++;
                        
                        // Update HUD occasionally
                        if (count % 100 === 0) {
                            const hs = document.getElementById("hud-score");
                            if (hs) hs.innerText = String(score);
                        }
                        
                        // Progress logging
                        if (count % 10000 === 0) {
                            console.log(`Progress: ${score.toLocaleString()} / ${targetScore.toLocaleString()}`);
                        }
                    }, 0);
                    
                    // Timeout after 30 seconds
                    setTimeout(() => {
                        if (!resolved) {
                            resolved = true;
                            clearInterval(winInterval);
                            resolve({success: false, error: "Timeout", score: score});
                        }
                    }, 30000);
                });
            }
        ''')
        
        print(f"\n[*] Exploit result:")
        print(f"    Success: {exploit_result.get('success')}")
        print(f"    Score: {exploit_result.get('score')}")
        print(f"    Previous Score: {exploit_result.get('previousScore')}")
        print(f"    Anti-cheat passed: {exploit_result.get('antiCheatPass')}")
        
        if exploit_result.get('flag'):
            print(f"\n[+] FLAG FOUND: {exploit_result['flag']}")
        else:
            print(f"\n[-] Flag not found in body")
            print(f"    Body snippet: {exploit_result.get('bodySnippet', 'N/A')}")
        
        # Check console logs
        print("\n[*] Checking page content...")
        page_content = await page.content()
        
        # Look for flag patterns
        import re
        flag_matches = re.findall(r'(flag\{[^}]+\}|FLAG\{[^}]+\}|jdh\{[^}]+\}|JDH\{[^}]+\})', page_content, re.IGNORECASE)
        if flag_matches:
            print(f"[+] Flag patterns found in page: {flag_matches}")
        
        # Take a screenshot
        await page.screenshot(path='flag_screenshot.png')
        print("[*] Screenshot saved to flag_screenshot.png")
        
        # Wait a bit to see the result
        print("\n[*] Waiting 5 seconds to capture any delayed flag display...")
        await page.wait_for_timeout(5000)
        
        # Check again
        final_content = await page.content()
        final_matches = re.findall(r'(flag\{[^}]+\}|FLAG\{[^}]+\}|jdh\{[^}]+\}|JDH\{[^}]+\})', final_content, re.IGNORECASE)
        if final_matches:
            print(f"[+] Final flag check: {final_matches}")
        
        # Also check for any alerts or overlays
        await page.screenshot(path='flag_screenshot_final.png')
        print("[*] Final screenshot saved to flag_screenshot_final.png")
        
        print("\n[*] Keeping browser open for 10 seconds... Check for flag manually if needed.")
        await page.wait_for_timeout(10000)
        
        await browser.close()

if __name__ == "__main__":
    print("="*60)
    print("Galactic Invaders - Auto Flag Extractor")
    print("="*60)
    asyncio.run(main())
