# Teal HQ Job Scraper - Browser Console Method

## 🔥 Quick Extract (Recommended)

1. Go to `https://app.tealhq.com` and login
2. Navigate to your Job Tracker
3. Open browser console (F12 → Console)
4. Paste this script:

```javascript
// Teal Job Extractor - David Shi Pipeline Compatible
function extractTealJobs() {
    console.log('🔍 Scanning for Teal jobs...');
    
    const jobs = [];
    
    // Multiple selector strategies for different Teal layouts
    const jobSelectors = [
        '[data-testid*="job"]',
        '.job-row, .JobRow',
        '[class*="job-item"], [class*="JobItem"]',
        'tr[role="row"]',
        '[class*="JobListItem"]'
    ];
    
    let jobElements = [];
    
    // Try each selector until we find jobs
    for (let selector of jobSelectors) {
        jobElements = document.querySelectorAll(selector);
        console.log(`Trying ${selector}: found ${jobElements.length} elements`);
        if (jobElements.length > 0) break;
    }
    
    if (jobElements.length === 0) {
        console.log('❌ No job elements found. Try scrolling down or checking selectors.');
        return;
    }
    
    console.log(`✅ Found ${jobElements.length} job elements`);
    
    // Extract data from each job
    jobElements.forEach((element, index) => {
        try {
            // Multiple strategies to find job title
            const titleSelectors = [
                '[class*="title"], [class*="Title"]',
                'h1, h2, h3',
                '.job-title, .JobTitle',
                '[data-testid*="title"]'
            ];
            
            const companySelectors = [
                '[class*="company"], [class*="Company"]',
                '.company-name, .CompanyName',
                '[data-testid*="company"]'
            ];
            
            const linkSelectors = [
                'a[href*="linkedin"]',
                'a[href*="indeed"]',
                'a[href*="glassdoor"]',
                'a[href*="jobs"]',
                'a[href^="http"]'
            ];
            
            let title = '', company = '', url = '';
            
            // Find title
            for (let sel of titleSelectors) {
                const el = element.querySelector(sel);
                if (el && el.textContent.trim()) {
                    title = el.textContent.trim();
                    break;
                }
            }
            
            // Find company
            for (let sel of companySelectors) {
                const el = element.querySelector(sel);
                if (el && el.textContent.trim()) {
                    company = el.textContent.trim();
                    break;
                }
            }
            
            // Find original job URL
            for (let sel of linkSelectors) {
                const el = element.querySelector(sel);
                if (el && el.href) {
                    url = el.href;
                    break;
                }
            }
            
            const job = {
                index: index + 1,
                title: title,
                company: company,
                url: url,
                extractedAt: new Date().toISOString()
            };
            
            if (title || company) {
                jobs.push(job);
                console.log(`Job ${index + 1}: ${title} at ${company}`);
            }
            
        } catch (e) {
            console.log(`Error extracting job ${index + 1}:`, e);
        }
    });
    
    console.log(`\n📊 Extracted ${jobs.length} jobs total`);
    
    // Generate David Shi scaffold CSV
    const csvHeader = 'job_title,company,original_url,poster_name,linkedin,title,email,confidence_score,source,date_scraped,notes';
    
    const csvRows = jobs.map(job => {
        const cleanTitle = (job.title || '').replace(/"/g, '""');
        const cleanCompany = (job.company || '').replace(/"/g, '""');
        const cleanUrl = (job.url || '').replace(/"/g, '""');
        const timestamp = job.extractedAt;
        
        return `"${cleanTitle}","${cleanCompany}","${cleanUrl}","","","","",0,"teal_hq","${timestamp}","Browser extraction job ${job.index}"`;
    });
    
    const fullCsv = [csvHeader, ...csvRows].join('\n');
    
    console.log('\n🎯 DAVID SHI SCAFFOLD CSV:');
    console.log('================================');
    console.log(fullCsv);
    console.log('================================');
    
    // Copy to clipboard if possible
    if (navigator.clipboard) {
        navigator.clipboard.writeText(fullCsv).then(() => {
            console.log('✅ CSV copied to clipboard!');
        }).catch(() => {
            console.log('❌ Could not copy to clipboard');
        });
    }
    
    return { jobs, csv: fullCsv };
}

// Run the extraction
extractTealJobs();
```

5. Copy the CSV output
6. Save to `data/teal_jobs_scaffold.csv`

## 🐍 Python Script Alternative

Run the Python script for guided extraction:

```bash
cd scripts/teal-integration
python3 teal_job_scraper.py
```

## 🤖 MCP Playwright (Full Automation)

If you have Playwright MCP set up:

```bash
# In Claude Desktop/Code with Playwright MCP
python3 teal_playwright_scraper.py
```

## 🔗 Pipeline Integration

Merge with existing David Shi pipeline:

```bash
python3 pipeline_integrator.py
```

This will:
- Copy Teal jobs to `data/teal_jobs_scaffold.csv`
- Merge with existing RSS jobs
- Run enrichment pipeline
- Generate outreach targets

## 📊 Output Format

All methods produce David Shi scaffold format:
- `job_title, company, original_url`
- `poster_name, linkedin, title, email` (to be enriched)
- `confidence_score, source, date_scraped, notes`