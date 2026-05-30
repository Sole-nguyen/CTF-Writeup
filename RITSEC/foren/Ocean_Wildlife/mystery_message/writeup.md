# Mystery Message (Ocean Wildlife)

The `mystery_message_0.db3` file is a ROS 2 bag (SQLite). The hint about sea creatures points to a turtlesim drawing stored in `/draw_commands` (`std_msgs/String`).

Each message payload is CDR-encoded: 4-byte encapsulation header, then a little‑endian `uint32` length, then the JSON string. Decoding those strings yields commands like `{"cmd":"pen",...}` and `{"cmd":"teleport",...}`. Replaying them as turtle movements (draw a line on each teleport when the pen is on) produces the hidden text. Flipping vertically makes it readable.

**Flag:** `RS{f0ll0w_th3_5ea_Turtl3s}`

## Minimal extraction script

```python
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
```
