"""
Weather Conditions class

Description: This class provide diferent weather variables from
differents APIs as OpenWeather and ECWMF.

Author: Sebastian Pasker
Date: 2024-03-17
"""

import log_config as log


class Weather_Conditions:
    """
    Weather Conditions class

    This class provides differents variables from weather APIs.
    """

    place = None
    coord = (None, None)
    search_by_coord = False
    api_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_token = ""
    api_weather_dict = None

    # TODO Set as empty weather dict
    # weather_dict = {
    #     "wind": None,
    #     "waves": None,
    #     "humidity": None,
    #     "temperature": None,
    # }
    weather_dict = None

    def __init__(self, search_by_coord=True, place=None, coord=None):
        """
        Weather Conditions class constructor

        This constructor initialize the class with the place or the
        coordinates to search the weather conditions.

        Args:
            search_by_coord (bool): If True, the search will be by coordinates.
            place (str): The place to search the weather conditions.
            coord (tuple): The coordinates to search the weather conditions.
        """

        # Set the logger
        log.log_config()

        # Set the search type
        self.search_by_coord = search_by_coord
        # Set the place or the coordinates
        if search_by_coord and coord is not None:
            self.coord = coord
        # Set the place
        elif place is not None:
            self.place = place
        # Get the token
        self.token = self.get_token()

        log.log_info("Weather Conditions class initialized")

    def call_api(self):
        if self.token is None:
            log.log_error("Token not found")
            return

        url = ""

        if self.search_by_coord:
            url = (
                self.api_url
                + "lat="
                + str(self.coord[0])
                + "&lon="
                + str(self.coord[1])
                + "&appid="
                + self.token
            )
        elif self.place is not None:
            url = self.api_url + "q=" + self.place + "&appid=" + self.token

        # TODO call api
        print(url)

        log.log_info("API called")

    def set_coord(self, coord):
        """
        Set the coordinates to search the weather conditions.

        Args:
            coord (tuple): The coordinates to search the weather conditions.
        """
        self.search_by_coord = True
        self.coord = coord

        log.log_info("Coordinates set to " + str(coord))

    def set_place(self, place):
        """
        Set the place to search the weather conditions.

        Args:
            place (str): The place to search the weather conditions.
        """
        self.search_by_coord = False
        self.place = place

        log.log_info("Place set to " + place)

    def get_token(self):
        """
        Get the token from the file.

        Returns:
            str: The token from the file.
        """
        token = None
        try:
            with open("../keys/token_open_weather.txt", "r") as f:
                token = f.read()
            log.log_info("Token read from file")
        except Exception as e:
            log.log_error("Error reading token from file: " + str(e))
            raise e

        return token

    def get_wind(self):
        wind = None
        if self.api_weather_dict is None:
            log.log_error("API weather dictionary not found")
        elif "wind" in self.api_weather_dict:
            wind = self.api_weather_dict["wind"]
        return wind

    def get_waves():
        waves = None
        if self.api_weather_dict is None:
            log.log_error("API weather dictionary not found")
        elif "waves" in self.api_weather_dict:
            waves = self.api_weather_dict["waves"]
        return waves

    def get_humidity():
        humidity = None
        if self.api_weather_dict is None:
            log.log_error("API weather dictionary not found")
        elif "humidity" in self.api_weather_dict:
            humidity = self.api_weather_dict["waves"]
        return humidity

    def get_temperature():
        temperature = None
        if self.api_weather_dict is None:
            log.log_error("API weather dictionary not found")
        elif "temperature" in self.api_weather_dict:
            temperature = self.api_weather_dict["waves"]
        return temperature

    def get_dictionary():
        # TODO
        weather_dict = {}
        return weather_dict
