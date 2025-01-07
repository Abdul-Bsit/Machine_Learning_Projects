from flask import Flask, render_template, request, redirect, url_for
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation
from joblib import load
import os

# Load the model and vectorizer
loaded_model = load("svm_model.joblib")
loaded_vectoriser = load("vectoriser.joblib")

# Define stopwords
STOPWORDS = set(stopwords.words('english'))

# Initialize Porter Stemmer
st = PorterStemmer()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = None
        if 'text' in request.form and request.form["text"].strip():
            text = request.form["text"]
            print("Text input received:", text)
        elif 'file' in request.files:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                with open(file_path, 'r') as f:
                    text = f.read()
                print("File content received:", text)
            else:
                return render_template("index.html", error="Invalid file type. Please upload a text file.")
        
        if text:
            # Preprocess the input text
            processed_text = preprocess_tweet(text)
            # Vectorize the processed text
            vectorised_text = loaded_vectoriser.transform([processed_text])
            # Predict sentiment
            sentiment = loaded_model.predict(vectorised_text)[0]
            # Determine sentiment label
            sentiment_label = "Positive" if sentiment == 1 else "Negative"
            return render_template("index.html", text=text, sentiment=sentiment_label)
    
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("About.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

def preprocess_tweet(tweet):
    # Convert to lowercase
    processed_tweet = tweet.lower()
    # Expand contractions
    processed_tweet = decontracted(processed_tweet)
    # Remove stopwords
    processed_tweet = cleaning_stopwords(processed_tweet)
    # Convert emoticons
    processed_tweet = smiley(processed_tweet)
    # Remove digits
    processed_tweet = re.sub(r'\w*\d\w*', '', processed_tweet)
    # Remove punctuations
    processed_tweet = clean_punctuations(processed_tweet)
    # Clean repeating characters
    processed_tweet = cleaning_repeating_char(processed_tweet)
    # Remove URLs
    processed_tweet = cleaning_URLs(processed_tweet)
    # Remove numbers
    processed_tweet = cleaning_numbers(processed_tweet)
    # Tokenize into sentences
    sentences = sent_tokenize(processed_tweet)
    # Join sentences
    processed_tweet = ' '.join(sentences)
    # Stemming
    processed_tweet = stemming_on_text(processed_tweet)
    # Convert chat words
    processed_tweet = chat_words_conversion(processed_tweet)
    return processed_tweet

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def cleaning_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

def smiley(a):
    x1 = a.replace(":‑)", "happy")
    x2 = x1.replace(";)", "happy")
    x3 = x2.replace(":-}", "happy")
    x4 = x3.replace(":)", "happy")
    x5 = x4.replace(":}", "happy")
    x6 = x5.replace("=]", "happy")
    x7 = x6.replace("=)", "happy")
    x8 = x7.replace(":D", "happy")
    x9 = x8.replace("xD", "happy")
    x10 = x9.replace("XD", "happy")
    x11 = x10.replace(":‑(", "sad")
    x12 = x11.replace(":‑[", "sad")
    x13 = x12.replace(":(", "sad")
    x14 = x13.replace("=(", "sad")
    x15 = x14.replace("=/", "sad")
    x16 = x15.replace(":[", "sad")
    x17 = x16.replace(":{", "sad")
    x18 = x17.replace(":P", "playful")
    x19 = x18.replace("XP", "playful")
    x20 = x19.replace("xp", "playful")
    x21 = x20.replace("<3", "love")
    x22 = x21.replace(":o", "shock")
    x23 = x22.replace(":-/", "sad")
    x24 = x23.replace(":/", "sad")
    x25 = x24.replace(":|", "sad")
    return x25

def clean_punctuations(text):
    translator = str.maketrans('', '', punctuation)
    return text.translate(translator)

def cleaning_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)

def cleaning_URLs(data):
    return re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', data)

def cleaning_numbers(data):
    return re.sub(r'\d+', '', data)

def stemming_on_text(data):
    words = word_tokenize(data)
    text = [st.stem(word) for word in words]
    return ' '.join(text)

slang_dict = {
    "bae": "Before Anyone Else",
    "bb": "Bareback",
    "bff": "Best Friends Forever",
    "brb": "Be Right Back",
    "btw": "By The Way",
    "bump": "Bring Up My Post",
    "cba": "Can't Be Arsed",
    "ciao": "Goodbye",
    "cu": "See You",
    "dank": "High-Quality Marijuana",
    "dawg": "Close Friend",
    "dm": "Direct Message",
    "dope": "Cool, Awesome",
    "eod": "End Of Discussion",
    "fam": "Family",
    "fbo": "Facebook Official",
    "ffs": "For Fuck's Sake",
    "fomo": "Fear Of Missing Out",
    "fml": "Fuck My Life",
    "foodie": "A Person Who Loves Food",
    "ftfy": "Fixed That For You",
    "ftw": "For The Win",
    "fwiw": "For What It's Worth",
    "gfy": "Go Fuck Yourself",
    "gg": "Good Game",
    "gotcha": "I Understand",
    "gr8": "Great",
    "gtg": "Got To Go",
    "hbu": "How About You?",
    "icymi": "In Case You Missed It",
    "idgaf": "I Don't Give A Fuck",
    "idk": "I Don't Know",
    "ikr": "I Know, Right?",
    "imho": "In My Humble Opinion",
    "irl": "In Real Life",
    "iso": "In Search Of",
    "jelly": "Jealous",
    "jk": "Just Kidding",
    "k": "Okay",
    "kms": "Kill Myself",
    "lit": "Awesome",
    "lmao": "Laughing My Ass Off",
    "lmk": "Let Me Know",
    "lol": "Laughing Out Loud",
    "mcm": "Man Crush Monday",
    "mfw": "My Face When",
    "ngl": "Not Gonna Lie",
    "nm": "Never Mind",
    "noob": "Newbie",
    "nsfw": "Not Safe For Work",
    "nvm": "Never Mind",
    "obvi": "Obviously",
    "og": "Original Gangster",
    "omg": "Oh My God",
    "ootd": "Outfit Of The Day"
}

def chat_words_conversion(text):
    return " ".join(slang_dict.get(word.lower(), word) for word in text.split())

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
