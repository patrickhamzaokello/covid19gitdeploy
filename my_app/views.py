from django.shortcuts import render
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


# rending the twitter page
from my_app.twittermodule.tweet_store import TweetStore


url = Request("https://www.worldometers.info/coronavirus/", headers={'User-Agent': 'Mozilla/5.0'})
# url = "file:///C:/Users/Freedom/Covid19Project/Offline%20sites/woldometersiteoffline.html"


news_url = Request("https://news.google.com/rss?hl=en-UG&gl=UG&ceid=UG:en", headers={'User-Agent': 'Mozilla/5.0'})
# news_url = "file:///C:/Users/Freedom/Covid19Project/Offline%20sites/googlenewsrss.xml"

gobalnewsurl = Request("https://news.google.com/news/rss", headers={'User-Agent': 'Mozilla/5.0'})
# gobalnewsurl = "file:///C:/Users/Freedom/Covid19Project/Offline%20sites/googlenewsrss.xml"




def basepage(request):
    html = urlopen(url).read()

    soup = BeautifulSoup(html, features="html.parser")

    #mytable = soup.find('table', {'class': 'table table-bordered table-hover main_table_countries dataTable no-footer'})
    mytable = soup.find('table')

    tableheadfind = mytable.find_all('th')
    tabletitles = []

    # getting titles for the table headings
    for titles in tableheadfind:
        tableheader = titles.text

        tabletitles.append(tableheader)

    # Getting top 5 records for the table

    table_rows = mytable.find_all('tr')[:7]
    tablerow = []

    for tr in table_rows:
        td = tr.find_all('td')[1:8]
        row = [(i.text).replace(" ", "") for i in td]
        tablerow.append(row)

    # tablewithzeros = [[x or '0' for x in xs] for xs in tablerow]
    tablewithzeros = tablerow

    import datetime
    x = datetime.datetime.now()

    timenow = x.strftime("%a") + ' ' + x.strftime("%B") + ' ' + x.strftime("%d") + ',' + x.strftime(
        "%Y") + ', ' + x.strftime(
        "%X") + ' ' + x.strftime("%Z")

    covidno = soup.find_all(class_="maincounter-number")
    finaldatacase = []

    for covidnogot in covidno:
        covidnogot = (covidnogot.text).strip()
        finaldatacase.append(covidnogot)

    cases = finaldatacase[0]
    deaths = finaldatacase[1]
    recovered = finaldatacase[2]

    # activecases
    covidcase = soup.find_all(class_="number-table")
    activecases = []

    for i in covidcase:
        i = (i.text).strip()
        activecases.append(i)

    mildcondition = int(activecases[0].replace(',', ''))
    SeriousCritical = int(activecases[1].replace(',', ''))
    Activecases = mildcondition+SeriousCritical
    commafixed = ('{:,}'.format(Activecases))

    # other summary
    total = soup.find('tr', {'class': 'total_row'})
    data = total.find_all('td')

    # search uganda
    alltable_rowsfind = mytable.find_all('tr')[1:]
    alltablerow = []
    for tr in alltable_rowsfind:
        td = tr.find_all('td')[1:]
        row = [(i.text).replace(" ", '') for i in td]

        alltablerow.append(row)

    allrecordswith0 = [[x or '0' for x in xs] for xs in alltablerow]

    sr = 'Uganda'

    keyword = sr.title()

    uganda = [i for i in allrecordswith0 if keyword in i]

    casesug = uganda[0][1]
    newcasesug = uganda[0][2]
    deathsug = uganda[0][3]
    recoveredug = uganda[0][5]
    activecasesug = uganda[0][6]
    testdone = uganda[0][10]

    # East africa
    s1 = 'Rwanda'
    s2 = 'Kenya'
    s3 = 'Burundi'
    s4 = 'Tanzania'
    s5 = 'SouthSudan'

    searchRwanda = [i for i in allrecordswith0 if s1 in i]
    searchKenya = [i for i in allrecordswith0 if s2 in i]
    searchBurundi = [i for i in allrecordswith0 if s3 in i]
    searchTanzania = [i for i in allrecordswith0 if s4 in i]
    searchSouthSudan = [i for i in allrecordswith0 if s5 in i]
    # african countries
    africareport = mytable.find_all('tr')[1:]
    africarows = []
    for tr in africareport:
        td = tr.find_all('td')[1:]
        row = [(i.text).replace(" ", '') for i in td]

        africarows.append(row)

    sr = 'Africa'

    keyword = sr.title()

    africacases = [i for i in africarows if keyword in i]
    #uganda = [[x or '0' for x in xs] for xs in africacases]

    store = TweetStore()
    tweets = store.tweets()

    # news site
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()

    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date

    allnews_list = []
    for news in news_list:
        newstitle = news.title.text
        newslink = news.link.text
        newspubDate = news.pubDate.text

        allnews_list.append((newstitle, newslink, newspubDate))

    stuff_for_frontend = {

        'tabletitle': tabletitles[1:8],
        'tablerow': tablewithzeros,
        'timenow': timenow,
        'cases': cases,
        'deaths': deaths,
        'recovered': recovered,
        'newcases': alltablerow[-1][2],  # from table
        'newdeath': alltablerow[-1][4],  # from table
        'Activecases': commafixed,
        'SeriousCritical': activecases[1],
        'mildcondition': activecases[0],
        'casesug': casesug,
        'newcasesug': newcasesug,
        'deathsug': deathsug,
        'recoveredug': recoveredug,
        'testdone': testdone,
        'activecasesug': activecasesug,
        'news_list': allnews_list,

        # eastafrica
        'Rtotal': searchRwanda[0][1],
        'Rdeaths': searchRwanda[0][3],
        'Rrecovered': searchRwanda[0][5],
        'Ractive': searchRwanda[0][6],

        'Ktotal': searchKenya[0][1],
        'Kdeaths': searchKenya[0][3],
        'Krecovered': searchKenya[0][5],
        'Kactive': searchKenya[0][6],

        'Btotal': searchBurundi[0][1],
        'Bdeaths': searchBurundi[0][3],
        'Brecovered': searchBurundi[0][5],
        'Bactive': searchBurundi[0][6],

        'Ttotal': searchTanzania[0][1],
        'Tdeaths': searchTanzania[0][3],
        'Trecovered': searchTanzania[0][5],
        'Tactive': searchTanzania[0][6],

        'Stotal': searchSouthSudan[0][1],
        'Sdeaths': searchSouthSudan[0][3],
        'Srecovered': searchSouthSudan[0][5],
        'Sactive': searchSouthSudan[0][6],

        # africa table
        'aftabletitles': tabletitles[1:],
        'africarow': africacases,
        'tweets': tweets

    }

    return render(request, 'base.html', stuff_for_frontend)



