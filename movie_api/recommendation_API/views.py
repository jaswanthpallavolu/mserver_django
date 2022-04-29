from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
# import pickle
from pathlib import Path

root = Path('.')
CBpath = root / 'data'/'CB_SimilarityMatrix.pkl'
CFpath = root / 'data'/'CF_SimilarityMatrix.pkl'
# cb_df = pd.DataFrame(pickle.load(open(path1, 'rb')))
# collab_df = pd.DataFrame(pickle.load(open(path2, 'rb')))
cb_df = pd.read_pickle(CBpath)
collab_df = pd.read_pickle(CFpath)


def getRelatedMovies(movieId, rating):
    # movieId = movie[0]
    # rate = movie[1]
    row = collab_df[movieId]*rating
    return row.sort_values(ascending=False)[1:11]


@api_view(['GET'])
def contentBased(request, movieId):
    try:
        ids = cb_df.index.tolist()
        if movieId not in ids:
            msg = 'id not found'
            result = []
        else:
            msg = 'content based'
            row = cb_df[movieId]
            result = row.sort_values(ascending=False)[1:11].index.tolist()

        return Response({'message': msg, 'result': result})
    except:
        return Response({'message': 'error', "result": []})


@api_view(['POST'])
def collaborativeFilter(request):
    try:
        data = request.data['movies']
        ids = collab_df.index.tolist()
        result = []
        if len(data) > 0:
            # existedIds = []
            # for movie in data:
            #     if (movie[0] in ids):
            #         existedIds.append(movie)
            similar_movies = pd.DataFrame()

            for movieId, rating in data:
                if movieId in ids:
                    similar_movies = pd.concat([similar_movies,
                                                getRelatedMovies(movieId, rating)], ignore_index=True, axis=1)

            movies = [i for i, j in data]
            similar_movies = similar_movies.sum(
                axis=1).sort_values(ascending=False)
            result = list(filter(lambda x: x not in movies,
                          similar_movies.index))[0:25]

        return Response({'message': 'collaborative filtering', "result": result})

    except:
        return Response({'message': 'error', "result": []})
