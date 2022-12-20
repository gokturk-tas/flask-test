from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import datetime
from justwatch import JustWatch

app = Flask(__name__)

providerDictionary = {}
userNameDictionary = []
passWordDictonary = []
userLoggedIn = False
finalResult = ''

def getSefaCalculatedGenreScore(longName):
    if longName=='Action and Adventure':
        return 7
    elif longName=='Comedy':
        return 12
    elif longName=='Documentary':
        return 10
    elif longName=='Fantasy':
        return 5
    elif longName=='Horror':
        return 4
    elif longName=='Music and Musical':
        return 3
    elif longName=='Romance':
        return 7
    elif longName=='Sport':
        return 1
    elif longName=='Western':
        return 1
    elif longName=='Animation':
        return 3
    elif longName=='Crime':
        return 5
    elif longName=='Drama':
        return 2
    elif longName=='History':
        return 2
    elif longName=='Kids and Family':
        return 6
    elif longName=='Mystery and Thriller':
        return 9
    elif longName=='Science-Fiction':
        return 3
    elif longName=='War and Military':
        return 1

def getShortNameOfCategory(longName):
    if longName=='Action and Adventure':
        return 'act'
    elif longName=='Comedy':
        return 'cmy'
    elif longName=='Documentary':
        return 'doc'
    elif longName=='Fantasy':
        return 'fnt'
    elif longName=='Horror':
        return 'hrr'
    elif longName=='Music and Musical':
        return 'msc'
    elif longName=='Romance':
        return 'rma'
    elif longName=='Sport':
        return 'spt'
    elif longName=='Western':
        return 'wsn'
    elif longName=='Animation':
        return 'ani'
    elif longName=='Crime':
        return 'crm'
    elif longName=='Drama':
        return 'drm'
    elif longName=='History':
        return 'hst'
    elif longName=='Kids and Family':
        return 'fml'
    elif longName=='Mystery and Thriller':
        return 'trl'
    elif longName=='Science-Fiction':
        return 'scf'
    elif longName=='War and Military':
        return 'war'

class UserSelectionData():
    topGenresList = []
    imdbWeight = 0
    priceWeight = 0
    contentAmountImportance = 0
    showImportance = 0
    movieImportance = 0

def generateUserSelectionData(topGenreList,imdb,price,contentAmount,showImportance, movieImportance):
    userSelectionData = UserSelectionData()
    userSelectionData.topGenresList = topGenreList
    userSelectionData.imdbWeight = imdb
    userSelectionData.priceWeight = price
    userSelectionData.contentAmountImportance = contentAmount
    userSelectionData.showImportance = showImportance
    userSelectionData.movieImportance = movieImportance
    return userSelectionData

class StreamingService(object):
    name = ""
    numberOfContentOnFirstCategory = 0
    numberOfContentOnSecondCategory = 0
    numberOfContentOnThirdCategory = 0
    imdbAverageScore = 0
    price = 0
    numberOfShows = 0
    numberOfMovies = 0
    totalScore = 0

    calculatedImdbScore = 0
    calculatedNumberOfContentScore = 0
    calculatedNumberOfMovieScore = 0
    calculatedNumberOfShowScore=0
    calculatedGenreScore=0


def generateStreamingService(name):
    service = StreamingService()
    service.name = name
    return service

def getLongNameOfStreamingPlatform(shortName):
    if shortName=='mbi':
        return 'Mubi'
    elif shortName=='qfs':
        return 'Quickflix Store'
    elif shortName=='tpl':
        return 'Tenplay'
    elif shortName=='msf':
        return 'Microsoft'
    elif shortName=='pls':
        return 'Playstation'
    elif shortName=='ply':
        return 'Google Play Store'
    elif shortName=='itu':
        return 'iTunes'
    elif shortName=='ddi':
        return 'Dendy Direct'
    elif shortName=='crk':
        return 'Crackle'
    elif shortName=='stn':
        return 'Stan'
    elif shortName=='prs':
        return 'Preste'
    elif shortName=='nfx':
        return 'Netflix'
    elif shortName=='dnp':
        return 'Disney Plus'
    elif shortName=='prv':
        return 'Amazon Prime Video'
    elif shortName=='blv':
        return 'BluTv'
    elif shortName=='exn':
        return 'Exen'
    elif shortName=='qfx':
        return 'Quickflix'

def getTotalContentCount(userInput:UserSelectionData, service:StreamingService):
    returnValue = []
    just_watch = JustWatch()
    results = just_watch.search_for_item(genres=[getShortNameOfCategory(userInput.topGenresList[0])],
                                         providers=[service.name])
    returnValue.append(results.get('total_results',0))

    results = just_watch.search_for_item(genres=[getShortNameOfCategory(userInput.topGenresList[1])],
                                         providers=[service.name])
    returnValue.append(results.get('total_results',0))

    results = just_watch.search_for_item(genres=[getShortNameOfCategory(userInput.topGenresList[2])],
                                         providers=[service.name])
    returnValue.append(results.get('total_results',0))
    return returnValue