def globaldata(request):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # mytable = soup.find('table', {'class': 'table table-bordered table-hover main_table_countries dataTable no-footer'})
    mytable = soup.find('table')

    tableheadfind = mytable.find_all('th')
    tabletitles = []

    # getting titles for the table headings
    for titles in tableheadfind:
        tableheader = titles.text

        tabletitles.append(tableheader)

    # Getting top 5 records for the table

    table_rows = mytable.find_all('tr')[8:]
    tablerow = []

    for tr in table_rows:
        td = tr.find_all('td')[1:]
        row = [(i.text).replace(" ", "") for i in td]
        tablerow.append(row)

    # tablewithzeros = [[x or '0' for x in xs] for xs in tablerow]

    import datetime
    x = datetime.datetime.now()

    timenow = x.strftime("%a") + ' ' + x.strftime("%B") + ' ' + x.strftime("%d") + ',' + x.strftime(
        "%Y") + ', ' + x.strftime(
        "%X") + ' ' + x.strftime("%Z")

    # news site
    Client = urlopen(gobalnewsurl)
    xml_page = Client.read()
    Client.close()

    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date

    allnews_list = []
    for news in news_list:
        newstitle = news.title.text
        newslink = news.link.text
        newspubDate = news.pubDate.text

        allnews_list.append((newstitle, newslink, newspubDate))

    stuff_for_frontend = {

        'tabletitle': tabletitles[1:],
        'tablerow': tablerow,
        'timenow': timenow,
        'news_list': allnews_list

    }

    return render(request, 'global.html', stuff_for_frontend)




def aboutpage(request):
    return render(request, 'about.html')


def wikipage(request):
    return render(request, 'covid19Info.html')


def newspage(request):

    # news site
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()

    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date

    allnews_list = []
    for news in news_list:
        newstitle = news.title.text
        newslink = news.link.text
        newspubDate = news.pubDate.text

        allnews_list.append((newstitle, newslink, newspubDate))

    stuff_for_frontend = {
        'news_list': allnews_list

    }

    return render(request, 'news.html', stuff_for_frontend)
