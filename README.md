# Website

My personal website built with [Quarto](https://quarto.org/), featuring projects, notes, and blog posts.

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) installed on your system
- Python 3.x
- Access to your Obsidian vault (for notes generation)

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd website
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the notes path (if needed):
   - Edit `publish_notes.py` and update the `VAULT_PATH` variable to point to your Obsidian vault location
   - Default path: `/Users/elainetsai/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tinkleberry`

## Running Locally

To preview the website locally:

```bash
quarto preview
```

This will start a local development server (typically at `http://localhost:4200`) where you can preview your changes in real-time.

To render the site without starting a server:

```bash
quarto render
```

The rendered website will be output to the `docs/` directory.

## Notes Generation

### Why Generate Notes?

The website includes a notes section that pulls content from your Obsidian vault. The `publish_notes.py` script:

- **Converts Obsidian wikilinks** (`[[Page Name]]`) to Markdown links
- **Adds Quarto frontmatter** (title, date, tags) to notes
- **Manages drafts** - new notes are automatically added to drafts
- **Filters published content** - only notes with `dg-publish: true` in their frontmatter are processed

### How to Generate Notes

1. **Mark notes for publishing** in Obsidian:
   - Add `dg-publish: true` to the frontmatter of any note you want to publish
   - Example:
     ```yaml
     ---
     dg-publish: true
     title: "My Note Title"
     tags: [tech, tutorial]
     ---
     ```

2. **Run the notes generation script**:
   ```bash
   python publish_notes.py
   ```

3. **Review the output**:
   - Published notes are copied to `notes/` directory
   - New notes are added to `notes/drafts/` as drafts
   - Existing notes in `notes/` are updated in place
   - The script will print how many notes were processed

4. **Review drafts**:
   - Check `notes/drafts/` for new notes
   - When ready to publish, move them from `notes/drafts/` to `notes/`
   - Or manually remove the `draft: true` frontmatter

### Notes Workflow

1. Write notes in Obsidian with `dg-publish: true`
2. Run `python publish_notes.py` to sync notes
3. Review new notes in `notes/drafts/`
4. Move approved notes from drafts to `notes/` or edit their frontmatter
5. Render/preview the site to see changes

## Deployment

This website is configured to deploy to GitHub Pages using the `docs/` directory as the output folder.

### Deploying to GitHub Pages

1. **Render the site**:
   ```bash
   quarto render
   ```

2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Update website"
   git push
   ```

3. **Configure GitHub Pages** (if not already done):
   - Go to your repository settings on GitHub
   - Navigate to Pages
   - Set source to "Deploy from a branch"
   - Select `main` (or your default branch) and `/docs` folder
   - Save

The site will be available at `https://<username>.github.io/<repository-name>/` after deployment.

## General Workflow

### Adding a New Blog Post/Project

1. Create a new `.qmd` file in the `posts/` directory
2. Add frontmatter with title, date, categories, etc.:
   ```yaml
   ---
   title: "My Post Title"
   date: "2024-01-15"
   categories: [tech, tutorial]
   ---
   ```
3. Write your content in Markdown
4. Preview locally with `quarto preview`
5. Render and deploy when ready

### Updating Notes

1. Edit notes in Obsidian
2. Run `python publish_notes.py` to sync changes
3. Review drafts if any new notes were added
4. Render and deploy

### Making Site-Wide Changes

1. Edit configuration in `_quarto.yml`
2. Edit styles in `styles.css`
3. Edit page files (`.qmd`) as needed
4. Preview with `quarto preview`
5. Render and deploy

## Project Structure

```
website/
├── _quarto.yml          # Quarto configuration
├── index.qmd            # Home page
├── about.qmd            # About page
├── projects.qmd         # Projects listing page
├── notes.qmd            # Notes listing page
├── posts/               # Blog posts and projects
│   └── drafts/          # Draft posts
├── notes/               # Published notes (generated)
│   └── drafts/          # Draft notes (generated)
├── docs/                # Rendered website output
├── styles.css           # Custom CSS
├── publish_notes.py     # Notes generation script
└── requirements.txt     # Python dependencies
```

## Troubleshooting

- **Notes not appearing**: Make sure `dg-publish: true` is in the note's frontmatter in Obsidian
- **Links broken**: The script converts Obsidian wikilinks, but complex link structures may need manual adjustment
- **Drafts not showing**: Drafts are hidden by default in Quarto. Remove `draft: true` from frontmatter to publish
- **Build errors**: Check that all required dependencies are installed and Quarto is up to date
