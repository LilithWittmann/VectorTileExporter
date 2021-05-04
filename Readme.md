# Vectortiles to GeoJSON
Nowadays modern web maps are usually based on Vectormaps. 
The great thing about Vectormaps is, that they are not just images but basically encoded representations of map data that can be decoded again.

In this repository there are two scripts, that allow you to download and parse vector maps that are hosted in the mapbox format.

``scraper.py`` - helps you in downloading maptiles from a server inside certain boundaries.
``parser.py `` - parses layers out of the downloaded map tiles and converts them into geojson

This is only a proof of concept 😉.