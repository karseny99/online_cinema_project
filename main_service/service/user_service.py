import logging
import time

from rpc_client.rpc_client import get_user_rpc_client
from models.models import BaseContractModel
from models.user_service_models import SetMovieRatingRequest, SetMovieRatingResponse

log = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.user_rpc = get_user_rpc_client()

    def set_movie_rating(self, req: SetMovieRatingRequest) -> SetMovieRatingResponse:
        request = BaseContractModel(
            contract_type="set_rating_request",
            body=req
        )
        response = self.user_rpc.call(request)

        if response is None:
            log.error(f"RESPONSE IS NONE")
            return SetMovieRatingResponse(movie_id=-1, user_id=-1, success=False)

        elif response.contract_type == "set_rating_response":
            log.debug(f" [.] Got {response}")
            return response.body
#

def main():
    user_rpc = get_user_rpc_client()

    set_rating = SetMovieRatingRequest(
        movie_id=7,
        user_id=15,
        rating=4.0
    )
    req = BaseContractModel(
        contract_type="set_rating_request",
        body=set_rating
    )

    while True:
        set_rating.rating += 0.1
        print(f" [x] Requesting set_rating({set_rating})")
        response = user_rpc.call(req)
        if response is not None:
            if response.contract_type == "set_rating_response":
                print(f" [.] Got {response}")
            if response.contract_type == "":
                print(f"Kak eto: {response}")
        else:
            print(" [.] No response received.")
        time.sleep(1)  # Задержка перед следующим запросом

if __name__ == "__main__":
    main()