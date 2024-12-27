import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from app.repository.repository import get_ratings_in_batches, get_unique_movies, update_database_recommendations, get_rated_movies
import os
from surprise import Reader, Dataset
from surprise import SVDpp
from joblib import dump, load
from collections import defaultdict
from datetime import datetime
import glob
import json
import ast


class MLRecommendation:
    def __init__(self, model_path: str = None):
        '''
            Инициализация модели
        '''
        self.svd_model = None
        self.load_batch_size = None
        self.fit_batch_size = None
        self.unique_movies = None

        if model_path == None:
            if not self.load_last_model():
                raise FileNotFoundError("File not found: Cannot load last model")
        elif not self.load_model(model_path):
            raise FileNotFoundError("File not found: Cannot load model")
        

    def update_model(self):
        '''
            Обучение новой модели батчами
        '''
        self.svd_model = SVDpp(n_factors=400, lr_all=0.006, n_epochs=20, verbose=True)
        self.batch_size = 10000
        self.fit_batch_size = 1000400 
        self.unique_movies = get_unique_movies()

        data = self.load_data()
        n_batches = len(data) // self.batch_size + 1 

        for i in range(n_batches):
            batch = data[i * self.fit_batch_size: (i + 1) * self.fit_batch_size]
            self.fit(batch)


    def fit(self, data):
        '''
            По данным делается fit в модель
        '''
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(data[["user_id", "movie_id", "rating"]], reader)
        trainset = data.build_full_trainset()

        self.svd_model.fit(trainset)


    def update_recommendations(self, users_list):
        '''
            Обновление рекомендаций для данного user списка в бд
        '''
        reader = Reader(rating_scale=(1, 5))
        data = self.load_data()
        dataset = Dataset.load_from_df(data, reader)
        full_trainset = dataset.build_full_trainset()

        batch_size = 1000 
        all_items = full_trainset.all_items()
        with open('temp.csv', 'a') as f:
            f.write('user_id,movie_ids\n')
            for user_inner_id in full_trainset.all_users():
                
                user_id = full_trainset.to_raw_uid(user_inner_id)

                rated_items = full_trainset.ur[user_inner_id] 
                rated_movie_ids = [full_trainset.to_raw_iid(movie_id) for movie_id, _ in rated_items]
                
                unobserved_items = [movie_id for movie_id in all_items if full_trainset.knows_item(movie_id) and full_trainset.to_raw_iid(movie_id) not in rated_movie_ids]
                
                anti_testset = [(user_id, movie_id, None) for movie_id in unobserved_items]
                
                predictions = self.svd_model.test(anti_testset)
                
                top_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:100]
                movie_ids = [pred[1] for pred in top_predictions]
                f.write(f'{user_id}, {str(movie_ids)}\n')

        self.update_recommendations_from_csv('temp.csv')

        # rated_movies = get_rated_movies(user_list=users_list)
        # users_recommendations = []
        # for user_id in users_list:
        #     user_recommendations = []
        #     for movie_id in self.unique_movies:
        #         if movie_id in rated_movies:
        #             continue

        #         predicted_rating = self.svd_model.predict(user_id, movie_id).est
        #         user_recommendations.append((movie_id, predicted_rating))

        #     user_recommendations.sort(key=lambda x: x[1], reverse=True)

        #     movie_ids = [rec[0] for rec in user_recommendations[:100]]
        #     users_recommendations.append((user_id, movie_ids))

        # update_database_recommendations(new_data=users_recommendations)


    def update_recommendations_from_csv(self, path: str):
        '''
            Обновление рекомендаций из csv файла
        '''

        data = pd.read_csv(path, sep='|')

        def convert_to_list(x):
            return list(map(int, x.split(',')))

        # Применяем функцию к столбцу 'movie_ids'
        data['movie_ids'] = data['movie_ids'].apply(convert_to_list)
        # print(data[['user_id', 'movie_ids']].values.tolist())
        # print(data.columns)

        print("Uploaded df")
        update_database_recommendations(new_data=data[['user_id', 'movie_ids']].values.tolist())



    def save_model(self) -> None:
        '''
            Сохранение модели
        '''

        filename = f"ml_models/svd_model{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        dump(self.svd_model, f'{filename}.pkl')

        params = {
            'load_batch_size': self.load_batch_size,
            'fit_batch_size': self.fit_batch_size,
            'unique_movies': self.unique_movies
        }
    
        with open(f'{filename}.json', 'w') as json_file:
            json.dump(params, json_file)


    def load_last_model(self) -> bool:
        '''
            Загрузка последнего файла модели c параметрами
        '''
        files = glob.glob('ml_models/svd_model*.pkl')
        if files:
            latest_file = sorted(files, key=lambda x: os.path.getmtime(x))[-1]
            self.svd_model = load(latest_file)

            param_file = f"{os.path.splitext(latest_file)[0]}.json"
            if os.path.exists(param_file):
                with open(param_file, 'r') as json_file:
                    params = json.load(json_file)
                    self.load_batch_size, self.fit_batch_size, self.unique_movies = params['load_batch_size'], params['fit_batch_size'], params['unique_movies']
            else:
                raise FileNotFoundError(f"Error: Cannot find param file {param_file}")

        return self.svd_model != None


    def load_model(self, path: str) -> bool:
        '''
            Загрузка модели (true/false была ли модель локально найдена c параметрами)
        '''
        if not os.path.isfile(path):
            return False
        else:
            self.svd_model = load(path)

            param_file = f"{os.path.splitext(path)[0]}.json"
            if os.path.exists(param_file):
                with open(param_file, 'r') as json_file:
                    params = json.load(json_file)
                    self.load_batch_size, self.fit_batch_size, self.unique_movies = params['load_batch_size'], params['fit_batch_size'], params['unique_movies']
            else:
                raise FileNotFoundError(f"Error: Cannot find param file {param_file}")

            return True


    def load_data(self, save_path = "ratings.csv") -> pd.DataFrame:
        '''
            Вызывает репо слой для загрузки всех нужных данных
            10 min execution time
        '''
        
        get_ratings_in_batches(batch_size=self.batch_size, save_path="ratings.csv")
        
        data = pd.read_csv(save_path)
        data.drop(columns=['rating_id', 'rated_at'], inplace=True)
        data.reset_index(drop=True, inplace=True)

        return data
