# cSpell: ignore hsnips
import os
import csv
from pprint import pprint


def line_parser(line: list[str]) -> dict[str, str | list[str]]:
    line = [x.strip() for x in line]
    if len(line) == 1 and line[0].startswith("#"):
        return {"comment": line[0]}
    body = line[0]
    name = line[0].lstrip("\\[").strip("]")
    trigger = line[1:]
    return {
        "trigger": trigger,
        "body": body,
        "name": name,
    }


def formatter(info: dict[str, str], indicator: str = "\\u0060") -> str:
    if "comment" in info:
        return info["comment"]
    if len(info["trigger"]) == 1:
        trigger = "`" + indicator + info["trigger"][0] + indicator + "`"
    else:
        trigger = "`" + indicator + f"({'|'.join(info['trigger'])})" + indicator + "`"
    return f"""snippet {trigger} "{info["name"]}" iA
{info["body"]}
endsnippet"""


if not os.path.exists("Wolfram.hsnips"):
    with open("Wolfram.hsnips", "w") as f:
        pass

with open("wolfram_snippets.csv", "r") as source, open("Wolfram.hsnips", "w") as dest:
    reader = csv.reader(source)
    # Skip the first two rows
    for _ in range(2):
        next(reader, None)
    for i, line in enumerate(reader):
        print("Processing line:", i)
        info = line_parser(line)
        dest.write(formatter(info) + "\n")
print("Processing complete")
