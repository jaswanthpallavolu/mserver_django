from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import ast
from fuzzywuzzy import fuzz
import random
from pathlib import Path
# import pickle

root = Path('.')
moviesPath = root / 'data'/'5kMovies.pkl'
# movietagsPath = root / 'data'/'movieTags.pkl'
movietagssubPath = root / 'data'/'movieTags_sub.pkl'
awardstagsPath = root / 'data'/'awardsTags.pkl'
movies = pd.read_pickle(moviesPath)
# categories = pd.read_pickle(movietagsPath)
categories_sub = pd.read_pickle(movietagssubPath)
awards = pd.read_pickle(awardstagsPath)
categories = pd.concat([categories_sub, awards], axis=0)

# Create your views here.

# getting movie info by passing movieId


@api_view(['GET'])
def movie(request, id):
    try:
        row = movies[movies['movieId'] == id]
        row = row.fillna('')
        x = row.to_dict(orient='records')[0]
        x["genre"] = ast.literal_eval(str(x["genre"]))
        x["actors"] = ast.literal_eval(x["actors"])
        x["directors"] = ast.literal_eval(x["directors"])
        return Response({"movieId": id, "details": x})
    except:
        return Response({"msg": "Invaild MovieId"})

# searching similar movies by passing title


@api_view(['GET'])
def search(request, name):
    # result = movies[movies['title'].apply(lambda x:fuzz.token_set_ratio(x.lower(),name.lower()) > 70)].head(20)['title']
    # result = sorted(result,key=lambda x:fuzz.token_set_ratio(x.lower(),name.lower()),reverse=True)
    # result = list(map(lambda x:movies[movies['title']==x].iloc[0]['movieId'],result))
    result = []

    def find(row):
        match = fuzz.token_set_ratio(row['title'].lower(), name.lower())
        if match >= 55:
            result.append([row['movieId'], match])

    movies.apply(find, axis=1)
    result = [i for i, j in sorted(result, key=lambda x: x[1], reverse=True)]

    return Response({'result': result[0:19], 'method': 'search'})


@api_view(['POST'])
def getGenreMovies(request):
    try:
        if (request.method == 'POST'):
            res = request.data
            category = res['genre']
            print(category)
            category_result = []

            result = movies[movies['genre'].apply(lambda x:[1 if i in x else 0 for i in category]
                                                  .count(1) == len(category))]\
                .sort_values(by=['imdbRating'], ascending=False).head(80)['movieId'].to_list()
            if len(result) <= 25:
                result = random.sample(result, len(result))
            else:
                result = random.sample(result, 25)
            category_result.append({'genre': category, 'result': result})
            return Response(category_result)
        else:
            return Response({'msg': 'no get request possible'})
    except:
        return Response({'msg': 'Invalid genres'})


# get movies by passing tags
@api_view(['GET'])
def listMoviesByTags(request, name):
    try:
        result = ast.literal_eval(
            categories[categories["tag"] == name.replace('+', ' ')]["movies"].values[0])
        if len(result) <= 25:
            result = random.sample(result, len(result))
        else:
            result = random.sample(result, 25)
        return Response({"tagname": name.replace('+', ' '), "movies": result})
    except:
        return Response({'msg': 'Tag name not found'})


# get tags by passing genres
@api_view(['GET', 'POST'])
def listTags(request):
    if (request.method == 'POST'):
        try:
            query = request.data["userHistory"]

            if len(list(query.keys())) > 5:
                query = dict(
                    sorted(query.items(), key=lambda x: x[1], reverse=True)[0:5])
            else:
                query = dict(
                    sorted(query.items(), key=lambda x: x[1], reverse=True))

            result_obj = {}
            priority_tags = []

            def reco_categories(x):
                matches = []
                genre = ast.literal_eval(x["genre"])
                for i in query:
                    if i in list(genre.keys())[0:3]:
                        matches.append(i)
                if len(matches) == 2 and matches == list(query.keys())[0:2]:
                    priority_tags.append(x["tag"])
                else:
                    if len(matches) in result_obj.keys():
                        result_obj[len(matches)].append(x["tag"])
                    else:
                        if matches != 0:
                            result_obj[len(matches)] = [x["tag"]]

            categories_sub.apply(reco_categories, axis=1)

            priority_tags = random.sample(
                priority_tags, len(priority_tags))[0:6]

            awards_list = awards["tag"].tolist()
            result = [] + priority_tags + random.sample(awards_list, 3)
            result = random.sample(result, len(result))

            for i in range(len(query), 1, -1):
                if i in list(result_obj.keys()):
                    if len(result_obj[i]) <= 20:
                        result = result + \
                            random.sample(result_obj[i], len(result_obj[i]))
                    else:
                        result = result + random.sample(result_obj[i], 20)

            return Response({'tagNames': result})
        except:
            return Response({'msg': 'Tags not found for post'})

    if (request.method == 'GET'):
        try:
            result = random.sample(awards['tag'].tolist(
            ), 3) + random.sample(categories_sub['tag'].tolist(), 25)
            return Response({'tagNames': random.sample(result, len(result))})
        except:
            return Response({'msg': 'Tags not found'})

# get movies by filters
@api_view(['POST'])
def filtering(request):
    if (request.method == 'POST'):
        try:
            query = request.data["query"]

            def filterMovies(query):
                result = movies[movies["genre"].apply(lambda x:all(i in ast.literal_eval(str(x)) for i in query["genre"])) & movies["imdbRating"].apply(lambda x:query["range"]<=x) & movies["year"].apply(lambda x:x<=query["released"])].sort_values(by=query["sort"][0],ascending=query["sort"][1]).head(200)
                total = len(result)
                result = result[(query["page"]-1)*query["nof"]:query["page"]*query["nof"]]["movieId"].tolist()
                return {"total_movies":total,"movies":result}

            return Response(filterMovies(query))
        except:
            return Response({'msg':'error on getting movies'})
