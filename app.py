from flask import Flask, render_template, request
import hashlib
import ephem
import math

app = Flask(__name__)

def calculate_real_moon_sign(dob, time_str):
    try:
        # Date और Time को ephem फॉर्मेट (YYYY/MM/DD HH:MM:SS) में बदलना
        date_format = dob.replace("-", "/") + " " + time_str
        
        observer = ephem.Observer()
        observer.date = date_format
        
        moon = ephem.Moon()
        moon.compute(observer)
        
        # Moon की Tropical Longitude (Degrees में)
        lon_deg = math.degrees(ephem.Ecliptic(moon).lon)
        
        # वैदिक ज्योतिष (Sidereal) के लिए Lahiri Ayanamsa (approx 24.13°) घटाना
        vedic_lon = (lon_deg - 24.13) % 360
        
        # 30-30 डिग्री की एक राशि होती है
        sign_index = int(vedic_lon / 30)
        
        rashis = ["Mesha (Aries) ♈", "Vrishabha (Taurus) ♉", "Mithuna (Gemini) ♊", "Karka (Cancer) ♋", 
                  "Simha (Leo) ♌", "Kanya (Virgo) ♍", "Tula (Libra) ♎", "Vrishchika (Scorpio) ♏", 
                  "Dhanu (Sagittarius) ♐", "Makara (Capricorn) ♑", "Kumbha (Aquarius) ♒", "Meena (Pisces) ♓"]
                  
        return rashis[sign_index]
    except Exception as e:
        return "Unable to calculate"

def get_prediction(name, dob, time_str):
    # असली चंद्र राशि निकालना
    moon_sign = calculate_real_moon_sign(dob, time_str)
    
    # Career, Money, Marriage के लिए हम Mock Logic (Hash) ही रखेंगे ताकि रिजल्ट्स फिक्स रहें
    hash_str = f"{name}{dob}"
    hash_val = int(hashlib.md5(hash_str.encode()).hexdigest(), 16)
    
    careers = [
        "Excellent time for IT, Cloud Computing, and DevOps roles. Leadership opportunities are visible.",
        "A sudden positive shift in your career path. Hard work will bring technical promotions.",
        "Favorable period for foreign opportunities or remote jobs with high packages.",
        "Your analytical skills will shine. Great time to switch jobs for a better role."
    ]
    money = [
        "Financial stability is strong. Good time for long-term investments in assets.",
        "Unexpected financial gains are indicated in the next 3 months.",
        "Avoid speculative investments right now; focus on saving your current income.",
        "Past investments will start yielding excellent returns very soon."
    ]
    marriage = [
        "Harmonious planetary alignments indicate peace and support from your partner.",
        "If you are single, there are high chances of finding a compatible partner soon.",
        "Focus on clear communication. A very stable and happy family life is predicted.",
        "Venus is in a strong position, bringing love, care, and mutual respect in relationships."
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
        name = request.form.get('name')
        dob = request.form.get('dob')
        time_str = request.form.get('time')
        
        result = get_prediction(name, dob, time_str)
        result['name'] = name
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
