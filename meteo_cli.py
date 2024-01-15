import requests
import base64
import click

def get_temperature(date, parameters, location, username, password):
    """
    Fetches weather data from the Meteomatics API based on the given parameters.

    Args:
        date (str): The date or date range for which to retrieve weather data.
                    Format should be 'YYYY-MM-DDTHH:MM:SSZ' time step: PT1H - time step (1 hour)
                    for a single date or 'start_date--end_date' for a range.
        parameters (str): The type of weather data to retrieve (e.g., t_<level>:<unit> ('t_2m:C') for temperature,
                          relative_humidity_<level>:<unit> (relative_humidity_2m:p) for 'humidity' etc check the meteomatics documentation).
        location (str): The geographical coordinates (latitude and longitude) for which to retrieve
                        the weather data. The format should be 'latitude, longitude'.
        username (str): Username for Meteomatics API access.
        password (str): Password for Meteomatics API access.

    Returns:
        dict: A dictionary containing the requested weather data if the request is successful.
              Returns None if the request fails.

    Example:
        >>> get_temperature("2024-01-15T00:00:00Z--2024-01-18T00:00:00Z:PT1H", "t_2m:C", "52.520551,13.461804", "username", "password")
    """
    # Construct the URL based on the input parameters
    url = f"https://api.meteomatics.com/{date}/{parameters}/{location}/json"

    # Encode the credentials
    credentials = base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}'
    }

    # Make the request
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()

        # Extracting and printing temperature data
        for item in data['data']:
            coordinates = item['coordinates']
            for coord in coordinates:
                dates = coord['dates']
                for date_info in dates:
                    date = date_info['date']
                    temperature = date_info['value']
                    print(f"Date: {date}, Temperature: {temperature}°C")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")


@click.command()
@click.argument('date', type=click.STRING)
@click.argument('parameters', type=click.STRING)
@click.argument('location', type=click.STRING)
@click.argument('username', type=click.STRING)
@click.argument('password', type=click.STRING)
def get_weather_data(date, parameters, location, username, password):
    """
    Fetches weather data from the Meteomatics API based on the given parameters.
    """
    try:
        url = f"https://api.meteomatics.com/{date}/{parameters}/{location}/json"
        credentials = base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            temperature_data = {}
            precipitation_data = {}
            humidity_data = {}

            for item in data['data']:
                parameter = item['parameter']
                for coord in item['coordinates']:
                    for date_info in coord['dates']:
                        date = date_info['date']
                        value = date_info['value']
                        if parameter == 't_2m:C':
                            temperature_data[date] = value
                        elif parameter == 'precip_1h:mm':
                            precipitation_data[date] = value
                        elif parameter == 'relative_humidity_2m:pct':
                            humidity_data[date] = value 

            click.echo("Temperature Data:")
            for date, temp in temperature_data.items():
                click.echo(f"Date: {date}, Temperature: {temp}°C")

            click.echo("\nPrecipitation Data:")
            for date, precip in precipitation_data.items():
                click.echo(f"Date: {date}, Precipitation: {precip}mm")

            click.echo("\nRelative Humidity Data:")
            for date, humidity in humidity_data.items():
                click.echo(f"Date: {date}, Relative Humidity: {humidity}%")

        else:
            click.echo(f"Error: Unable to fetch data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        click.echo(f"Request failed: {e}")

if __name__ == "__main__":
    get_weather_data()

#def main():
    # Example usage
#    date = "2024-01-15T00:00:00Z--2024-01-18T00:00:00Z:PT1H"
#    parameters = "t_2m:C,precip_1h:mm"
#    location = "52.520551,13.461804"
#    username = "atkins_ejenam_enemchukwu"
#    password = "f8EchDB8u8"
    
#    get_weather_data(date, parameters, location, username, password)

#if __name__ == '__main__':
#    main()
