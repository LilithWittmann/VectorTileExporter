# Vector tiles to GeoJSON

Nowadays modern web maps are usually based on [vector tiles](https://en.wikipedia.org/wiki/Vector_tiles).

The great thing about vector tiles is, that they are not just images but basically encoded representations of map data that can be decoded again.

In this repository there are two scripts, that allow you to download and parse web maps based on vector tiles that are hosted in the [Mapbox format](https://en.wikipedia.org/wiki/Vector_tiles#Protocol_buffers_(Mapbox)):

- `scraper.py` - helps you in downloading vector tiles from a map server inside certain boundaries;
- `parser.py ` - parses layers out of the downloaded vector tiles and converts them into [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON).

Before use those scripts [install requirements using PIP](https://pip.pypa.io/en/latest/user_guide/#requirements-files).

**NOTE:** This is only a proof of concept 😉.
