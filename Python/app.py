from flask import Flask , render_template
from bs4 import BeautifulSoup
import requests




def getSchedule():
    url = "https://cloud.timeedit.net/hda/web/public/s/s.html?tab=3&object=person.stud.h22carja&type=Alla&object=courseOccasion.H3J6K&type=Alla&object=courseOccasion.H3KAY&type=Alla&object=courseOccasion.V3KPR&type=Alla&object=courseOccasion.V3KPS&type=Alla&object=programmeOccasion.H3BCW&type=Alla&p=6.months"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "fail"
    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    for tr in soup.find_all('tr', class_='clickable2'):
        event_data = {
            'tid': tr.find('td', class_='time').text.strip(),
            'koder': tr.find('td', class_='column0').text.strip(),
            'namn': tr.find('td', class_='column1').text.strip(),
            'typ': tr.find_all('td', class_='column0')[2].text.strip(),
            'ledare': tr.find('td', class_='column1', id=None).text.strip(),  # Senare förekomst av column1 utan id
            'plats': tr.find_all('td', class_='column0')[-1].text.strip(),
        }
        events.append(event_data)
    return events


app = Flask(__name__)

@app.route('/')
def home():
    events = getSchedule()  # Hämta listan med events
    return render_template('home.html')


@app.route('/schedule')
def schedule():
    events = getSchedule()  # Hämta listan med events
    return render_template('schedule.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)


