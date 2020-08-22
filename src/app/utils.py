from .configuration import BASE_URL, NOMINATIM_API_CONFIGURATION


def prepare_full_api_url(
        address: str
) -> str:
    """
    Function to create full url used in getting data from the Nominatim API.

    Args:
        address: Formatted string containing query data.

    Returns:
        Full url for the query data.
    """

    # Prepare string containing configuration data.
    configuration_string = '&'.join([
        f'{parameter}={parameter_value}'
        for parameter, parameter_value
        in NOMINATIM_API_CONFIGURATION.items()
    ])

    # Concatenate base url, address query and configuration string into full url needed for the API.
    full_api_url = f'{BASE_URL}{address}&{configuration_string}'

    return full_api_url
