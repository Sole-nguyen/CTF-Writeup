import sqlite3, struct, json

conn = sqlite3.connect("mystery_message_0.db3")
cur = conn.cursor()
topic_id = cur.execute(
    "SELECT id FROM topics WHERE name='/draw_commands'"
).fetchone()[0]

commands = []
for _, blob in cur.execute(
    "SELECT timestamp, data FROM messages WHERE topic_id=? ORDER BY timestamp",
    (topic_id,),
):
    length = struct.unpack("<I", blob[4:8])[0]  # skip CDR header
    s = blob[8:8+length].rstrip(b"\x00").decode("utf-8")
    commands.append(json.loads(s))