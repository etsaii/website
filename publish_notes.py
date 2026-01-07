import re
import pathlib
import frontmatter
from datetime import datetime

# This file is a script that copies over notes from Obsidian to be published.

# --- CONFIG ---
VAULT_PATH = pathlib.Path("/Users/elainetsai/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tinkleberry")
OUTPUT_PATH = pathlib.Path("./notes")
DRAFTS_PATH = OUTPUT_PATH / "_drafts"

# --- UTILITIES
# Compile regex pattern once for better performance
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

def convert_wikilinks(text: str) -> str:
    """Convert Obsidian wikilinks to Markdown links.
    
    Examples:
        [[Page Name]] -> [Page Name](Page-Name)
        [[Page Name|Display Text]] -> [Display Text](Page-Name)
    """
    def replace_wikilink(match: re.Match) -> str:
        """Replace a single wikilink match with a Markdown link."""
        link_target = match.group(1)
        display_text = match.group(2) or link_target
        url_path = link_target.replace(' ', '-')
        return f"[{display_text}]({url_path})"
    
    return WIKILINK_PATTERN.sub(replace_wikilink, text)

def ensure_quarto_frontmatter(post, src_path, is_draft=False):
    """Ensure each note has Quarto YAML frontmatter."""
    fm = post.metadata.copy() if post.metadata else {}

    #title
    if "title" not in fm or not fm["title"]:
        if post.content and post.content.strip():
            first_line = post.content.split("\n", 1)[0].strip()
            if first_line.startswith("#"):
                # Remove leading # and any following spaces, but preserve the rest
                fm["title"] = first_line.lstrip("#").lstrip()
            else:
                fm["title"] = src_path.stem
        else:
            fm["title"] = src_path.stem

    #date if missing (use file modification time)
    if "date" not in fm or not fm["date"]:
        mod_time = datetime.fromtimestamp(src_path.stat().st_mtime)
        fm["date"] = mod_time.strftime("%Y-%m-%d")

    # Convert tags to categories for Quarto compatibility
    if post.metadata and "tags" in post.metadata and post.metadata["tags"]:
        # Quarto uses "categories" instead of "tags"
        if "categories" not in fm:
            fm["categories"] = post.metadata["tags"]
        # Keep tags as well for backwards compatibility
        fm["tags"] = post.metadata["tags"]

    #mark as draft if it's a new file
    if is_draft:
        fm["draft"] = True
    
    return frontmatter.Post(post.content, **fm)

#--- MAIN FUNCTION ---
def publish_notes():
    """Convert public notes to be published on the website."""
    # Check if vault path exists
    if not VAULT_PATH.exists():
        print(f"❌ Error: Vault path does not exist: {VAULT_PATH}")
        print("Please update VAULT_PATH in publish_notes.py to point to your Obsidian vault.")
        return
    
    # Create output directories if they don't exist
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    DRAFTS_PATH.mkdir(parents=True, exist_ok=True)
    
    count = 0
    draft_count = 0

    # Process each note file
    for file in VAULT_PATH.rglob("*.md"):
        if not file.is_file():
            continue

        try:
            post = frontmatter.load(file)
        except Exception as e:
            print(f"⚠️  Error loading {file}: {e}")
            continue

        if not post.metadata or not post.metadata.get("dg-publish", False):
            continue

        # Convert links and ensure YAML frontmatter
        post.content = convert_wikilinks(post.content)
        
        # Check if this file already exists in either location
        dest_path = OUTPUT_PATH / file.stem
        dest_path = dest_path.with_suffix(".md")
        draft_path = DRAFTS_PATH / file.stem
        draft_path = draft_path.with_suffix(".md")
        
        # Determine if file is new and where it should go
        exists_in_main = dest_path.exists()
        exists_in_drafts = draft_path.exists()
        
        if exists_in_main:
            # File exists in main folder - update it there
            post = ensure_quarto_frontmatter(post, file, is_draft=False)
            final_dest_path = dest_path
            count += 1
        elif exists_in_drafts:
            # File exists in drafts - update it there (keep as draft)
            post = ensure_quarto_frontmatter(post, file, is_draft=True)
            final_dest_path = draft_path
            draft_count += 1
        else:
            # New file - add to drafts
            post = ensure_quarto_frontmatter(post, file, is_draft=True)
            final_dest_path = draft_path
            draft_count += 1
        
        final_dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        try:
            with open(final_dest_path, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))
        except Exception as e:
            print(f"⚠️  Error writing {final_dest_path}: {e}")
            continue
    
    print(f"✅ {count} notes published to {OUTPUT_PATH.resolve()}")
    if draft_count > 0:
        print(f"📝 {draft_count} new notes added to drafts in {DRAFTS_PATH.resolve()}")

if __name__ == "__main__":
    publish_notes()