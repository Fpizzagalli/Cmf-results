import requests
from bs4 import BeautifulSoup
from datetime import datetime

def format_date(date_str):
    # Handle the hyphen case first
    if date_str == "-":
        return "" # Or None, depending on how your calendar expects missing dates

    # Try DD/MM/YYYY format first
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        # If that fails, try DD-MM-YYYY format
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            # If both fail, print a warning and return empty string
            print(f"Could not parse date: {date_str}. Returning empty string.")
            return ""

def get_financial_events():
    url = "https://www.cmfchile.cl/institucional/mercados/novedades_envio_fechas_eeff.php"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.cmfchile.cl/institucional/mercados/home.php"
    }

    print(f"Attempting to fetch data from: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    events = []

    if not tables:
        print("No tables found on the page.")

    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue
            
            row_data = [cell.get_text(strip=True) for cell in cells]
            
            # This print is useful for seeing raw row data
            # print(f"Raw row data: {row_data}") 

            if not row_data:
                continue

            # This check for "fondo" might need adjustment if row_data[0] is not always the first relevant text field
            if "fondo" in row_data[0].lower():
                continue

            try:
                # Based on your output:
                # row_data[0] seems to be 'nombreEmisor' (e.g., 'ABC S.A.')
                # row_data[1] seems to be 'rut' (e.g., '96874030-K')
                # row_data[2] seems to be 'fechaEnvioLimite' (e.g., '30/05/2025')
                # The 'tipoEEFF' seems to be missing or needs further investigation.

                if len(row_data) < 3:
                    print(f"Skipping row due to insufficient data (expected at least 3 cells for meaningful data): {row_data}")
                    continue

                # Extract all relevant date columns (indices 2, 3, 4, 5, 6)
                date_columns = [
                    (2, '1Q'),
                    (3, '2Q'),
                    (4, '3Q'),
                    (5, '4Q'),
                ]
                for idx, tipo in date_columns:
                    if len(row_data) > idx:
                        date_val = format_date(row_data[idx])
                        if date_val:  # Only add event if date is valid
                            event = {
                                "rut": row_data[1],
                                "nombreEmisor": row_data[0],
                                "tipoEEFF": tipo,
                                "fechaEnvioLimite": date_val,
                                "estado": "Vigente"
                            }
                            events.append(event)
            except IndexError:
                print(f"IndexError processing row: {row_data}. Likely incorrect indexing for expected columns.")
                continue
            except Exception as e:
                print(f"An unexpected error occurred while processing row {row_data}: {e}")
                continue

    return events

if __name__ == "__main__":
    print("Starting CMF Scraper...")
    all_events = get_financial_events()
    
    if all_events:
        print(f"\nSuccessfully scraped {len(all_events)} financial events:")
        for i, event in enumerate(all_events[:10]): # Print more to see better
            print(f"  Event {i+1}: {event}")
        if len(all_events) > 10:
            print("  (and more...)")
    else:
        print("\nNo financial events found or an error occurred during scraping.")