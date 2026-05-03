
"""
Lead Generation Data Processing Pipeline
Processes scraped NGO data, cleans it, and generates leads
"""
import pandas as pd
import re
import sys


def extract_email(text):
    """Extract email from text using regex"""
    if not isinstance(text, str):
        return ""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""


def extract_phone(text):
    """Extract phone number from text"""
    if not isinstance(text, str):
        return ""
    phone_pattern = r'\d{10}|\d{9,11}'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else ""


def clean_name(text):
    """Clean organization name"""
    if not isinstance(text, str):
        return ""
    # Remove extra whitespace and line breaks
    cleaned = re.sub(r'\s+', ' ', text.strip())
    # Remove duplicate org name patterns
    parts = cleaned.split()
    if len(parts) > 0:
        return parts[0] + ' ' + ' '.join(dict.fromkeys(parts[1:]))
    return cleaned


def clean_location(text):
    """Extract location from text"""
    if not isinstance(text, str):
        return ""
    # Remove coordinates in format "- | -"
    text = re.sub(r'-\s*\|\s*-', '', text)
    # Remove postal codes at end and extra spaces
    text = re.sub(r'\s*-\s*\d{6}\s*$', '', text)
    return text.strip()


def generate_email_format(email):
    """Generate standardized email format"""
    if not email:
        return ""
    return email.lower().strip()


def remove_duplicates(df):
    """Remove duplicate entries based on name and email"""
    initial_count = len(df)
    # Remove rows with duplicate names/emails
    df = df.drop_duplicates(subset=['Name'], keep='first')
    removed = initial_count - len(df)
    print(f"Removed {removed} duplicate entries")
    return df


def validate_data(df):
    """Validate data quality"""
    print("\n--- Data Quality Report ---")
    print(f"Total rows: {len(df)}")
    print(f"Rows with email: {df['Email'].notna().sum()}")
    print(f"Rows with location: {df['Location'].notna().sum()}")
    print(f"Rows with phone: {df['Phone'].notna().sum()}")
    print(f"Empty rows: {df.isna().any(axis=1).sum()}")


def process_data():
    """Main processing pipeline"""
    try:
        print("Starting data processing...")
        
        # Read the scraped data
        df = pd.read_csv('scraped_data.csv')
        print(f"Loaded {len(df)} rows from scraped_data.csv")
        
        # Extract key fields from messy data
        df['Name'] = df['NGO Name'].apply(clean_name)
        df['Email'] = df['Contact'].apply(extract_email)
        df['Phone'] = df['Contact'].apply(extract_phone)
        df['Location'] = df['NGO Name'].apply(clean_location)
        
        # Select required columns
        leads_df = df[['S.No.', 'Name', 'Email', 'Phone', 'Location']].copy()
        
        # Data cleaning
        print("Cleaning data...")
        # Strip whitespace from all string columns
        leads_df = leads_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Remove rows where Name is empty
        leads_df = leads_df[leads_df['Name'].notna() & (leads_df['Name'] != '')]
        
        # Remove duplicates
        leads_df = remove_duplicates(leads_df)
        
        # Fill remaining NaN values with empty strings
        leads_df = leads_df.fillna('')
        
        # Reset index
        leads_df = leads_df.reset_index(drop=True)
        
        # Format emails
        leads_df['Email'] = leads_df['Email'].apply(generate_email_format)
        
        # Validate and report
        validate_data(leads_df)
        
        # Save to Excel
        leads_df.to_excel('leads.xlsx', index=False)
        print("\n[OK] Data cleaned and saved to leads.xlsx")
        print(f"[OK] Total leads generated: {len(leads_df)}")
        
        return leads_df
        
    except Exception as e:
        print(f"Error processing data: {str(e)}", file=sys.stderr)
        raise


if __name__ == "__main__":
    process_data()
