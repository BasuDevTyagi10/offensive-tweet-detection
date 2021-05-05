from flask import Flask,render_template,request
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import unidecode
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle

app = Flask(__name__)
WEBAPPNAME = "Offensive Content Detection"

def decision(results):
    outcome = []
    for prediction in results:
        if prediction == 0:
            outcome.append("Non-Offensive Language")
        elif prediction == 1:
            outcome.append("Offensive Language")
    return outcome

def cleanData(df):
    df['text'] = df['text'].apply(lambda x : ' '.join([tweet for tweet in x.split()if not tweet.startswith("@")]))
    df['text'] = df['text'].str.replace("[^a-zA-Z#*]"," ")
    df['text'] = df['text'].str.replace("RT","")
    df['text'] = df['text'].str.replace(r"#(\W+)","")
    df['text'] = df['text'].apply(lambda x : ' '.join([unidecode.unidecode(word) for word in x.split()]))
    stopWords = set(stopwords.words('english'))
    df['text'] = df['text'].apply(lambda x : ' '.join([word for word in x.split() if word not in stopWords]))
    from nltk.stem import WordNetLemmatizer 
    lemmatizer = WordNetLemmatizer()
    df['text'] = df['text'].apply(lambda x : ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
    ps = PorterStemmer()
    tokens = []
    for i in range(0,len(df)):
        tweet = df['text'][i]
        tweet = tweet.lower()
        tweet = tweet.split()
        tweet = [ps.stem(word) for word in tweet if word not in stopWords]
        tweet = ' '.join(tweet)
        tokens.append(tweet)
    df['text'] = tokens

    return df

try:
    model = pickle.load(open("./trained_model.pickle","rb"))
    vectorizer = pickle.load(open("./vectorizer.pickle","rb"))
except:
    print("Error Loading Pickle Files!")

@app.route('/')
def homePage(name=WEBAPPNAME):
    return render_template("home.html",name=name)

@app.route('/checkTweet',methods=['POST','GET'])
def checkTweet(name=WEBAPPNAME):
    if request.method == 'POST':
        tweetData = request.form['data']
        if tweetData:
            tweetData = list(filter(None, tweetData.splitlines()))
            df = pd.DataFrame(tweetData,columns=['text'])
            df = cleanData(df)
            df = vectorizer.transform(df['text'].values.astype('U'))
            predictions = model.predict(df)
            predictions = decision(predictions)
            return render_template("checkTweet.html",name=name,tweets=tweetData,results=predictions)
        else:
            errorMsg = "Please Input Some Data"
            return render_template("checkTweet.html",name=name,errorMsg=errorMsg)
    else:
        return render_template("checkTweet.html",name=name)

if __name__ == "__main__":
    app.run(debug=True)