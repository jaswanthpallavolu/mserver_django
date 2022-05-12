from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import ast
from fuzzywuzzy import fuzz
import random
from pathlib import Path
# import pickle

root = Path('.')
moviesPath = root / 'data'/'5kMovies_12.05.pkl'
movietagssubPath = root / 'data'/'movieTags_12.05.pkl'
awardstagsPath = root / 'data'/'awardTags_12.05.pkl'
movies = pd.read_pickle(moviesPath)

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

# searching similar movies ,tags by passing title
@api_view(['GET'])
def search(request, name):
    # result = movies[movies['title'].apply(lambda x:fuzz.token_set_ratio(x.lower(),name.lower()) > 70)].head(20)['title']
    # result = sorted(result,key=lambda x:fuzz.token_set_ratio(x.lower(),name.lower()),reverse=True)
    # result = list(map(lambda x:movies[movies['title']==x].iloc[0]['movieId'],result))
    result = []
    result_tags = []

    def find(row):
        match = fuzz.token_set_ratio(row['title'].lower(), name.lower())
        if match >= 55:
            result.append([row['movieId'], match])

    def findTags(row):
        match = fuzz.token_set_ratio(row["tag"].lower(),name.lower())
        if match >= 50:
            result_tags.append([row["tag"],match])

    movies.apply(find, axis=1)
    categories.apply(findTags,axis=1)
    result = [i for i, j in sorted(result, key=lambda x: x[1], reverse=True)]
    result_tags = [i for i, j in sorted(result_tags, key=lambda x: x[1], reverse=True)]

    return Response({'movies': result[0:19], 'method': 'search','tags': result_tags[:20]})


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
        result = ast.literal_eval(str(categories[categories["tag"] ==
                                                 name.replace('+', ' ')]["movies"].values[0]))
        if len(result) <= 25:
            result = random.sample(result, len(result))
        else:
            result = random.sample(result, 25)
        return Response({"tagname": name.replace('+', ' '), "movies": result})
    except Exception as e:
        # print(e)
        return Response({'message': 'Tag not found', 'error': str(e)})

# complex computation
def filterCategories(query):
    result_obj = {}
    priority_tags = []

    def filterTags(x):
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
            elif len(matches) > 0:
                result_obj[len(matches)] = [x["tag"]]

    categories_sub.apply(filterTags, axis=1)

    return [result_obj, priority_tags]

# default tags list
def defaultTags():
    award_list = random.sample(awards['tag'].tolist(
    ), len(awards["tag"].tolist()))
    tags = random.sample(categories_sub['tag'].tolist(), 32)
    award_list_top = random.sample(
        award_list[:3]+tags[0:5], len(award_list[:3]+tags[0:5]))
    result = award_list_top + tags[5:] + award_list[3:]

    return Response({'tagNames': result})

# get tags by passing genres
@api_view(['GET', 'POST'])
def listTags(request):
    if (request.method == 'POST'):
        try:
            query = request.data["userHistory"]
            if (len(query.items()) < 3): return defaultTags()
            query = dict(
                sorted(query.items(), key=lambda x: x[1], reverse=True)[0:4])

            [result_obj, priority_tags] = filterCategories(query)

            priority_tags = random.sample(
                priority_tags, len(priority_tags))[0:3]

            awards_list = awards["tag"].tolist()
            result = [] + priority_tags + random.sample(awards_list, 3)
            result = random.sample(result, len(result))
            for i in range(len(query), 0, -1):
                if i in list(result_obj.keys()):
                    if len(result_obj[i]) <= (40 - len(result)):
                        result = result + \
                            random.sample(result_obj[i], len(result_obj[i]))
                    else:
                        result = result + random.sample(result_obj[i], (40 - len(result)))

            return Response({'tagNames': result})
        except Exception as e:
            return Response({'msg': 'Tags not found', 'error': str(e)})

    if (request.method == 'GET'):
        try:
            return defaultTags()
        except Exception as e:
            return Response({'msg': 'Tags not found', 'error': str(e)})

# get movies by filters
@api_view(['POST'])
def filtering(request):
    if (request.method == 'POST'):
        try:
            query = request.data["query"]

            def filterMovies(query):

                result = movies[movies["genre"].apply(lambda x:all(i in ast.literal_eval(str(x)) for i in query["genre"])) & movies["imdbRating"].apply(
                    lambda x:query["range"] <= x) & movies["year"].apply(lambda x:x <= query["released"])].sort_values(by=query["sort"][0], ascending=query["sort"][1])
                total = len(result)
                result = result[(query["page"]-1)*query["nof"]                                :query["page"]*query["nof"]]["movieId"].tolist()
                return {"total_movies": total, "movies": result}

            return Response(filterMovies(query))
        except:
            return Response({'msg': 'error on getting movies'})
