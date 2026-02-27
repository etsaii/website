# Website

My personal website built with [Quarto](https://quarto.org/), featuring projects, notes, and blog posts.

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) installed on your system
- Python 3.x

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


## Project Structure

```
website/
├── _quarto.yml          # Quarto configuration
├── index.qmd            # Home page
├── about.qmd            # About page
├── projects.qmd         # Projects listing page
├── notes.qmd            # Notes listing page
├── posts/               # Blog posts and projects
│   └── _drafts/          # Draft posts
├── notes/               # Published notes
├── docs/                # Rendered website output
├── styles.css           # Custom CSS
├── publish_notes.py     # Notes generation script
└── requirements.txt     # Python dependencies
```
