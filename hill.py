import requests,re,bs4,pymongo,sklearn,pandas,concurrent.futures,html
from settings import dbuser,dbpassword
from flask import Flask, render_template, request
from selenium import webdriver

app = Flask(__name__)

categories = []

opinion_url = 'http://thehill.com/opinion/'
whurl = 'http://thehill.com/opinion/white-house?page=2'
opinion_base = 'http://thehill.com{}'
def get_mc():
    return pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword))

def scrape():
    template='http://thehill.com/opinion/white-house?page={}'
    urls = [template.format(i) for i in range(0,169)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        l = executor.map(scrape_page, urls)
    l = [subitem for item in l if item for subitem in item]
    pandas.DataFrame(l).to_csv("whitehouse.csv", index=False)
    with get_mc() as mc:
        for item in l:
            print(mc.hillops['white-house'].insert_one(item).inserted_id)
    print('inserted {} articles'.format(len(l)))
        
 
#    l = [
#    with open
    
def scrape_page(url):
    try:
        r = requests.get(url)
        print('{} request returned with status {}'.format(url, r.status_code)) 

    #    if r.status_code == 200:
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        elements = soup.select('h2.node-title > a')
        things = [{'category':'white-house','title':element.text, 'href':'http://thehill.com{}'.format(element['href']), 'id':re.findall('[\d]{6}', element['href'])[0]} for element in elements]
        return things
    except Exception as e:
        print(e)
        return None
        

@app.route("/")
def index():

#    categories = [(category, " ".join([c.capitalize() for c in category.split("-")])) for category in load_categories()]
    with pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword)) as mc:
        articles = list(mc.hillops.whitehouse.find({'lean': {"$exists":True}}).limit(20))
    
    return return_articles(which="articles2.html", page_header="Classification of The Hill opinion pieces", category='', articles=articles, categories=categories)
    


@app.route("/category/<category>/")
def get_category(category):

    # ADD AJAX to preview articles

    global categories
    if category not in load_categories():
        return render_template('error.html')
    with pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword)) as mc:
        articles = list(mc.hillops.whitehouse.find({'category': category, 'lean': {"$exists":True}}))
    
    return return_articles(which="articles2.html", page_header=" ".join(category.split("-")).capitalize(), category=category, articles=articles, categories=categories)

@app.route("/columnist/<columnist>/")
def columnnist(columnist):
    global categories
    decode_col = html.unescape(columnist)
    " ".join([c.capitalize() for c in decode_col.split(" ")])
    with get_mc() as mc:
        articles = list(mc.hillops.whitehouse.find({"author":decode_col}))
    if len(articles) == 0:
        return "error: no articles found"
    return return_articles(which="articles2.html", page_header=decode_col,category='', articles=articles, categories=categories)

@app.route("/classify", methods=["GET", "POST"])
def classify(previous=''):
    if request.method == "POST":
        id = int(request.form.get("article_id", None))



        lean = request.form.get("classification", None)

        if not id and not lean:
            previous = "wtf1"
        elif not id:
            previous = lean
        elif not lean:
            previous = id
        else:
            previous = " - ".join([str(id), lean])
        with get_mc() as mc:
            mc.hillops.whitehouse.find_one_and_update({"id": id}, {"$set": {"lean": lean}})
            
    with get_mc() as mc:
        articles = mc.hillops.whitehouse.find({"lean": {"$exists": False}}).limit(20)
        articles = list(articles)
    if not previous:
        previous = "Please classify these by political lean, if you have the time :)"
    return return_articles(which="classify.html", page_header=previous, category='', articles=articles, categories=categories, do_shorten=False)

        

        
    

    
def return_articles(which, page_header, category, articles, categories, do_shorten=True):
                              
    mod_categories = [(topic_c, " ".join([c.capitalize() for c in topic_c.split("-")])) for topic_c in categories]
    if do_shorten:
        for article in articles:
            article["text"] = " ".join(article["text"].split(" ")[:50])
    if len(articles) > 20:
        articles = articles[:21]
    for article in articles:
        article["encode_author"] = html.escape(article["author"])
    return render_template(which, page_header=page_header, category=category, articles=articles, categories=mod_categories)
def load_categories():
    global categories

    if not categories:
        with pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword)) as mc:
            categories = mc.hillops.hillops.find_one({'category': 'id'})['categories']
    return categories 

def get_opinions():
    r = requests.get(whurl)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    ops = soup.find_all('a', href=re.compile('/opinion/[a-z\-]+/'))
    op_links = [op['href'] for op in ops]
#    mc = pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword))
    driver = webdriver.Chrome()

    categories = load_categories()
    op_links = [opinion_base.format(op_link) for op_link in op_links if op_link.split("/")[2] in categories]
    op_links = pandas.unique(op_links)
    with pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword)) as mc:
        for op_link in op_links:
            driver.get(op_link)
            print("choose `l`, `c`, `r`")
            ci = input('lean \t>>')
            print("0: anti, 1: neutral, 2: pro, 3: doesn't mention")
            pt = input('protrump \t>>')
            cat = op_link.split("/")[2]
            id = re.findall("([0-9]+)", op_link)[0]
            ins_id = mc.hillops.hillops.insert_one({'article-id': id, 'lean': ci, 'protrump': pt, 'category': cat, 'href':op_link}).inserted_id
            print(ins_id)
    print('done')
    
def load_training_lean():
    """ returns [(text, classlabel)] """
    with pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword)) as mc:
        articles = mc.hillops.allarticles.find({})
        training = [(fetch_text(article['href']), article['lean']) for article in articles if 'article-id' in article]
    return training

def fetch_text(href):
    r = requests.get(opinion_base.format(href))
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    text = " ".join([item.text for item in soup.select('div.field-item > p')])
    return text

if __name__ == "__main__": 
    app.run()
