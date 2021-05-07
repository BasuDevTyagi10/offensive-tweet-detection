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
import tweepy
from tweepy import OAuthHandler
import pygal

app = Flask(__name__)
WEBAPPNAME = "Offensive Content Detection"

class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        api_key = '8GiR9xnlVbv5PO42MOxJPsT2g'
        api_secret = 'kbTVKxrENF4Ykz3h813VzUZP40dCHqcpZRkVfsSByBkXrkEpM5'
        access_token = '1103383570087763969-rYOVL2XnAV5tf9LgqeG6cU3rCbUYFL'
        access_token_secret = 'RGsdXYfSnKBgU5MqipHRDHF1x31grnrj8LFo3qSbAKDie'
  
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(api_key, api_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
    def get_tweets(self, query, count = 100):
        
        try:
            # call twitter api to fetch 
            fetched_tweets = self.api.search(query,count=count,lang='en')
            tweets = []
            for tweet in fetched_tweets:
                tweets.append(tweet.text)

            # return parsed tweets
            tweets = list(dict.fromkeys(tweets))
            return tweets
  
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

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
            offensive = 0
            nonoffensive = 0
            for prediction in predictions:
                if prediction == 0:
                    nonoffensive = nonoffensive+1
                else:
                    offensive = offensive+1
            total = offensive+nonoffensive
            offensivePer = float(offensive)/float(total)*100
            nonoffensivePer = float(nonoffensive)/float(total)*100
            predictions = decision(predictions)
            pie_chart = pygal.Pie(inner_radius=.4)
            pie_chart.title = "Pie-Chart for Offensive Tweets vs Non-Offensive Tweets (%)"
            pie_chart.add('Offensive',offensivePer)
            pie_chart.add('Non-Offensive',nonoffensivePer)
            pie_chart = pie_chart.render_data_uri()
            return render_template("checkTweet.html",name=name,tweets=tweetData,results=predictions,graph=pie_chart)
        else:
            errorMsg = "Please Input Some Data"
            return render_template("checkTweet.html",name=name,errorMsg=errorMsg)
    else:
        data = {'Offensive' : 100, 'Non-Offensive' : 200}
        return render_template("checkTweet.html",name=name,data=data)

@app.route('/getTweetsAPI',methods=['POST','GET'])
def getTweetsAPI(name=WEBAPPNAME):
    if request.method == 'POST':
        api = TwitterClient()
        topic = request.form['keyword']
        count = request.form['count']
        if topic:
            try:
                if count:
                    tweets = api.get_tweets(topic,count=count)
                else:
                    tweets = api.get_tweets(topic)
                return render_template("getTweetsAPI.html",name=name,results=tweets)
                # return(str(tweets))
            except:
                return "Error Occured"
        else:
            errorMsg = "Please Input Some Data"
            return render_template("getTweetsAPI.html",name=name,errorMsg=errorMsg)
    else:
        return render_template("getTweetsAPI.html",name=name)

if __name__ == "__main__":
    app.run(debug=True)