def getNumberOfShowAndMovie(userInput:UserSelectionData, service:StreamingService):
    just_watch = JustWatch()
    returnValue = []
    showCount = just_watch.search_for_item(genres=[getShortNameOfCategory(userInput.topGenresList[0]),getShortNameOfCategory(userInput.topGenresList[1]),getShortNameOfCategory(userInput.topGenresList[2])],
                                         providers=[service.name],
                                         content_types=['show'])
    movieCount = just_watch.search_for_item(genres=[getShortNameOfCategory(userInput.topGenresList[0]),getShortNameOfCategory(userInput.topGenresList[1]),getShortNameOfCategory(userInput.topGenresList[2])],
                                         providers=[service.name],
                                         content_types=['movie'])
    returnValue.append(showCount.get('total_results',0))
    returnValue.append(movieCount.get('total_results',0))
    return returnValue

def getAverageImbdbScoreOfContent(userInput:UserSelectionData, service:StreamingService):
    just_watch = JustWatch()
    totalScore = 0
    totalCount = 0
    results = just_watch.search_for_item(page_size=100,
                                         providers=[service.name],
                                         genres=[getShortNameOfCategory(userInput.topGenresList[0])])

    for z in range(len(results.get('items',0))):
        scoringList = results.get('items')[z].get('scoring')
        for i in scoringList:
            if i.get('provider_type','')=='imdb:score':
                totalScore+=(i.get('value',0))
                break
    totalCount += len(results.get('items',0))


    results = just_watch.search_for_item(page_size=100,
                                         providers=[service.name],
                                         genres=[getShortNameOfCategory(userInput.topGenresList[1])])

    for z in range(len(results.get('items',0))):
        scoringList = results.get('items')[z].get('scoring')
        for i in scoringList:
            if i.get('provider_type','')=='imdb:score':
                totalScore+=(i.get('value',0))
                break
    totalCount += len(results.get('items',0))


    results = just_watch.search_for_item(page_size=100,
                                         providers=[service.name],
                                         genres=[getShortNameOfCategory(userInput.topGenresList[2])])

    for z in range(len(results.get('items',0))):
        scoringList = results.get('items')[z].get('scoring')
        for i in scoringList:
            if i.get('provider_type','')=='imdb:score':
                totalScore+=(i.get('value',0))
                break
    totalCount += len(results.get('items',0))


    if(totalCount==0):
        return 0
    else:
        return (totalScore/totalCount)


def fillUserInputDataToSystem(request):
    topGenres = []
    topGenres.append(request.form['dropdown1'])
    topGenres.append(request.form['dropdown2'])
    topGenres.append(request.form['dropdown3'])
    return generateUserSelectionData(topGenres,int(request.form['imdb']),int(request.form['price']),int(request.form['content_amount']),int(request.form['show']),int(request.form['movie']))

providersNameList = {'mbi','nfx','dnp','prv','itu'}

