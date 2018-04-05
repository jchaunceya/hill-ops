import requests,re,bs4,pymongo,sklearn,pandas,concurrent.futures
from settings import dbuser,dbpassword
from flask import Flask, render_template
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

    categories = [(category, " ".join([c.capitalize() for c in category.split("-")])) for category in load_categories()]
    
    return render_template('index.html', categories=categories)

@app.route("/category/<category>/")
def get_category(category):

    # ADD AJAX to preview articles

    global categories
    if category not in load_categories():
        return render_template('error.html')
    with pymongo.MongoClient('mongodb://{}:{}@ds117469.mlab.com:17469/hillops'.format(dbuser, dbpassword)) as mc:
        articles = mc.hillops.allarticles.find({'category': category})

    mod_categories = [(category, " ".join([c.capitalize() for c in category.split("-")])) for category in categories]
    if articles:
        r = requests.get(opinion_base.format(articles[0]['href']))
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        preview = " ".join([item.text for item in soup.select('div.field-item > p')])[:50] + '...'
                         
    return render_template('articles.html', category=category, articles=[article['href'] for article in articles], categories=mod_categories, preview=preview)

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
    scrape()
