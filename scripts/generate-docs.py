"""Generate the code reference pages and navigation."""

from pathlib import Path
import mkdocs_gen_files

# Set files to exclude from the docs
excluded_files = [
    "__init__",
    "_client_sdk_version",
    "handler/__init__",
    "handler/api_resources",
    "handler/http_client",
    "models/__init__",
    "resources/__init__",
]

# Prepare Navigation
nav = mkdocs_gen_files.Nav()

# Traverse through SDK source files to generate markdown docs for them
for path in sorted(Path("nylas").rglob("*.py")):
    # Calculate paths
    module_path = path.relative_to("nylas").with_suffix("")
    doc_path = path.relative_to("nylas").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    # Skip excluded files
    if str(module_path) in excluded_files:
        continue

    # Add file to navigation
    parts = tuple(module_path.parts)
    nav[parts] = doc_path.as_posix()

    # Generate markdown docs
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

# Write navigation to SUMMARY.md
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
