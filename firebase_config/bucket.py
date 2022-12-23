from firebase_config.firebase import bucket
from pathlib import Path
import os
import pickle as pkl

root = Path('.')

files = ['5kMovies_11.06.pkl', 'awardTags_11.06.pkl',
         'CB_SimilarityMatrix_14.05.pkl', 'CF_SimilarityMatrix.pkl', 'movieTags_11.06.pkl']


def downloadPickleFiles():
    try:
        for name in files:
            filePath = root / 'data' / name
            isExits = os.path.exists(filePath)
            if (isExits == False):
                blob = bucket.blob(name)
                blob.download_to_filename(filePath)
                print(blob)

    except Exception as e:
        print("error:", str(e))
