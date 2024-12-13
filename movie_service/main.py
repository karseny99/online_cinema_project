# from app.elastic_service.elastic_search import elastic_search
# import asyncio

# example_query = ElasticRequest(
#     contract_type=
#     title="Inception", 
#     year=None, 
#     genre=None, 
#     director="Christopher Nolan",
#     page=1,         
#     page_size=10   
# )

# search_query = {
#     "title": "Inception",
#     "year": 2010,
#     "genre": ["Sci-Fi"], # Also as select box   
#     "director": "Christopher Nolan", # Should be as selection in front
#     "page": 1,
#     "page_size": 10
# }

# incoming_message = BaseContractModel(
#     contract_type="search_request",
#     body={
#         "title": "Inception",
#         "year": 2010,
#         "genre": ["Action", "Sci-Fi"],
#         "director": "Christopher Nolan",
#         "page": 1,
#         "page_size": 10
#     }
# )


 

# if __name__ == "__main__":
#     asyncio.run(elastic_search(parse_search_request(incoming_message)))


from message_queue.rpc_client import *

if __name__ == "__main__":
    main()