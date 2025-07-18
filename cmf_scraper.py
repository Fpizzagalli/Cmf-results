import requests
from bs4 import BeautifulSoup
from datetime import datetime

def format_date(date_str):
    if date_str == "-":
        return "" 
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
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
            if not row_data:
                continue
            if "fondo" in row_data[0].lower():
                continue
            try:
                if len(row_data) < 3:
                    print(f"Skipping row due to insufficient data (expected at least 3 cells for meaningful data): {row_data}")
                    continue
        # Extract only the valid columns
                date_columns = [
                    (2, '1Q'),
                    (3, '2Q'),
                    (4, '3Q'),
                    (5, '4Q'),
                ]
                for idx, tipo in date_columns:
                    if len(row_data) > idx:
                        date_val = format_date(row_data[idx])
                        if date_val:  
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
        for i, event in enumerate(all_events[:10]):
            print(f"  Event {i+1}: {event}")
        if len(all_events) > 10:
            print("  (and more...)")
    else:
        print("\nNo financial events found or an error occurred during scraping.")