@app.route('/', methods=['POST', 'GET'])
def index():
    global userLoggedIn
    global finalResult
    if request.method == 'POST':
        userData = fillUserInputDataToSystem(request)
        startApiService(userData)
        calculateScoreForEachService(userData)
        bestProvider = generateStreamingService('test')
        secondBestProvider = generateStreamingService('test2')
        thirdBestProvider = generateStreamingService('test3')
        fourthBestProvider = generateStreamingService('test4')
        fifthBestProvider = generateStreamingService('test5')

        prov_lst = list(providerDictionary.items())
        prov_lst.sort(key=lambda x: x[1].totalScore)
        bestProvider = prov_lst[0][1]
        secondBestProvider = prov_lst[1][1]
        thirdBestProvider = prov_lst[2][1]
        fourthBestProvider = prov_lst[3][1]
        fifthBestProvider = prov_lst[4][1]

            
        bestName = getLongNameOfStreamingPlatform(bestProvider.name)
        bestImdbScore = str(bestProvider.calculatedImdbScore)
        bestNumberOfContentScore = str(bestProvider.calculatedNumberOfContentScore)
        bestNumberOfMovieScore = str(bestProvider.calculatedNumberOfMovieScore)
        bestNumberOfShowScore = str(bestProvider.calculatedNumberOfShowScore)
        bestGenreScore = str(bestProvider.calculatedGenreScore)
        bestTotalScore = str(bestProvider.totalScore)
        
        secondName = getLongNameOfStreamingPlatform(secondBestProvider.name)
        secondImdbScore = str(secondBestProvider.calculatedImdbScore)
        secondNumberOfContentScore = str(secondBestProvider.calculatedNumberOfContentScore)
        secondNumberOfMovieScore = str(secondBestProvider.calculatedNumberOfMovieScore)
        secondNumberOfShowScore = str(secondBestProvider.calculatedNumberOfShowScore)
        secondGenreScore = str(secondBestProvider.calculatedGenreScore)
        secondTotalScore = str(secondBestProvider.totalScore)

        thirdName = getLongNameOfStreamingPlatform(thirdBestProvider.name)
        thirdImdbScore = str(thirdBestProvider.calculatedImdbScore)
        thirdNumberOfContentScore = str(thirdBestProvider.calculatedNumberOfContentScore)
        thirdNumberOfMovieScore = str(thirdBestProvider.calculatedNumberOfMovieScore)
        thirdNumberOfShowScore = str(thirdBestProvider.calculatedNumberOfShowScore)
        thirdGenreScore = str(thirdBestProvider.calculatedGenreScore)
        thirdTotalScore = str(thirdBestProvider.totalScore)

        fourthName = getLongNameOfStreamingPlatform(fourthBestProvider.name)
        fourthImdbScore = str(fourthBestProvider.calculatedImdbScore)
        fourthNumberOfContentScore = str(fourthBestProvider.calculatedNumberOfContentScore)
        fourthNumberOfMovieScore = str(fourthBestProvider.calculatedNumberOfMovieScore)
        fourthNumberOfShowScore = str(fourthBestProvider.calculatedNumberOfShowScore)
        fourthGenreScore = str(fourthBestProvider.calculatedGenreScore)
        fourthTotalScore = str(fourthBestProvider.totalScore)

        fifthName = getLongNameOfStreamingPlatform(fifthBestProvider.name)
        fifthImdbScore = str(fifthBestProvider.calculatedImdbScore)
        fifthNumberOfContentScore = str(fifthBestProvider.calculatedNumberOfContentScore)
        fifthNumberOfMovieScore = str(fifthBestProvider.calculatedNumberOfMovieScore)
        fifthNumberOfShowScore = str(fifthBestProvider.calculatedNumberOfShowScore)
        fifthGenreScore = str(fifthBestProvider.calculatedGenreScore)
        fifthTotalScore = str(fifthBestProvider.totalScore)

        return render_template('result.html',bestName=bestName,bestImdbScore=bestImdbScore,bestNumberOfContentScore=bestNumberOfContentScore,\
            bestNumberOfMovieScore=bestNumberOfMovieScore,\
            bestNumberOfShowScore=bestNumberOfShowScore,bestTotalScore=bestTotalScore,bestGenreScore=bestGenreScore,\
            secondName=secondName,secondImdbScore=secondImdbScore,\
            secondNumberOfContentScore=secondNumberOfContentScore,secondNumberOfMovieScore=secondNumberOfMovieScore,\
            secondNumberOfShowScore=secondNumberOfShowScore,secondTotalScore=secondTotalScore,secondGenreScore=secondGenreScore,\
            thirdName=thirdName,thirdImdbScore=thirdImdbScore,thirdNumberOfContentScore=thirdNumberOfContentScore,\
            thirdNumberOfMovieScore=thirdNumberOfMovieScore,\
            thirdNumberOfShowScore=thirdNumberOfShowScore,thirdTotalScore=thirdTotalScore,thirdGenreScore=thirdGenreScore,\
            fourthName=fourthName,fourthImdbScore=fourthImdbScore,\
            fourthNumberOfContentScore=fourthNumberOfContentScore,fourthNumberOfMovieScore=fourthNumberOfMovieScore,\
            fourthNumberOfShowScore=fourthNumberOfShowScore,fourthTotalScore=fourthTotalScore,fourthGenreScore=fourthGenreScore,\
            fifthName=fifthName,fifthImdbScore=fifthImdbScore,\
            fifthNumberOfContentScore=fifthNumberOfContentScore,fifthNumberOfMovieScore=fifthNumberOfMovieScore,\
            fifthNumberOfShowScore=fifthNumberOfShowScore,fifthTotalScore=fifthTotalScore,fifthGenreScore=fifthGenreScore)
    else:
        if userLoggedIn:
            return render_template('query.html')
        else:
            return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userNameDictionary.append(username)
        passWordDictonary.append(password)
        global userLoggedIn
        global finalResult
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global userLoggedIn
    global finalResult
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(userNameDictionary.count(username)>0):
            userNameDictionary.index(username)
            if(passWordDictonary[userNameDictionary.index(username)]==password):
                userLoggedIn = True
                
    
    if userLoggedIn:
        return render_template('query.html')
    else:
        flash('Wrong ID or password')
        return render_template('login.html')

