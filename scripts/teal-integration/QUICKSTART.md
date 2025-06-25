# 🔥 Teal HQ → David Shi Pipeline Scraper

**Status: READY TO USE**  
**Location: `scripts/teal-integration/`**

## ⚡ Quick Start (Choose Your Method)

### 🏆 Method 1: Browser Console (2 mins - RECOMMENDED)

1. Go to `https://app.tealhq.com` → Login → Job Tracker
2. Press `F12` → Console tab
3. Paste the extraction script from `README.md`
4. Copy CSV output → Save to `../../data/teal_jobs_scaffold.csv`

### 🐍 Method 2: Python Guided (5 mins)

```bash
cd scripts/teal-integration
python3 teal_job_scraper.py
```

### 🤖 Method 3: MCP Automation (Advanced)

```bash
# Requires Playwright MCP
python3 teal_playwright_scraper.py
```

### 🔗 Method 4: Full Pipeline Integration

```bash
# Integrates with David Shi pipeline
python3 pipeline_integrator.py
```

## 📁 File Structure

```
scripts/teal-integration/
├── teal_job_scraper.py      # Main extraction script
├── teal_playwright_scraper.py # MCP automation
├── pipeline_integrator.py   # David Shi integration
├── mcp_processor.py         # Advanced MCP features
├── README.md               # Browser console guide
├── setup.sh               # Dependencies installer
└── QUICKSTART.md          # This file
```

## 🎯 Output Format

All methods produce David Shi scaffold format:
- `job_title, company, original_url`
- `poster_name, linkedin, title, email` (to be enriched)
- `confidence_score, source, date_scraped, notes`

## 🔧 Mac M4 Pro CLI Commands

```bash
# Quick setup
cd scripts/teal-integration && ./setup.sh

# Run extraction
python3 teal_job_scraper.py

# Integrate with pipeline
python3 pipeline_integrator.py
```

## 🧠 MCP Integration Features

- **Memory MCP**: Store job entities for enrichment
- **GitHub MCP**: Auto-commit results to pipeline
- **Airtable MCP**: Track jobs in database
- **Web Search MCP**: Enrich missing contact data
- **Filesystem MCP**: Handle CSV operations

## ⚡ Next Steps

1. **Extract jobs** using preferred method
2. **Review** `data/teal_jobs_scaffold.csv`
3. **Run enrichment** via David Shi pipeline
4. **Scale outreach** with confidence scores

**Ready to go! Pick your extraction method and start scaling your job outreach.**