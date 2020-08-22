import json
import sys

from datetime import timedelta
from typing import Optional, Dict

import httpx
import redis

from fastapi import FastAPI, HTTPException

from .configuration import REDIS_CONFIGURATION, REDIS_LIFE_SPAN
from .utils import prepare_full_api_url
from .logger import logger


def connect_to_redis() -> Optional[redis.client.Redis]:
    """
    Standard function for connecting to Redis.

    Returns:
        Returns Redis client object.

    """

    try:
        client = redis.Redis(
            host=REDIS_CONFIGURATION["host"],
            port=REDIS_CONFIGURATION["port"],
            password=REDIS_CONFIGURATION["password"],
            socket_timeout=5,
        )

        # Check if connection is established.
        if client.ping() is True:
            return client

    except redis.AuthenticationError:
        logger.error(
            msg='Authentication Error occurred.',
        )
        sys.exit(1)


# Establish connection to Redis database.
redis_client = connect_to_redis()


def get_address_data_from_nominatim_api(
        query: str
) -> Optional[Dict]:
    """
    Function to get query data from the Nominatim API: https://nominatim.org/release-docs/develop/api.

    Args:
        query: Formatted string containing query data.

    Returns:
        Address data from the Nominatim API.

    """

    api_url = prepare_full_api_url(query)

    with httpx.Client() as client:
        response = client.get(api_url)
        response_data = response.json()

        if response_data:
            address_data = response_data[0].get('address')
            return address_data

        raise HTTPException(
            status_code=404,
            detail='No data found for this query. Please check if address query is correct.'
        )


def get_data_from_cache(
        query_key: str
) -> Optional[str]:
    """
    Function to retrieve data from the Redis, if key already exists.

    Args:
        query_key: Key which we want to get the value for.

    Returns:
        Address information for the query specified by the input key.

    """

    address_information = redis_client.get(query_key)

    return address_information


def set_data_to_cache(
        query_key: str,
        address_information: str
) -> bool:
    """
    Set the data to the Redis.

    Args:
        query_key: Key for the new entry.
        address_information: Value for the new entry.

    Returns:
        Boolean indicator if action was performed.

    """

    state = redis_client.setex(
        name=query_key,
        time=timedelta(**REDIS_LIFE_SPAN),
        value=address_information
    )

    return state


def get_query_data(
        query: str
) -> Dict:
    """
    Function to get the query data. Firstly function checks if the data is already cached. If not API call is made,
    data is cached and delivered.

    Args:
        query: Formatted string containing query data.

    Returns:
        Address data from the Nominatim API.

    """

    # Check if data is cached in Redis.
    data = get_data_from_cache(
        query_key=query
    )

    # If data is already cached, avoid making expensive API call and retrieve data from Redis.
    if data is not None:
        data = data.decode('utf-8')
        data = json.loads(data)

        # Add information that the data was cached before the call.
        data["cache"] = True
        return data

    # If data was not already cached, send a request to the Nominatim API.
    data = get_address_data_from_nominatim_api(
        query=query
    )

    # After getting the data from the API cached it to the Redis and serve it directly.
    if data:

        # Add information that the data was not cashed prior to the API call.
        data["cache"] = False

        data = json.dumps(
            obj=data,
            ensure_ascii=False
        )
        state = set_data_to_cache(
            query_key=query,
            address_information=data
        )

        if state is True:
            return json.loads(data)

    return data


app = FastAPI()


@app.get("/geolocate/address={address_string}")
def view(
        address_string: str
) -> Dict:
    """
    Wrapper for the data optimization API incorporating Redis caching.

    Args:
        address_string: Formatted string containing query data.

    Returns:
        Address data from the Nominatim API.

    """

    return get_query_data(
        query=address_string
    )
