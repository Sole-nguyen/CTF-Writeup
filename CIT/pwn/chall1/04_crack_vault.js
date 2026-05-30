const fs = require("fs");
const readline = require("readline");
const kdbxweb = require("kdbxweb");

const vaultPath = process.argv[2] || "vault.kdbx";
const wordlistPath = process.argv[3] || "common10k.txt";

const data = fs.readFileSync(vaultPath);
const ab = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);

async function run() {
  const rl = readline.createInterface({
    input: fs.createReadStream(wordlistPath),
    crlfDelay: Infinity,
  });

  let i = 0;
  for await (const line of rl) {
    const pw = line.trim();
    if (!pw) continue;
    i++;
    try {
      await kdbxweb.Kdbx.load(ab, new kdbxweb.Credentials(kdbxweb.ProtectedValue.fromString(pw)));
      console.log(`[+] FOUND_PASSWORD=${pw}`);
      return;
    } catch (_) {}
  }

  console.log("[-] Password not found in wordlist");
}

run();
