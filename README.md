# David Shi Scaffold Format Pipeline

## 🧠 Purpose

This project standardizes job opportunity data into the **David Shi Scaffold Format** — a gold-standard row structure designed to identify, verify, and reach the true job decision-maker behind any listing.

## 📁 Folder Structure

- `data/` — Source CSVs in scaffold format
- `scripts/` — Python + shell tools to enrich, scrape, and convert data
- `output/` — Final scored + contact-enriched job rows
- `agents/` — Claude YAML task files (MCP-enabled)
- `docs/` — Format definitions, scoring rules, protocol flows

## ✅ Status

- First entry completed: **David Shi**, TikTok GenAI Infra team lead  
- Full scaffold format verified and saved to: `data/david_shi_scaffold_format.csv`

## 🚀 Coming Next

- RSS job ingestion into scaffold
- Teal job enrichment
- GitHub/Twitter/email contact enrichment
- Claude agent orchestration via MCP
