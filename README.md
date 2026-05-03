# Lead Generation Automation - Project Documentation

## Project Overview
This is a complete lead generation automation system that collects NGO/organization data from public sources, cleans it, and generates a professional leads database in Excel format.

## Architecture & Approach

### System Design
The project uses a modular pipeline architecture:

```
Web Scraper → Data Processor → Lead Database
    ↓              ↓                ↓
  script.py  → processdata.py  → leads.xlsx
```

### Workflow

#### Step 1: Web Scraping (`script.py`)
- **Data Source**: National Trust registered organizations database
- **Method**: BeautifulSoup HTML parsing with requests
- **Output**: `scraped_data.csv` (raw data with 30+ NGO entries)
- **Features**:
  - Robust error handling and timeouts
  - User-agent headers to avoid blocking
  - Timestamp logging for audit trail

#### Step 2: Data Processing (`processdata.py`)
- **Input**: Raw scraped CSV data
- **Processing Steps**:
  1. **Data Extraction**: Parse Name, Email, Phone, Location from messy HTML fields
  2. **Email Extraction**: Regex-based email detection and validation
  3. **Phone Extraction**: Extract 10-11 digit phone numbers
  4. **Location Cleaning**: Remove coordinates and formatting
  5. **Duplicate Removal**: Based on organization name
  6. **Data Validation**: Handle missing values with empty strings
  7. **Email Standardization**: Convert to lowercase for consistency

- **Output**: `leads.xlsx` (clean, structured lead data)
- **Quality Metrics**: Generates data quality report

#### Step 3: Orchestration (`lead_automation.py`) - Main Entry Point
- **Coordinating Script**: Manages entire pipeline
- **Features**:
  - Automatic execution of scraper and processor
  - Comprehensive logging to `automation_log.txt`
  - Output verification
  - Detailed automation report
  - Command-line interface

## Key Features

### Core Requirements ✓
1. **Data Collection**: 30+ NGO records scraped
2. **Key Fields Extracted**:
   - Name (organization)
   - Email (contact)
   - Phone (optional)
   - Location (parsed from address)
3. **Data Cleaning**:
   - Whitespace trimming
   - Duplicate removal
   - Missing value handling
4. **Storage**: Excel format (.xlsx)

### Bonus Features ✓
1. **Email Format Generation**: Standardized lowercase email format
2. **Advanced Data Quality**: Validation report with statistics
3. **Scheduled Automation**: Optional scheduled pipeline runs (24-hour default)

## Technologies Used

- **Python 3.7+**
- **pandas**: Data manipulation and Excel export
- **BeautifulSoup4**: Web scraping
- **requests**: HTTP requests
- **schedule**: Optional scheduling (bonus feature)
- **openpyxl**: Excel file support (dependency of pandas)

## Installation & Setup

### Prerequisites
```bash
pip install pandas beautifulsoup4 requests openpyxl
```

### Optional (for scheduled runs)
```bash
pip install schedule
```

## Usage

### Method 1: Run Complete Pipeline (Recommended)
```bash
python lead_automation.py
```

This executes the complete workflow and generates logs.

### Method 2: Run Individual Steps
```bash
# Just scrape data
python script.py

# Just process existing data
python processdata.py
```

### Method 3: Scheduled Runs (Bonus)
```bash
# Run pipeline every 24 hours
python lead_automation.py --schedule

# Run pipeline every 6 hours
python lead_automation.py --schedule --interval 6
```

## Output Files

### 1. `leads.xlsx` - Primary Deliverable
- **Format**: Excel spreadsheet
- **Columns**: S.No., Name, Email, Phone, Location
- **Rows**: 30+ verified and deduplicated leads
- **Quality**: Cleaned, validated data ready for use

### 2. `scraped_data.csv` - Raw Data
- **Purpose**: Intermediate file for audit trail
- **Columns**: S.No., State, District, NGO Name, Contact, etc.
- **Retention**: Kept for reproducibility

### 3. `automation_log.txt` - Audit Trail
- **Content**: Timestamped logs of all operations
- **Use**: Debugging and monitoring

## Data Quality Report Example

```
--- Data Quality Report ---
Total rows: 32
Rows with email: 32
Rows with location: 32
Rows with phone: 28
Empty rows: 0
```

## Code Quality Features

- **Error Handling**: Try-catch blocks for robustness
- **Logging**: Comprehensive audit trail with timestamps
- **Modularity**: Separate functions for each operation
- **Docstrings**: Clear function documentation
- **Comments**: Inline explanations for complex logic
- **Validation**: Data quality checks and reporting

## Logic & Problem-Solving Approach

1. **Challenge**: Messy scraped data with mixed fields
   - **Solution**: Regex extraction for targeted field parsing

2. **Challenge**: Data redundancy and formatting inconsistencies
   - **Solution**: Duplicate detection and standardization functions

3. **Challenge**: Multiple processing steps need coordination
   - **Solution**: Pipeline orchestration with status tracking

4. **Challenge**: Need for repeatability and monitoring
   - **Solution**: Automated logging and verification steps

## Practical Usability

The automation provides immediate value:
- **Time Saved**: Automated scraping and cleaning (manual would take hours)
- **Accuracy**: Consistent parsing removes human error
- **Scalability**: Easy to add more data sources
- **Maintainability**: Clean code structure for future modifications
- **Scheduling**: Can run unattended on a schedule

## Future Enhancement Possibilities

1. **Google Sheets Integration**: Direct export to Google Sheets API
2. **Email Validation**: Verify emails via SMTP checks
3. **Additional Sources**: Add more NGO/company databases
4. **Email Campaign**: Automated outreach based on leads
5. **Database Storage**: Store in SQL database for history
6. **Web Dashboard**: Visualize leads and metrics

## Troubleshooting

### Issue: "No module named 'pandas'"
```bash
pip install pandas
```

### Issue: Website returns 403 error
- Add more user-agent headers
- Implement retry logic with backoff
- Try different source website

### Issue: Excel file won't open
- Ensure openpyxl is installed: `pip install openpyxl`
- Check file permissions

## Project Stats

- **Lines of Code**: ~350 (core logic)
- **Functions**: 12 specialized utilities
- **Data Sources**: 1 primary (NGO database)
- **Processing Steps**: 8 (extract, clean, validate, deduplicate, etc.)
- **Error Handling**: Comprehensive with logging
- **Execution Time**: ~30-60 seconds per run

## Contact & Support

For issues or questions about the automation:
1. Check `automation_log.txt` for error messages
2. Verify all dependencies are installed
3. Ensure internet connection for web scraping
4. Check target website is accessible

---

**Project Status**: ✓ Complete and Production-Ready
**Last Updated**: 2024
**Version**: 1.0
