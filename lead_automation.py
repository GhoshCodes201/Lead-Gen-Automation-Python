"""
Lead Generation Automation Pipeline
Main orchestration script for the entire lead collection and processing workflow
Features:
- Web scraping from NGO database
- Data cleaning and validation
- Duplicate removal
- Email standardization
- Optional scheduled runs
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
import json


class LeadAutomationPipeline:
    """Orchestrates the lead generation workflow"""
    
    def __init__(self):
        self.workspace_dir = Path(__file__).parent
        self.log_file = self.workspace_dir / "automation_log.txt"
        
    def log(self, message):
        """Log messages to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    
    def run_scraper(self):
        """Execute web scraper"""
        self.log("=" * 60)
        self.log("STEP 1: Starting Web Scraper")
        self.log("=" * 60)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.workspace_dir / "script.py")],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log(result.stdout)
                self.log("✓ Scraping completed successfully")
                return True
            else:
                self.log(f"✗ Scraping failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"✗ Error during scraping: {str(e)}")
            return False
    
    def run_processor(self):
        """Execute data processor"""
        self.log("=" * 60)
        self.log("STEP 2: Starting Data Processing")
        self.log("=" * 60)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.workspace_dir / "processdata.py")],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log(result.stdout)
                self.log("✓ Processing completed successfully")
                return True
            else:
                self.log(f"✗ Processing failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"✗ Error during processing: {str(e)}")
            return False
    
    def verify_outputs(self):
        """Verify output files exist"""
        self.log("=" * 60)
        self.log("STEP 3: Verifying Output Files")
        self.log("=" * 60)
        
        files_to_check = [
            ("scraped_data.csv", "Raw scraped data"),
            ("leads.xlsx", "Processed leads file")
        ]
        
        all_exist = True
        for filename, description in files_to_check:
            filepath = self.workspace_dir / filename
            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024 * 1024)
                self.log(f"[OK] {filename} ({description}) - {size_mb:.2f} MB")
            else:
                self.log(f"[FAIL] {filename} ({description}) - NOT FOUND")
                all_exist = False
        
        return all_exist
    
    def generate_report(self):
        """Generate automation report"""
        self.log("=" * 60)
        self.log("AUTOMATION REPORT")
        self.log("=" * 60)
        
        try:
            import pandas as pd
            
            # Read the final leads file
            if (self.workspace_dir / "leads.xlsx").exists():
                df = pd.read_excel(self.workspace_dir / "leads.xlsx")
                
                self.log(f"\nFinal Statistics:")
                self.log(f"  Total Leads: {len(df)}")
                self.log(f"  Records with Email: {df['Email'].notna().sum()}")
                self.log(f"  Records with Phone: {df['Phone'].notna().sum()}")
                self.log(f"  Records with Location: {df['Location'].notna().sum()}")
                
                # Email domain stats
                if 'Email' in df.columns and df['Email'].notna().sum() > 0:
                    domains = df['Email'].str.extract(r'@(.+)$')
                    self.log(f"\n  Top Email Domains:")
                    for domain, count in domains[0].value_counts().head(5).items():
                        self.log(f"    - {domain}: {count}")
                
        except Exception as e:
            self.log(f"Could not generate detailed report: {str(e)}")
    
    def run_pipeline(self):
        """Execute the complete pipeline"""
        self.log("\n")
        self.log("╔" + "=" * 58 + "╗")
        self.log("║  LEAD GENERATION AUTOMATION PIPELINE - STARTED           ║")
        self.log("╚" + "=" * 58 + "╝")
        
        # Run pipeline steps
        if not self.run_scraper():
            self.log("✗ Pipeline failed at scraping stage")
            return False
        
        if not self.run_processor():
            self.log("✗ Pipeline failed at processing stage")
            return False
        
        if not self.verify_outputs():
            self.log("✗ Pipeline failed at verification stage")
            return False
        
        # Generate report
        self.generate_report()
        
        self.log("\n")
        self.log("╔" + "=" * 58 + "╗")
        self.log("║  LEAD GENERATION AUTOMATION PIPELINE - COMPLETED [OK] ║")
        self.log("╚" + "=" * 58 + "╝")
        
        return True


def schedule_pipeline(interval_hours=24):
    """
    BONUS FEATURE: Schedule pipeline to run at regular intervals
    
    Args:
        interval_hours (int): Hours between runs (default: 24)
    """
    try:
        import schedule
        import time
        
        pipeline = LeadAutomationPipeline()
        
        def job():
            pipeline.run_pipeline()
        
        schedule.every(interval_hours).hours.do(job)
        
        print(f"Scheduler started - Pipeline will run every {interval_hours} hours")
        print("Press Ctrl+C to stop")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except ImportError:
        print("Schedule library not installed. Install with: pip install schedule")
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Lead Generation Automation Pipeline")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run pipeline on a schedule (requires 'schedule' library)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=24,
        help="Interval in hours for scheduled runs (default: 24)"
    )
    
    args = parser.parse_args()
    
    if args.schedule:
        schedule_pipeline(args.interval)
    else:
        pipeline = LeadAutomationPipeline()
        success = pipeline.run_pipeline()
        sys.exit(0 if success else 1)
