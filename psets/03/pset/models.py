"""Data models."""

# Numpy
import numpy as np


class Museum:
    """Museum.

    Store information like ID, name, latitude and longitude
    along with the other museums its connected with.
    """

    R = 6373000

    def __init__(self, pk, name, lat, long, N):
        self.pk = pk
        self.name = name
        self._latitude = lat
        self._longitude = long

        # System normalizer
        self.N = N

        # Connections. Store distance and uses the museum's IDs as keys
        self.connections = {}

    @property
    def lat(self, rad=False):
        """Return latitude, in radians if requested."""
        return np.radians(_latitude) if rad else self._latitude

    @property
    def lon(self, rad=False):
        """Return longitude, in radians if requested."""
        return np.radians(_longitude) if rad else self._longitude

    def is_connected_to(self, museum):
        """Given a museum ID, return True if a connection exists."""
        if self.connections.get(museum, None):
            return True
        return False

    def connect_to(self, museum, distance):
        """Given a museum ID, create a new connections using distance."""
        if not self.is_connected_to(museum):
            self.connections[museum] = distance

    def get_distance_from(self, museum):
        """Return distance from given museum object.

        If no connection exists, return the weight specified by
        the problem set.
        """
        if self.is_connected_to(museum.pk):
            return self.connections[museum.pk]
        return self.__compute_missing_connection_weight(museum)

    def __compute_missing_connection_weight(self, museum):
        """Compute custom weight as specified in the problem set."""
        A = (
            (np.sin((self.lat(rad=True) - museum.lat(rad=True)) / 2) ** 2) +
            (
                np.cos(museum.lat(rad=True)) *
                np.cos(self.lat(rad=True)) *
                np.sin((self.lon(rad=True) - museum.lon(rad=True)) / 2) ** 2
            )

        )
        C = 2 * np.arctan2(np.sqrt(A), np.sqrt(1 - A))
        return self.R * C * self.N
