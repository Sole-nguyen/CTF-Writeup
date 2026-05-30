const fs = require("fs");
const kdbxweb = require("kdbxweb");

const vaultPath = process.argv[2] || "vault.kdbx";
const password = process.argv[3] || "winter";

const data = fs.readFileSync(vaultPath);
const ab = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);

function walk(group) {
  for (const e of group.entries) {
    const titleField = e.fields.get("Title");
    const notesField = e.fields.get("Notes");
    const title = titleField && titleField.getText
      ? titleField.getText()
      : (titleField || "");
    const notes = notesField && notesField.getText
      ? notesField.getText()
      : (notesField || "");

    if (notes) {
      const m = notes.match(/CIT\{[^}\n]+\}/);
      if (m) {
        console.log(`[+] Entry=${title}`);
        console.log(`[+] flag1=${m[0]}`);
        process.exit(0);
      }
    }
  }

  for (const g of group.groups) walk(g);
}

(async () => {
  const db = await kdbxweb.Kdbx.load(
    ab,
    new kdbxweb.Credentials(kdbxweb.ProtectedValue.fromString(password))
  );
  walk(db.getDefaultGroup());
  console.log("[-] Flag not found");
})();
