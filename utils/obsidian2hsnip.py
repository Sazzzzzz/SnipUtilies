import re
from typing import Any


# cSpell:words hsnips


class Hsnips2Obsidian:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.parse_hsnips()

    def _global_processor(self, global_str: str) -> str:
        return global_str.removeprefix("global\n").removesuffix("endglobal\n")

    def snippet_processor(self, snippet: str) -> dict[str, Any]:
        """Process a snippet string and extract its components."""

        data = {"priority": 0, "trigger": "", "description": "", "mode": "", "body": ""}
        lines = snippet.splitlines()

        line_index = 0

        # Check if the snippet starts with a priority declaration
        if lines[line_index].startswith("priority"):
            priority_match = re.match(r"^priority\s+(\d+)$", lines[line_index])
            if priority_match:
                data["priority"] = int(priority_match.group(1))
                line_index += 1

        # Process the snippet declaration line
        if line_index < len(lines) and lines[line_index].startswith("snippet"):
            snippet_match = re.match(
                r'^snippet\s+(\S+)\s+"([^"]+)"\s+(\S+)$', lines[line_index]
            )
            if snippet_match:
                data["trigger"] = snippet_match.group(1)
                data["description"] = snippet_match.group(2)
                data["mode"] = snippet_match.group(3)
                line_index += 1

        # Collect the body content (everything between snippet declaration and endsnippet)
        body_lines = []
        while line_index < len(lines) and not lines[line_index].strip() == "endsnippet":
            body_lines.append(lines[line_index])
            line_index += 1

        # Join the body lines
        data["replacement"] = "\n".join(body_lines)

        return data

    def parse_hsnips(self) -> dict[str, Any]:
        data: dict[str, Any] = {"global": "", "snippets": []}
        global_content = ""
        snippet_content = ""
        with open(self.file_path, "r") as file:
            for line in file:
                if global_content:
                    global_content += line
                    if line.strip() == "endglobal":
                        global_data = self._global_processor(global_content)
                        data["global"] += global_data + "\n"
                        global_content = ""
                    continue
                if snippet_content:
                    snippet_content += line
                    if line.strip() == "endsnippet":
                        snippet_data = self.snippet_processor(snippet_content)
                        data["snippets"].append(snippet_data)
                        snippet_content = ""
                    continue

                if line.startswith("#") or re.match(r"^==.+==", line):
                    continue
                elif line.strip().startswith("global"):
                    global_content += "global" + "\n"
                elif line.strip().startswith(("snippet", "priority")):
                    snippet_content += line + "\n"
        return data

    # There is information loss between conversion of snippets,
    # see https://github.com/artisticat1/obsidian-latex-suite?tab=readme-ov-file#snippets
    # for more details.

    def syntax_conversion(self) -> None:
        """Convert a hsnips snippet to a obsidian-compatible format."""
        #! Two platforms do not map their snippets exactly, there WILL be information loss.
        # Tag mapping
        tags = set(self.data["mode"])
        tags.discard("i")
        tags.discard("b")
        self.data["tags"] = "".join(tags)
        # Trigger Conversion
        if re.match(r"``.*``", self.data["trigger"]):
            raise ValueError(
                f"Error Processing {self.data['description']}, can not process snippet body with js functions."
            )
        if match := re.fullmatch(r"`(.*)`", self.data["trigger"]):
            self.data["trigger"] = "\\" + match.group(1) + "\\"
        return None

    def write(self, output_path: str) -> None:
        """Write the processed data to a file."""
        with open(output_path, "wt") as f:
            f.write("[\n")
            for snippet in self.data["snippets"]:
                f.write(
                    f"trigger: \"{snippet['trigger']}\", replacement: \"{snippet['description']}\" options: {snippet['mode']}\n"
                )
                f.write(snippet["replacement"] + "\n")
                f.write("endsnippet\n")
            f.write("]\n")


# 	{trigger: "@l", replacement: "\\lambda", options: "mA"},
# Example usage
if __name__ == "__main__":
    result = parse_hsnips("LaTeX.hsnips")
    print(f"Global section: {len(result['global'])} characters")
    print(f"Found {len(result['snippets'])} snippets")
    print(result["global"])

    # Print a sample snippet
    if result["snippets"]:
        sample = result["snippets"][78]
        print("\nSample snippet:")
        print(f"  Priority: {sample['priority']}")
        print(f"  Trigger: {sample['trigger']}")
        print(f"  Description: {sample['description']}")
        print(f"  Mode: {sample['mode']}")
        print(f"  Body: {sample['replacement']}")
