"""Print handoff & sprint focus at shell startup."""

import datetime
import pathlib
import textwrap

doc = pathlib.Path("documents/execution/dev_log.md")
last_entry = "Unknown"
try:
    text = doc.read_text()
    if "[" in text and "]" in text:
        last_entry = text.split("[")[-1].split("]")[0]
except Exception as e:
    last_entry = f"Error reading dev_log.md: {e}"

print(
    textwrap.dedent(f"""
🕒 {datetime.date.today()} | Last session: {last_entry}
Next task → see implementation_schedule.md
""")
)
