# Ocean Wildlife Revenge — Mystery Message

**Flag:** `RS{W4tch1ng_r0b0t_turtl3s}`

## Summary
The rosbag contains turtlesim draw commands. Replaying or rendering the `/draw_commands` topic reveals a two‑line message. Converting the drawing to an image makes the text legible.

## Steps
1. **Inspect the rosbag database**
   ```bash
   sqlite3 mystery_message_0.db3 ".tables"
   sqlite3 mystery_message_0.db3 "SELECT id,name,type FROM topics"
   ```
   The interesting topic is `/draw_commands` (`std_msgs/msg/String`).

2. **Decode and render the draw commands**
   The payload is a CDR string; the first 4 bytes are length, followed by a JSON blob. The JSON contains `pen` (on/off) and `teleport` commands that define line segments.

   ```python
   import sqlite3, struct, json
   from pathlib import Path

   db = Path("mystery_message_0.db3")
   conn = sqlite3.connect(db)
   cur = conn.cursor()
   (topic_id,) = cur.execute(
       "SELECT id FROM topics WHERE name='/draw_commands'"
   ).fetchone()

   rows = cur.execute(
       "SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp",
       (topic_id,),
   ).fetchall()

   commands = []
   for (data,) in rows:
       length = struct.unpack("<I", data[:4])[0]
       raw = data[4:4 + length].decode("utf-8", "ignore").replace("\x00", "")
       raw = raw[raw.index("{"):]  # strip leading pad
       commands.append(json.loads(raw))

   # Build SVG lines from pen-on teleport segments (scaling omitted here)
   ```

3. **Convert to an image and read the text**
   Render the SVG with ImageMagick, then zoom/crop to read the two lines.

   ```bash
   convert /tmp/revenge.svg -resize 300% /tmp/revenge.png
   ```

   The text in the image reads:
   ```
   RS{W4tch1ng_
   r0b0t_turtl3s}
   ```

## Flag
`RS{W4tch1ng_r0b0t_turtl3s}`
