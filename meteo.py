import requests
import base64
import click

def get_weather_data(date, parameters, location, username, password):
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
    """

    # Adjust the URL to include the relative humidity parameter
    url = f"https://api.meteomatics.com/{date}/{parameters}/{location}/json"
    credentials = base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}'
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()

        # Initialize dictionaries to store the data
        temperature_data = {}
        precipitation_data = {}
        humidity_data = {}

        for item in data['data']:
            parameter = item['parameter']
            for coord in item['coordinates']:
                for date_info in coord['dates']:
                    date = date_info['date']
                    value = date_info['value']
                    if parameter == 't_2m:C': # Adjust this key based on the actual parameter name ie the level
                        temperature_data[date] = value
                    elif parameter == 'precip_1h:mm': # Adjust this key based on the actual parameter name ie the level
                        precipitation_data[date] = value
                    elif parameter == 'relative_humidity_2m:pct':  # Adjust this key based on the actual parameter name ie the level
                        humidity_data[date] = value 
                    

        # Print the collected data
        print("Temperature Data:")
        for date, temp in temperature_data.items():
            print(f"Date: {date}, Temperature: {temp}°C")

        print("\nPrecipitation Data:")
        for date, precip in precipitation_data.items():
            print(f"Date: {date}, Precipitation: {precip}mm")

        print("\nRelative Humidity Data:")
        for date, humidity in humidity_data.items():
            print(f"Date: {date}, Relative Humidity: {humidity}%")

    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    return None

def main():
    # Example usage
    date = "2024-01-15T00:00:00Z--2024-01-18T00:00:00Z:PT1H"
    parameters = "t_2m:C,precip_1h:mm"
    location = "52.520551,13.461804"
    username = "atkins_ejenam_enemchukwu"
    password = "f8EchDB8u8"
    
    get_weather_data(date, parameters, location, username, password)

if __name__ == '__main__':
    main()