@app.route('/return', methods=['GET', 'POST'])
def registerToMainPage():
    if request.method == 'POST':
        global userLoggedIn
        global finalResult
        return render_template('index.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global userLoggedIn
    global finalResult
    userLoggedIn = False
    return render_template('login.html')

@app.route('/gotologin', methods=['GET', 'POST'])
def gotologin():
    if request.method == 'POST':
        global userLoggedIn
        global finalResult
        if(userLoggedIn):
            return render_template('query.html')
        else:
            return render_template('login.html')

@app.route('/hreflogout', methods=['GET', 'POST'])
def hreflogout():
    logout()

@app.route('/hrefhome', methods=['GET', 'POST'])
def hrefhome():
    return render_template('index.html')

@app.route('/hrefaboutus', methods=['GET', 'POST'])
def hrefaboutus():
    return render_template('aboutus.html')

@app.route('/hreftool', methods=['GET', 'POST'])
def hreftool():
    if(userLoggedIn):
        return render_template('query.html')
    else:
        return render_template('index.html')

@app.route('/hrefplatforms', methods=['GET', 'POST'])
def hrefplatforms():
    return render_template('hrefplatforms.html')

@app.route('/hrefcontact', methods=['GET', 'POST'])
def hrefcontact():
    return render_template('contactus.html')

@app.route('/gotoregister', methods=['GET', 'POST'])
def gotoregister():
    if request.method == 'POST':
        global userLoggedIn
        global finalResult
        if(userLoggedIn):
            return render_template('query.html')
        else:
            return render_template('register.html')


def startApiService(userData:UserSelectionData):
    for provider in providersNameList:
       
        totalContentCountList = getTotalContentCount(userData,providerDictionary[provider])
        showMovieCount = getNumberOfShowAndMovie(userData, providerDictionary[provider])
        averageImdbScoreOfContent = getAverageImbdbScoreOfContent(userData,providerDictionary[provider])
        service = providerDictionary[provider]
        service.numberOfContentOnFirstCategory = totalContentCountList[0]
        service.numberOfContentOnSecondCategory = totalContentCountList[1]
        service.numberOfContentOnThirdCategory = totalContentCountList[2]
        service.numberOfShows = showMovieCount[0]
        service.numberOfMovies = showMovieCount[1]
        service.imdbAverageScore = averageImdbScoreOfContent
        providerDictionary[provider] = service
        
    

def fillDictionaryData():
    for provider in providersNameList:
        providerDictionary[provider] = generateStreamingService(provider)

def calculateScoreForEachService(userInput:UserSelectionData):
    firstCategoryScorePerContent = 3
    secondCategoryScorePerContent = 2
    thirdCategoryScorePerContent = 1
    showScore = 1
    movieScore = 1
    imdbScore = 5

    for provider in providersNameList:
        service = providerDictionary[provider]
        service.calculatedNumberOfContentScore = 0
        service.calculatedGenreScore = 0
        service.calculatedImdbScore = int(service.imdbAverageScore*userInput.imdbWeight*imdbScore)
        service.calculatedNumberOfContentScore += int(service.numberOfContentOnFirstCategory*firstCategoryScorePerContent)
        service.calculatedNumberOfContentScore += int(service.numberOfContentOnSecondCategory*secondCategoryScorePerContent)
        service.calculatedNumberOfContentScore += int(service.numberOfContentOnThirdCategory*thirdCategoryScorePerContent)
        service.calculatedNumberOfMovieScore = int(service.numberOfMovies*userInput.movieImportance*movieScore)
        service.calculatedNumberOfShowScore = int(service.numberOfShows*userInput.showImportance*showScore)

        service.calculatedGenreScore += int(service.numberOfContentOnFirstCategory*getSefaCalculatedGenreScore(userInput.topGenresList[0]))
        service.calculatedGenreScore += int(service.numberOfContentOnSecondCategory*getSefaCalculatedGenreScore(userInput.topGenresList[1]))
        service.calculatedGenreScore += int(service.numberOfContentOnThirdCategory*getSefaCalculatedGenreScore(userInput.topGenresList[2]))

        service.totalScore = service.calculatedGenreScore+service.calculatedImdbScore+service.calculatedNumberOfContentScore+service.calculatedNumberOfMovieScore+service.calculatedNumberOfShowScore        
        providerDictionary[provider] = service

if __name__ == "__main__":
    fillDictionaryData() # generates key value pairs for every streaming service and gives them a score of 0
    app.secret_key = 'the random string'
    app.run(debug=True)
    