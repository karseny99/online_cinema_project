import service.ml as ml_service
import repository.movie_user_repo as repo

if __name__ == "__main__":
    recommendation_system = ml_service.MLRecomendation()

    '''
        репо слой предназначен для работы с базой данных, 
        а здесь вызывается основная логика с него

        Эта функция должна быть из сервиса и возвращать, 
        например, имя файла, куда было сохранено, и для сохранения вызывать репозитории
    '''
    repo.run_pipeline(recommendation_system)
