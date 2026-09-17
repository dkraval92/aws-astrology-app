from flask import Flask, render_template, request
import hashlib
import ephem
import math
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  <-- यह लाइन जोड़ दें

def calculate_real_moon_sign(dob, time_str):
    try:
        dt_str = f"{dob} {time_str}"
        local_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=5, minutes=30)
        
        ephem_date = ephem.Date(utc_dt)
        moon = ephem.Moon(ephem_date)
        ecliptic = ephem.Ecliptic(moon)
        tropical_lon = math.degrees(ecliptic.lon)
        
        days_from_2000 = (utc_dt - datetime(2000, 1, 1, 12, 0)).total_seconds() / 86400.0
        ayanamsa = 23.85 + (days_from_2000 / 365.25) * 0.0139694
        
        vedic_lon = (tropical_lon - ayanamsa) % 360
        sign_index = int(vedic_lon / 30)
        
        rashis = ["Mesha (Aries) ♈", "Vrishabha (Taurus) ♉", "Mithuna (Gemini) ♊", "Karka (Cancer) ♋", 
                  "Simha (Leo) ♌", "Kanya (Virgo) ♍", "Tula (Libra) ♎", "Vrishchika (Scorpio) ♏", 
                  "Dhanu (Sagittarius) ♐", "Makara (Capricorn) ♑", "Kumbha (Aquarius) ♒", "Meena (Pisces) ♓"]
                  
        return rashis[sign_index]
    except Exception as e:
        return "Calculation Error"

def get_prediction(name, dob, place):
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
        
        moon_sign = calculate_real_moon_sign(dob, time_str)
        
        result = get_prediction(name, dob, place)
        result['name'] = name
        result['place'] = place
        result['moon_sign'] = moon_sign
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
