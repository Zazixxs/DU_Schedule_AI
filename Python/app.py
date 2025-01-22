from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import datetime
import locale


def getSchedule():
    url = "https://cloud.timeedit.net/hda/web/public/s/s.html?tab=3&object=person.stud.h22carja&type=Alla&object=courseOccasion.H3J6K&type=Alla&object=courseOccasion.H3KAY&type=Alla&object=courseOccasion.V3KPR&type=Alla&object=courseOccasion.V3KPS&type=Alla&object=programmeOccasion.H3BCW&type=Alla&p=6.months"
    response = requests.get(url)

    if response.status_code != 200:
        return "fail"

    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    current_date = None  # Initialize to handle rows without a preceding date row

    for tr in soup.find_all('tr'):
        # Check if the row is a date row
        date_td = tr.find('td', class_='headline t') or tr.find('td', class_='headline t dateIsToday')
        if date_td:
            current_date = date_td.text.strip()
            # Remove any week information (e.g., ' v 5') from the date
            current_date = current_date.split(' v ')[0]
            continue  # Skip processing this row further

        # Process event rows
        if 'clickable2' in tr.get('class', []):
            time_cell = tr.find('td', class_='time')
            if time_cell:
                event_data = {
                    'datum': current_date if current_date else "Unknown Date",
                    'tid': time_cell.text.strip(),
                    'koder': tr.find('td', class_='column0').text.strip(),
                    'namn': tr.find('td', class_='column1').text.strip(),
                    'typ': tr.find_all('td', class_='column0')[2].text.strip(),
                    'ledare': tr.find('td', class_='column1', id=None).text.strip(),  # Subsequent column1
                    'plats': tr.find_all('td', class_='column0')[-1].text.strip(),
                }
                events.append(event_data)
                #print(f"Date: {event_data['datum']}, Time: {event_data['tid']}", flush=True)

    return events

def get_classes():
    url = "https://cloud.timeedit.net/hda/web/public/s/s.html?tab=3&object=person.stud.h22carja&type=Alla&object=courseOccasion.H3J6K&type=Alla&object=courseOccasion.H3KAY&type=Alla&object=courseOccasion.V3KPR&type=Alla&object=courseOccasion.V3KPS&type=Alla&object=programmeOccasion.H3BCW&type=Alla&p=6.months"
    response = requests.get(url)

    if response.status_code != 200:
        return "fail"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate today's date row
    date_row = soup.find('td', class_='headline t dateIsToday')
    if not date_row:
        return []  # No data for today

    # Initialize list for today's classes
    classes_today = []

    # Traverse sibling rows after today's date row
    for tr in date_row.find_parent('tr').find_next_siblings():
        if 'clickable2' in tr.get('class', []):  # Class rows have 'clickable2' class
            # Extract data from columns
            event_data = {
                'Tid': tr.find('td', class_='time').text.strip(),
                'Programtillfälle': tr.find_all('td', class_='column0')[0].text.strip(),
                'Kurskod': tr.find('td', class_='column1').text.strip(),
                'Kurstillfälle': tr.find_all('td', class_='column0')[1].text.strip(),
                'Grupp': tr.find_all('td', class_='column1')[1].text.strip() if len(tr.find_all('td', class_='column1')) > 1 else '',
                'Moment': tr.find_all('td', class_='column0')[2].text.strip(),
                'Lärare': tr.find_all('td', class_='column1')[2].text.strip() if len(tr.find_all('td', class_='column1')) > 2 else '',
                'Lokal/Plats': tr.find_all('td', class_='column0')[-1].text.strip(),
                'Kommentar': tr.find_all('td', class_='column1')[-1].text.strip() if len(tr.find_all('td', class_='column1')) > 3 else ''
            }
            classes_today.append(event_data)
        else:
            break  # Stop processing if the row is not a class row
    #print(classes_today,flush=True)
    return classes_today

def get_weather():
    url = "https://www.smhi.se/q/Falun/2715459"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to fetch weather data"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    temp_block = soup.find('div', class_='_valueCol_qjy2j_166')
    if not temp_block:
        return "No temperature data found"
    
    temps = temp_block.find_all('div')
    if len(temps) < 2:
        return "Incomplete temperature data"
    
    day_temp = temps[0].text.strip()  
    night_temp = temps[1].text.strip()
    
    return day_temp, night_temp

def stockmarket():
    url = "https://www.avanza.se/aktier/om-aktien.html/5247/tele2-b"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to fetch stock data"



def connect_to_ollama(prompt):
    """
    Connects to the Ollama model API and sends a prompt.
    """
    api_url = "http://127.0.0.1:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
    "model": "deepseek-r1:7b",  # Replace with your specific model
    "prompt": prompt,
    "stream": False  # Include the stream parameter to disable streaming
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP error codes
        return response.json().get("response", "No response field in API response")
    except requests.RequestException as e:
        return f"Failed to connect to Ollama model: {str(e)}"



app = Flask(__name__)

@app.route('/')
def home():
    events = getSchedule()  # Hämta listan med events
    weather = get_weather()
    stock = stockmarket()
    classes_today = get_classes()  # Hämta dagens klasser

    return render_template('home.html', stock=stock, weather=weather, classes=classes_today)


@app.route('/schedule')
def schedule():
    events = getSchedule()  # Hämta listan med events
    return render_template('schedule.html', events=events)


@app.route('/ask_ollama', methods=['GET', 'POST'])
def ask_ollama():
    if request.method == 'POST':
        data = request.json
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        prompt = data["prompt"]
        response = connect_to_ollama(prompt)
        return jsonify({"response": response}), 200
    
    return render_template('ask_ollama.html')






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)







