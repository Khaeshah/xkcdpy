from flask import Flask, render_template
import xkcd, re
app = Flask(__name__)

@app.route('/')
def index():
    # At start we get the latest comic
    latestComic = xkcd.getLatestComic()
    # Parse the comic to HTML
    return parseComicHTML(latestComic)

@app.route('/<int:comicId>')
def show_post(comicId):

    # show the comic with the given id, the id is an integer
    comic = xkcd.getComic(comicId)

    # Parse the comic to HTML
    return parseComicHTML(comic, comicId)

@app.route('/random')
def randomComic():
    # show a random comic
    randomComic = xkcd.getRandomComic()
    return parseComicHTML(randomComic);

def parseComicHTML(comic, comicId = -1):
    try:
        title = comic.getTitle()
        imageUrl = comic.getImageLink()
        # Get the source url
        sourceUrl = comic.getExplanation().replace("explain", "")
        # Get the current comicId from sourceUrl using re
        if(comicId == -1):
            comicId = int(re.search(r'\d+',sourceUrl).group())

    except Exception as e:
        # If comic does not exist the latest is returned
        return parseComicHTML(xkcd.getLatestComic())
    return render_template('showComic.html',title = title, sourceUrl = sourceUrl, imageUrl = imageUrl, comicId = comicId)
