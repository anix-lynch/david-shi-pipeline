#!/usr/bin/env python3
"""
Teal HQ Job Scraper - David Shi Pipeline Integration
Extracts LinkedIn job URLs from Teal saved jobs via MCP automation
"""

import csv
import json
import os
import time
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# David Shi Scaffold Format Headers
SCAFFOLD_HEADERS = [
    'job_title', 'company', 'original_url', 'poster_name', 
    'linkedin', 'title', 'email', 'confidence_score',
    'source', 'date_scraped', 'notes'
]

class TealJobScraper:
    def __init__(self, output_path="output/teal_jobs_scaffold.csv"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(exist_ok=True)
        self.session = requests.Session()
        
        # Setup headers to look like real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
    def manual_extract_flow(self):
        """Guide user through manual extraction process"""
        print("🚀 Teal HQ Job Extraction - Manual Flow")
        print("=" * 50)
        
        print("\n📋 Step 1: Export your Teal jobs")
        print("1. Go to https://app.tealhq.com")
        print("2. Navigate to your Job Tracker")
        print("3. Look for Export/Download option (if available)")
        print("4. Or prepare to copy job data manually")
        
        input("\nPress Enter when ready to continue...")
        
        print("\n🔍 Step 2: Job URL extraction methods")
        print("Method A - Browser Console (Recommended):")
        print("Run this in your browser console on app.tealhq.com:")
        
        console_script = '''
// Teal Job URL Extractor
function extractTealJobs() {
    const jobs = [];
    
    // Try different selectors for job rows
    const selectors = [
        '[data-testid*="job"]',
        '.job-row',
        '[class*="job-item"]',
        'tr[role="row"]',
        '[class*="JobRow"]'
    ];
    
    let jobRows = [];
    for (let selector of selectors) {
        jobRows = document.querySelectorAll(selector);
        if (jobRows.length > 0) break;
    }
    
    console.log(`Found ${jobRows.length} job rows`);
    
    jobRows.forEach((row, index) => {
        try {
            // Extract job data from each row
            const titleEl = row.querySelector('[class*="title"], [class*="Title"], h2, h3, .job-title');
            const companyEl = row.querySelector('[class*="company"], [class*="Company"], .company-name');
            const linkEl = row.querySelector('a[href*="linkedin"], a[href*="indeed"], a[href*="glassdoor"], a');
            
            const job = {
                index: index + 1,
                title: titleEl?.textContent?.trim() || '',
                company: companyEl?.textContent?.trim() || '',
                url: linkEl?.href || '',
                extracted_at: new Date().toISOString()
            };
            
            if (job.title) jobs.push(job);
        } catch (e) {
            console.log(`Error extracting job ${index}:`, e);
        }
    });
    
    // Generate CSV output
    const csvHeader = 'job_title,company,original_url,poster_name,linkedin,title,email,confidence_score,source,date_scraped,notes';
    const csvRows = jobs.map(job => 
        `"${job.title}","${job.company}","${job.url}","","","","",0,"teal_hq","${job.extracted_at}","Extracted via browser console"`
    );
    
    const csv = [csvHeader, ...csvRows].join('\\n');
    
    console.log('\\n=== COPY THIS CSV DATA ===');
    console.log(csv);
    console.log('=== END CSV DATA ===\\n');
    
    return { jobs, csv };
}

// Run the extraction
extractTealJobs();
'''
        
        print(console_script)
        
        print("\nMethod B - Manual copy:")
        print("If console method doesn't work, manually copy each job's:")
        print("- Job Title")
        print("- Company Name") 
        print("- Original URL (from job details)")
        
        return self.process_manual_input()
    
    def process_manual_input(self):
        """Process manually extracted job data"""
        print("\n📝 Manual Job Entry")
        jobs = []
        
        while True:
            print(f"\n--- Job #{len(jobs) + 1} ---")
            title = input("Job Title (or 'done' to finish): ").strip()
            
            if title.lower() == 'done':
                break
                
            company = input("Company: ").strip()
            url = input("Original URL: ").strip()
            notes = input("Notes (optional): ").strip()
            
            job = {
                'title': title,
                'company': company,
                'url': url,
                'notes': notes,
                'extracted_at': datetime.now().isoformat()
            }
            
            jobs.append(job)
            print(f"✅ Added job {len(jobs)}")
            
            continue_adding = input("Add another job? (y/n): ").strip().lower()
            if continue_adding != 'y':
                break
        
        return jobs
    
    def csv_import_flow(self):
        """Import from CSV file if user has exported from Teal"""
        print("\n📁 CSV Import Flow")
        csv_path = input("Enter path to your Teal export CSV: ").strip()
        
        if not os.path.exists(csv_path):
            print(f"❌ File not found: {csv_path}")
            return []
            
        jobs = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Map Teal CSV columns to our format
                    job = {
                        'title': row.get('Job Title', row.get('title', '')),
                        'company': row.get('Company', row.get('company', '')),
                        'url': row.get('URL', row.get('url', row.get('link', ''))),
                        'notes': row.get('Notes', ''),
                        'extracted_at': datetime.now().isoformat()
                    }
                    jobs.append(job)
            
            print(f"✅ Imported {len(jobs)} jobs from CSV")
            
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            
        return jobs
    
    def save_to_scaffold(self, jobs):
        """Save jobs to David Shi scaffold format"""
        if not jobs:
            print("❌ No jobs to save")
            return
            
        with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=SCAFFOLD_HEADERS)
            writer.writeheader()
            
            for i, job in enumerate(jobs):
                scaffold_row = {
                    'job_title': job.get('title', ''),
                    'company': job.get('company', ''),
                    'original_url': job.get('url', ''),
                    'poster_name': '',  # To be enriched later
                    'linkedin': '',     # To be enriched later  
                    'title': '',        # To be enriched later
                    'email': '',        # To be enriched later
                    'confidence_score': 0,
                    'source': 'teal_hq',
                    'date_scraped': job.get('extracted_at', datetime.now().isoformat()),
                    'notes': job.get('notes', f"Job #{i+1} from Teal HQ extraction")
                }
                writer.writerow(scaffold_row)
                
        print(f"✅ Saved {len(jobs)} jobs to {self.output_path}")
        print(f"📁 File location: {self.output_path.absolute()}")
        
        # Show preview
        self.preview_results()
    
    def preview_results(self):
        """Show preview of saved data"""
        try:
            with open(self.output_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            print(f"\n📊 Preview of {self.output_path}:")
            print("=" * 60)
            for i, line in enumerate(lines[:6]):  # Header + 5 rows
                print(f"{i:2d}: {line.strip()}")
                
            if len(lines) > 6:
                print(f"... and {len(lines) - 6} more rows")
                
        except Exception as e:
            print(f"❌ Error reading preview: {e}")
    
    def run(self):
        """Main execution flow"""
        print("🔥 Teal HQ → David Shi Pipeline Scraper")
        print("=" * 50)
        
        print("\nSelect extraction method:")
        print("1. Manual extraction (guided)")
        print("2. Import from CSV export")
        print("3. Browser console method")
        
        choice = input("\nChoice (1-3): ").strip()
        
        jobs = []
        
        if choice == "1":
            jobs = self.manual_extract_flow()
        elif choice == "2":
            jobs = self.csv_import_flow()
        elif choice == "3":
            jobs = self.manual_extract_flow()  # Same flow, different instructions
        else:
            print("❌ Invalid choice")
            return
            
        if jobs:
            self.save_to_scaffold(jobs)
            print(f"\n🎯 Next steps:")
            print(f"1. Review the generated file: {self.output_path}")
            print(f"2. Run your David Shi enrichment pipeline")
            print(f"3. Use the enriched data for outreach")
        else:
            print("❌ No jobs extracted")

if __name__ == "__main__":
    scraper = TealJobScraper()
    scraper.run()