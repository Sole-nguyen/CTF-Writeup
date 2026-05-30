const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const querystring = require('querystring');
const path = require('path');
const crypto = require('crypto');
const cookieParser = require('cookie-parser');

const app = express();
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

const BACKEND = { host: 'backend', port: 5000 };

function generateSessionId() {
    return crypto.randomBytes(32).toString('hex');
}

app.use((req, res, next) => {
    if (!req.cookies.session_id) {
        const sessionId = generateSessionId();
        res.cookie('session_id', sessionId, { httpOnly: true, path: '/' });
        req.sessionId = sessionId;
    } else {
        req.sessionId = req.cookies.session_id;
    }
    next();
});

function sendPostRequest(host, port, path, payload, headers = {}, sessionId = '') {
    return new Promise((resolve, reject) => {
        const postData = typeof payload === 'object' ? querystring.stringify(payload) : payload;
        
        let cookieHeader = '';
        if (sessionId) {
            cookieHeader = `session_id=${sessionId}`;
        }
        
        const options = {
            host,
            port,
            path,
            method: 'POST',
            headers: Object.assign({
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            }, cookieHeader ? { 'Cookie': cookieHeader } : {}, headers)
        };
        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch {
                    resolve(data);
                }
            });
        });
        req.setTimeout(1000, () => {
            req.abort();
            reject(new Error("Request timed out"));
        });
        req.on('error', (e) => reject(e));
        req.write(postData);
        req.end();
    });
}

app.use((req, res, next) => {
    const originalJson = res.json;
    
    res.json = function(data) {
        if (req.path === '/documents') {
            const responseStr = JSON.stringify(data);
            if (responseStr.includes('flag_2.txt')) {
                return res.status(403).json({
                    error: "Access denied - forbidden content detected"
                });
            }
        }
        return originalJson.call(this, data);
    };
    
    if (req.path === '/documents' && req.method === 'POST') {
        const requestStr = JSON.stringify(req.body);
        if (requestStr.includes('flag_2.txt')) {
            return res.status(403).json({
                error: "Access denied - forbidden content detected"
            });
        }
    }
    
    next();
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        const response = await sendPostRequest(BACKEND.host, BACKEND.port, '/auth/login', {username, password}, {}, req.sessionId);
        res.json(response);
    } catch (err) {
        res.status(500).json({ error: 'Login failed', details: err.message });
    }
});

app.post('/debug', async (req, res) => {
    const { data, headers, access_token } = req.body; 
    if (!access_token) {
        return res.status(401).json({ error: 'Missing access_token' });
    }
    try {
        let requestHeaders = {};
        if (headers) {
            try {
                requestHeaders = JSON.parse(headers);
            } catch (e) {
                return res.status(400).json({ error: 'Invalid headers format. Must be a valid JSON string.', details: e.message });
            }
        }
        const finalHeaders = {
            Authorization: `Bearer ${access_token}`,
            ...requestHeaders
        };
        
        const response = await sendPostRequest(BACKEND.host, BACKEND.port, '/process/debug', data, finalHeaders, req.sessionId);
        res.json(response);
    } catch (err) {
        res.status(500).json({ error: 'Debugging failed', details: err.message });
    }
});

app.post('/documents', async (req, res) => {
    try {
        const { file_name, access_token } = req.body;
        if (!access_token) {
            return res.status(401).json({ error: 'Missing access_token' });
        }
        const response = await sendPostRequest(BACKEND.host, BACKEND.port, '/process/documents', { file_name }, { 'Authorization': `Bearer ${access_token}` }, req.sessionId);
        res.json(response);
    } catch (err) {
        res.status(500).json({ details: 'Invalid file' });
    }
});

const PORT = 4000;  
app.listen(PORT, () => console.log(`Front-end running at http://localhost:${PORT}`));
