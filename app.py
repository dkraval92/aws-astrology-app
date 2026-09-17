from flask import Flask, render_template, request
import hashlib
import ephem
import math
from geopy.geocoders import Nominatim

app = Flask(__name__)
# Geolocator API जो शहर के नाम को Latitude/Longitude में बदलेगी
geolocator = Nominatim(user_agent="aws_cloud_astrology_app")

def calculate_real_moon_sign(dob, time_str, place):
    try:
        # शहर के नाम से Latitude और Longitude निकालना
        try:
            location = geolocator.geocode(place, timeout=5)
            lat = str(location.latitude)
            lon = str(location.longitude)
        except:
            # अगर कोई छोटा गांव डाला जो मैप पर न मिले, तो डिफ़ॉल्ट इंडिया की लोकेशन ले लेगा
            lat = '20.5937'
            lon = '78.9629'

        date_format = dob.replace("-", "/") + " " + time_str
        
        observer = ephem.Observer()
        observer.date = date_format
        observer.lat = lat  # सटीक कैलकुलेशन के लिए Latitude
        observer.lon = lon  # सटीक कैलकुलेशन के लिए Longitude
        
        moon = ephem.Moon()
        moon.compute(observer)
        
        # वैदिक अयानांश घटाकर मून साइन निकालना
        lon_deg = math.degrees(ephem.Ecliptic(moon).lon)
        vedic_lon = (lon_deg - 24.13) % 360
        sign_index = int(vedic_lon / 30)
        
        rashis = ["Mesha (Aries) ♈", "Vrishabha (Taurus) ♉", "Mithuna (Gemini) ♊", "Karka (Cancer) ♋", 
                  "Simha (Leo) ♌", "Kanya (Virgo) ♍", "Tula (Libra) ♎", "Vrishchika (Scorpio) ♏", 
                  "Dhanu (Sagittarius) ♐", "Makara (Capricorn) ♑", "Kumbha (Aquarius) ♒", "Meena (Pisces) ♓"]
                  
        return rashis[sign_index]
    except Exception as e:
        return "Unable to calculate"

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
        # name.title() पहला अक्षर अपने आप Capital कर देगा (उदा: rahul -> Rahul)
        name = request.form.get('name').title() 
        dob = request.form.get('dob')
        time_str = request.form.get('time')
        place = request.form.get('place')
        
        result = get_prediction(name, dob, time_str, place)
        result['name'] = name
        result['place'] = place.title()
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
