import requests,bs4,re,hill,sklearn,numpy
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, cross_val_predict, GridSearchCV
from datetime import datetime
from pymongo import ReturnDocument
url1 = 'http://thehill.com/opinion/campaign/381765-mueller-will-drop-midterm-russia-bombshells-on-gop-congress'

def cv_opinions():
    with hill.get_mc() as mc:
        documents = []
        labels = []
        l_ops = list(mc.hillops.whitehouse.find({'lean':'l'}))
        l_documents = [item['text'] for item in l_ops]
        l_labels = [item['lean'] for item in l_ops]
        c_ops = list(mc.hillops.whitehouse.find({'lean':'c'}))
        c_documents = [item['text'] for item in c_ops]
        c_labels = [item['lean'] for item in c_ops]
        r_ops = list(mc.hillops.whitehouse.find({'lean':'r'}))
        r_documents = [item['text'] for item in r_ops]
        r_labels = [item['lean'] for item in r_ops]

    documents.extend(l_documents)
    documents.extend(c_documents)
    documents.extend(r_documents)
    labels.extend(l_labels)
    labels.extend(c_labels)
    labels.extend(r_labels)
    clf1 = SVC(kernel="linear", C=0.001)
    clf2 = SVC(kernel="linear", C=0.1)        
    clf3 = SVC(kernel="linear", C=1)
    clf4 = SVC(kernel="linear", C=10)
    clf5 = SVC(kernel="linear", C=100)
    clf6 = SVC(kernel="linear", C=1000)

    clf7 = GaussianNB()
    vec = TfidfVectorizer()
    trans_documents = vec.fit_transform(documents).toarray()
    scaler = MinMaxScaler()
    trans_documents = scaler.fit_transform(trans_documents)

    ############################################################################
    print("Support Vector Machine, linear kernel, C = 0")                    #
    print(numpy.mean(cross_val_score(clf1, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, linear kernel, C = 0.1")                  #
    print(numpy.mean(cross_val_score(clf2, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, linear kernel, C = 1")                    #
    print(numpy.mean(cross_val_score(clf3, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, linear kernel, C = 10")                   #
    print(numpy.mean(cross_val_score(clf4, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, linear kernel, C = 100")                  #
    print(numpy.mean(cross_val_score(clf5, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, linear kernel, C = 1000")                 #
    print(numpy.mean(cross_val_score(clf6, trans_documents, labels, cv=10))) #
                                                                             #
    clf1 = SVC(kernel="rbf", C=0.001, gamma=0.001)                           #
    clf2 = SVC(kernel="rbf", C=0.1, gamma=0.001)                             #
    clf3 = SVC(kernel="rbf", C=1, gamma=0.001)                               #
    clf4 = SVC(kernel="rbf", C=10, gamma=0.001)                              #
    clf5 = SVC(kernel="rbf", C=100, gamma=0.001)                             #
    clf6 = SVC(kernel="rbf", C=1000, gamma=0.001)                            #
    print("Support Vector Machine, rbf kernel, C = 0")                    #
    print(numpy.mean(cross_val_score(clf1, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 0.1")                  #
    print(numpy.mean(cross_val_score(clf2, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 1")                    #
    print(numpy.mean(cross_val_score(clf3, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 10")                   #
    print(numpy.mean(cross_val_score(clf4, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 100")                  #
    print(numpy.mean(cross_val_score(clf5, trans_documents, labels, cv=10))) #
    clf1 = SVC(kernel="rbf", C=0.001, gamma=0.0001)                          #
    clf2 = SVC(kernel="rbf", C=0.1, gamma=0.0001)                            #
    clf3 = SVC(kernel="rbf", C=1, gamma=0.0001)                              #
    clf4 = SVC(kernel="rbf", C=10, gamma=0.0001)                             #
    clf5 = SVC(kernel="rbf", C=100, gamma=0.0001)                            #
    clf6 = SVC(kernel="rbf", C=1000, gamma=0.0001)                           #
    print("Support Vector Machine, rbf kernel, C = 0.001")                #
    print(numpy.mean(cross_val_score(clf1, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 0.1")                  #
    print(numpy.mean(cross_val_score(clf2, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 1")                    #
    print(numpy.mean(cross_val_score(clf3, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 10")                   #
    print(numpy.mean(cross_val_score(clf4, trans_documents, labels, cv=10))) #
    print("Support Vector Machine, rbf kernel, C = 100")                  #
    print(numpy.mean(cross_val_score(clf5, trans_documents, labels, cv=10))) #
    ############################################################################

    ################################################################################################
    # parameters = {"C": [0.01, 1, 10, 100, 1000], "kernel": ["linear", "rbf", "sigmoid", "poly"]} #
    # gscv = GridSearchCV(SVC(), parameters)                                                       #
    ################################################################################################


    clf9 = MLPClassifier()
    clf10 = MLPClassifier(solver="lbfgs")



#    print("Neural Network, 'adam'")
#    print(numpy.mean(cross_val_score(clf9, trans_documents, labels, cv=10)))
#    print("Neural Network, 'lbfgs'")
#    print(numpy.mean(cross_val_score(clf10, trans_documents, labels, cv=10)))
    clf9.fit(trans_documents, labels)
    s = """Today, American women are assuming leadership positions in their industries, starting businesses, working hard, and pursing their own visions of happiness. They are succeeding as never before.

Yet women still, on average, earn less than men do. The creators of Equal Pay Day want to convince women that fact is evidence that, in America, the deck is still stacked against women, and the women and men who make employment decisions consistently short-change female workers out of old-fashioned bias. They declare today for Equal Pay Day, claiming that American women had to work until April 10th to make up for last year's wage gap.


That's an insult to American employers and harmful to women everywhere who deserve to know the real reasons for differences in average earnings so that they can make informed choices about their work life.
Equal Pay Day's false premise begins with a Department of Labor statistic that shows that, on average, women earn 82 percent of what men earn. But this statistic doesn't claim to compare two workers in the same job, with the same level of experience, working the same hours. It merely totals up the earnings of all full-time working women and all full-time working men and compares them.

It isn't trying to speak to “equal pay for equal work,” but rather compares the earnings of a female librarian, working 36 hours a week, for example, to the earnings of the man working 50 hours a week and risking life-and-limb manning a fishing boat. It ignores that men and women still tend to gravitate to different industries, have different work histories, and prioritize different job attributes when making career decisions.

For example, according to the Bureau of Labor Statistics Time Use Survey, full-time working men worked 8.4 hours on an average work day while full-time working women worked 7.8 hours. It is hardly surprising — or evidence of workplace discrimination — that someone who works an extra 3 hours a week earns more than someone who doesn't. In fact, that one factor alone explains about a third of the wage gap.

Women also choose jobs closer to home and that entail less physical risks. Men suffer the overwhelming majority of major physical injuries and casualties that occur on the job. It makes sense that those additional risks also garner additional rewards in the form of higher compensation.

Clearly, differences in the amount of time the average woman or man spends taking care of children plays a driving role. Society can consider why women and men make these different choices, but people shouldn't be surprised that these different decisions result in different levels of take home pay. They also shouldn't conflate the consequences of these different decisions with workplace discrimination.  

Studies that control for factors like industries, hours work, and time taken out of the workforce show a much smaller gap between men and women's pay. This is important information for women to have: Women — like men — should be aware of how the choices they make about what to study in school, what jobs, industries and specialties to pursue, and how much time to dedicate to their careers will impact their long-term earnings.

Yet earnings are just one attribute that people consider when evaluating potential jobs and careers. Increasingly, people also want jobs that are flexible, allow them to work from home or pursue other interests, and that they find personally rewarding. Women, on average, tend to have different priorities than men do. That's not a mistake or a problem that society has to solve.

Equal Pay Day's false logic isn't just the misuse of a statistic that isn't meant to speak to workplace discrimination. It also implies that women are making a mistake when they prioritize job attributes and pursuits other than earning money, and that women will only be truly equal when they make decisions that mirror men's. That's not only wrong, but insulting.  

Women shouldn't worry about what the statistics say, but should make informed decisions about the trade-offs associated with work as they pursue their own versions of happiness."""

    print(clf9.predict([scaler.transform(vec.transform(s)]))
    clf12 = GaussianNB()
    clf13 = MultinomialNB()
    print("Gaussian Naive Bayes")
    print(numpy.mean(cross_val_score(clf12, trans_documents, labels, cv=10)))
    print("Multinomial Naive Bayes")
    print(numpy.mean(cross_val_score(clf13, trans_documents, labels, cv=10)))
def present():
    with hill.get_mc() as mc:
        a = list(mc.hillops.whitehouse.find({"lean": {"$exists": False}}))
        counter = 0
        for i in a:
            counter += 1
            print(i['text'])
            lean = input('l: left, c: center, r: right, d: discard >>')
            if lean == 'd':
                mc.hillops.whitehouse.delete_one({'id':i['id']})
                continue
            elif lean != 'd' or lean != 'c' or lean != 'r' or lean != 'l':

                print('{} not an option'.format(lean))
                lean = input('l: left, c: center, r: right, d: discard >>')

            print(mc.hillops.whitehouse.find_one_and_update({'id':i['id']}, {'$set': {'lean':lean}}, projection=['id', 'lean'], return_document=ReturnDocument.AFTER))
            if counter >= 10:
                break
    print('done')
            
            


def clean(text):

    text = re.sub("[\n]+", " ", text)
    
    text = re.sub("[\s]+", " ", text)
    text = re.sub("(^\s)|(\s$)", "", text)
    return text
def get_author_and_text(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    date_ele = soup.select('span.submitted-date')
    if date_ele:
        # 04/05/18 12:15 PM EDT
        date = date_ele[0].text[:-4]

        date = datetime.strptime(date, "%m/%d/%y %I:%M %p")

        
    else:
        date = ''
        
    author_ele = soup.select('span.submitted-by')
    if author_ele:
        author = clean(author_ele[0].text).split(" ", 1)[1].split(",")[0]
    else:
        author = ''
    [item.decompose() for item in soup.select('span.rollover-people-block, div.field-item > p > ul, div.field-item > p > strong')]
    article_text = " ".join([item.text for item in soup.select('div.field-item > p, div.field-item > a[rel|=noopener]')])
    print(date)
    print(author)
    print(clean(article_text))
    return {'date':date, 'author': author, 'text': clean(article_text)}

def mc_update():
    with hill.get_mc() as mc:
        obj = list(mc.hillops.whitehouse.find({}))
        for item in obj:
            r = get_author_and_text(item['href'])
            print(mc.hillops.whitehouse.find_one_and_update({'id':item['id']}, {"$set": r}, return_document=ReturnDocument.AFTER))
            
if __name__ == "__main__":
    cv_opinions()


        
