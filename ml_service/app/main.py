import service.ml as ml_service

if __name__ == "__main__":
    recommendation_system = ml_service.MLRecomendation()

    relevance_matrix = recommendation_system.run_recommendation_pipeline()

    relevance_matrix.to_csv("relevance_matrix.csv", index=True) # сохранение файла
    # print(relevance_matrix.head())