#!/bin/bash
# Teal HQ Job Scraper - Quick Setup Script
# For Mac M4 Pro + Sequoia 15.5

echo "🚀 Setting up Teal HQ Job Scraper..."

# Create directories
mkdir -p ../../output
mkdir -p ../../data

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install requests beautifulsoup4 lxml pandas pyyaml

# Make scripts executable
chmod +x teal_job_scraper.py
chmod +x teal_playwright_scraper.py
chmod +x pipeline_integrator.py
chmod +x mcp_processor.py

# Create sample David Shi scaffold format if not exists
if [ ! -f "../../data/david_shi_scaffold_format.csv" ]; then
    echo "📋 Creating sample scaffold format..."
    cat > ../../data/david_shi_scaffold_format.csv << 'EOF'
job_title,company,original_url,poster_name,linkedin,title,email,confidence_score,source,date_scraped,notes
"Senior Software Engineer - GenAI Infrastructure","TikTok","https://linkedin.com/jobs/view/123456","David Shi","https://linkedin.com/in/davidshi","Engineering Manager, GenAI Infrastructure","david.shi@tiktok.com",95,"manual_research","2024-06-24T10:30:00Z","Gold standard example - verified contact match"
EOF
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Usage options:"
echo "1. Browser console: Follow README.md instructions"
echo "2. Python guided: python3 teal_job_scraper.py"
echo "3. MCP automation: python3 teal_playwright_scraper.py"
echo "4. Full integration: python3 pipeline_integrator.py"
echo ""
echo "📁 Files ready in scripts/teal-integration/"