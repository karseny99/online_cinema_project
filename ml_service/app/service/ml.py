import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from repository.movie_user_repo import get_ratings, get_movies


class MLRecommendation:

    # https://github.com/rcz7795/Movie-Recommendation-System/blob/main/Movie_Recommendation_System.ipynb
    # Тут буквально есть всё на требуемом уровне

    def __init__(self):
        '''
            Здесь инициализация бустинга (xgboost | catboost) решайте сами
            вызывается load_model

            Первое: проверка, можно ли вгрузить веса или как-то 
            загрузить локально сохраненную модель. 
            Реализовать вгрузку локальных данных без обработки датафрейма. 
            
            Если нельзя:
            сюда нужно вынести загрузку этих 20 млн рейтингов
            с вызовом обработки данных.
            Можно либо загружать с нуля всё здесь, 
            либо использовать метод fit и в него кидать батчи
            (То есть в data будет, например, информация по 1000 человек)
            Но, подозреваю, будет больно с обработкой данных, потому что 
            data_processing работает на всем датасете вроде как
        '''
        pass

    def prepare_data(self):
        pass

    def fit(self, data: list[your_type]):
        '''
            Функция нужна для дообучения
            data - это список, в котором элемент - это информация об оценках пользователей,
            как выглядит эта информация вы решаете сами 
            (она должна еще и совпадать с тем, что получится после data_preparation)
        '''
        # for user in data:
        #     model.fit(user)

    def predict_for_user(self, user_id: int) -> list:
        '''
            Посмотреть можно ли сделать предикт только для одного юзера 
            без подсчета всей матрицы
            Возврат list[movie_id]
        '''
        pass

    def predict_relevance_matrix(self):
        '''
            Подсчет всей матрицы
        '''
        pass

    def save_model(self, path: str) -> None:
        '''
            Примерно так
            from catboost import CatBoostClassifier

            # Создание и обучение модели
            model = CatBoostClassifier(iterations=100, depth=3, learning_rate=0.1, loss_function='Logloss')
            model.fit(X_train, y_train)

            # Сохранение модели
            model.save_model('catboost_model.cbm')

        '''
        pass
    
    def save_model_mlflow(self):
        '''
            Сохранить модель в MLflow (пока не надо)
        '''
        weights = self.get_model_weights()
        pass

    def load_model(self, path: str) -> None:
        '''
            Загрузить модель 
            Пример
            from catboost import CatBoostClassifier

            # Создание экземпляра модели
            model = CatBoostClassifier()

            # Загрузка модели
            model.load_model('catboost_model.cbm')

        '''
        pass


class MLRecomendation:
    def __init__(self):
        # Параметры для инициализации
        self.knn_model = None
        self.user_item_matrix = None
        self.csr_data = None

    def prepare_data(self, ratings_path: str, movies_path: str) -> None:
        """
        Подготавливает данные для модели.
        """
        ratings = get_ratings(ratings_path)
        movies = get_movies(movies_path)

        # Создание матрицы пользователь-фильм
        self.user_item_matrix = ratings.pivot(index='movie_id', columns='user_id', values='rating')
        self.user_item_matrix.fillna(0, inplace = True)

        # Отфильтровываем фильмы и пользователей с малым количеством оценок
        users_votes = ratings.groupby('user_id')['rating'].count()
        movies_votes = ratings.groupby('movie_id')['rating'].count()
        user_mask = users_votes[users_votes > 50].index
        movie_mask = movies_votes[movies_votes > 10].index

        self.user_item_matrix = self.user_item_matrix.loc[movie_mask, :]
        self.user_item_matrix = self.user_item_matrix.loc[:, user_mask]

        # Преобразование разреженной матрицы
        self.csr_data = csr_matrix(self.user_item_matrix.values)
        self.user_item_matrix = self.user_item_matrix.rename_axis(None, axis = 1).reset_index()

    def train_knn(self) -> None:
        """
        Обучает модель kNN.
        """
        self.knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        self.knn_model.fit(self.csr_data)

    def predict_relevance_matrix(self) -> pd.DataFrame:
        """
        Создает матрицу предсказаний релевантности.
        """
        user_ids = self.user_item_matrix.columns
        movie_ids = self.user_item_matrix.index

        relevance_matrix = pd.DataFrame(0, index=user_ids, columns=movie_ids, dtype=float)

        for movie_index, row in enumerate(self.user_item_matrix.itertuples(index=False)):
            distances, indices = self.knn_model.kneighbors(self.csr_data[movie_index], n_neighbors=20)

            for user_index, distance in zip(indices.flatten(), distances.flatten()):
                if user_index >= len(user_ids):
                    continue
                user_id = user_ids[user_index]
                movie_id = movie_ids[movie_index]
                relevance_matrix.loc[user_id, movie_id] = (1 - distance) * 5

        return relevance_matrix

    def run_recommendation_pipeline(self) -> pd.DataFrame:
        """
        Полный цикл работы рекомендательной системы.
        """
        # Пути к данным
        ratings_path ="~/rating.csv"
        movies_path ="~/movie.csv"

        # print("получили пути")

        # Подготовка данных
        self.prepare_data(ratings_path, movies_path)

        # print("подготовили данные")

        # Обучение модели
        self.train_knn()

        # print("обучили модель")

        # Предсказание матрицы релевантности
        relevance_matrix = self.predict_relevance_matrix()
        # print("матрица создана")
        return relevance_matrix
