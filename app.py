from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

def get_prediction(name, dob):
    # यह लॉजिक नाम और जन्मतिथि के आधार पर हमेशा एक फिक्स रिज़ल्ट देगा (Cloud Demo के लिए परफेक्ट)
    hash_str = f"{name}{dob}"
    hash_val = int(hashlib.md5(hash_str.encode()).hexdigest(), 16)
    
    # 12 राशियां (Moon Signs)
    rashis = ["Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)", 
              "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)", 
              "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"]
    
    moon_sign = rashis[hash_val % 12]
    
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
        result = get_prediction(name, dob)
        result['name'] = name
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
