from flask import Flask, render_template, request
import hashlib
import ephem
import math
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

app = Flask(__name__)
geolocator = Nominatim(user_agent="aws_cloud_astrology_app")

def calculate_real_moon_sign(dob, time_str, place):
    try:
        # 1. IST समय को UTC में बदलना (सबसे बड़ी गलती यहीं ठीक की गई है)
        local_dt = datetime.strptime(f"{dob} {time_str}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=5, minutes=30)
        ephem_date = utc_dt.strftime("%Y/%m/%d %H:%M:%S")

        # 2. जगह का Latitude/Longitude निकालना
        try:
            location = geolocator.geocode(place, timeout=5)
            lat = str(location.latitude)
            lon = str(location.longitude)
        except:
            lat = '23.0225' # Default to Ahmedabad if place not found
            lon = '72.5714'

        # 3. Observer (व्यक्ति) की स्थिति सेट करना
        observer = ephem.Observer()
        observer.date = ephem_date
        observer.lat = lat
        observer.lon = lon
        
        moon = ephem.Moon()
        moon.compute(observer)
        
        # 4. Ayanamsa Calculation (सटीक वैदिक गणित के लिए)
        year_fraction = utc_dt.year + (utc_dt.timetuple().tm_yday / 365.25)
        ayanamsa = 23.85 + (year_fraction - 2000) * 0.0139694
        
        lon_deg = math.degrees(ephem.Ecliptic(moon).lon)
        vedic_lon = (lon_deg - ayanamsa) % 360
        sign_index = int(vedic_lon / 30)
        
        rashis = ["Mesha (Aries) ♈", "Vrishabha (Taurus) ♉", "Mithuna (Gemini) ♊", "Karka (Cancer) ♋", 
                  "Simha (Leo) ♌", "Kanya (Virgo) ♍", "Tula (Libra) ♎", "Vrishchika (Scorpio) ♏", 
                  "Dhanu (Sagittarius) ♐", "Makara (Capricorn) ♑", "Kumbha (Aquarius) ♒", "Meena (Pisces) ♓"]
                  
        return rashis[sign_index]
    except Exception as e:
        return "Unable to calculate (Check details)"

def get_prediction(name, dob, time_str, place):
    moon_sign = calculate_real_moon_sign(dob, time_str, place)
    
    hash_str = f"{name}{dob}{place}"
    hash_val = int(hashlib.md5(hash_str.encode()).hexdigest(), 16)
    
    careers = [
        "Excellent planetary alignments for IT, Cloud, and DevOps. Major success indicated.",
        "Sudden positive shift in career. Focus on upskilling, promotion is on the way.",
        "Foreign travel or high-paying remote opportunities are strongly visible in your chart.",
        "Great time for leadership roles. Your technical skills will bring major financial rewards."
    ]
    money = [
        "Strong wealth yog! Long-term investments will yield excellent returns.",
        "Unexpected financial gains from past work. A very prosperous period.",
        "Stable income flow. Avoid risky investments for the next 45 days.",
        "Your hard work is converting into solid assets. Great time to buy property."
    ]
    marriage = [
        "Venus and Jupiter indicate a highly supportive and loving life partner.",
        "Perfect time for relationships. A deep, soulful connection is on the horizon.",
        "Harmony in personal life will give you peace of mind to focus on career.",
        "Mutual respect and immense love are the foundation of your relationship axis."
    ]
    
    return {
        "moon_sign": moon_sign,
        "career": careers[hash_val % 4],
        "money": money[(hash_val + 1) % 4],
        "marriage": marriage[(hash_val + 2) % 4]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        name = request.form.get('name').title()
        dob = request.form.get('dob')
        time_str = request.form.get('time')
        place = request.form.get('place').title()
        
        result = get_prediction(name, dob, time_str, place)
        result['name'] = name
        result['place'] = place
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
