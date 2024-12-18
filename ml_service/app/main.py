import service.ml as ml_service
import repository.movie_user_repo as repo

if __name__ == "__main__":
    recommendation_system = ml_service.MLRecomendation()

    repo.run_pipeline(recommendation_system)
