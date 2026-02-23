#!/usr/bin/env python3
"""
=============================================================================
API Query Script for Reporter Application
=============================================================================

API Name: USGS Earthquake Catalog API
API Documentation: https://earthquake.usgs.gov/fdsnws/event/1/

Endpoint: https://earthquake.usgs.gov/fdsnws/event/1/query

Description:
    This script queries the USGS Earthquake Catalog API to retrieve recent
    earthquake data. This is a FREE public API that does NOT require an API key.

    The data is useful for building a reporter application that can:
    - Track seismic activity worldwide
    - Analyze earthquake patterns by magnitude, location, and time
    - Generate reports on earthquake frequency and intensity

Parameters Used:
    - format: geojson (response format)
    - starttime: Start date for earthquake search
    - endtime: End date for earthquake search
    - minmagnitude: Minimum earthquake magnitude (filters smaller quakes)
    - limit: Maximum number of results to return
    - orderby: Sort order (time, magnitude, etc.)

Expected Data:
    - Returns 20+ earthquake records
    - Each record contains: time, location (lat/lon), magnitude, depth, place name
    - Data structure: GeoJSON FeatureCollection with earthquake features

Key Fields in Response:
    - properties.mag: Earthquake magnitude
    - properties.place: Location description
    - properties.time: Unix timestamp of event
    - properties.type: Event type (earthquake, quarry blast, etc.)
    - properties.tsunami: Tsunami warning flag
    - geometry.coordinates: [longitude, latitude, depth]

=============================================================================
"""

import requests
import json
from datetime import datetime, timedelta

def fetch_earthquake_data():
    """
    Fetch recent earthquake data from USGS API.
    Returns earthquakes with magnitude >= 4.0 from the past 30 days.
    """

    # API endpoint
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    # Calculate date range (past 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Query parameters
    params = {
        "format": "geojson",
        "starttime": start_date.strftime("%Y-%m-%d"),
        "endtime": end_date.strftime("%Y-%m-%d"),
        "minmagnitude": 4.0,  # Only significant earthquakes
        "limit": 50,          # Get up to 50 records
        "orderby": "time"     # Most recent first
    }

    print("=" * 70)
    print("USGS Earthquake Data Query")
    print("=" * 70)
    print(f"\nQuery Parameters:")
    print(f"  - Date Range: {params['starttime']} to {params['endtime']}")
    print(f"  - Minimum Magnitude: {params['minmagnitude']}")
    print(f"  - Max Results: {params['limit']}")
    print(f"  - API Endpoint: {base_url}")
    print("\nFetching data...")

    try:
        # Make API request
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Extract earthquake features
        earthquakes = data.get("features", [])
        total_count = data.get("metadata", {}).get("count", len(earthquakes))

        print(f"\n✅ Success! Retrieved {total_count} earthquake records.\n")
        print("=" * 70)
        print(f"{'#':<4} {'Magnitude':<10} {'Location':<35} {'Date/Time':<20}")
        print("=" * 70)

        # Display earthquake data
        for i, quake in enumerate(earthquakes, 1):
            props = quake.get("properties", {})
            coords = quake.get("geometry", {}).get("coordinates", [0, 0, 0])

            # Extract fields
            magnitude = props.get("mag", "N/A")
            place = props.get("place", "Unknown")[:33]
            timestamp = props.get("time", 0)

            # Convert timestamp to readable date
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1000)
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            else:
                date_str = "Unknown"

            # Print row
            print(f"{i:<4} {magnitude:<10} {place:<35} {date_str:<20}")

        print("=" * 70)

        # Summary statistics
        magnitudes = [q["properties"]["mag"] for q in earthquakes if q["properties"].get("mag")]
        if magnitudes:
            print(f"\n📊 Summary Statistics:")
            print(f"  - Total Records: {len(earthquakes)}")
            print(f"  - Max Magnitude: {max(magnitudes):.1f}")
            print(f"  - Min Magnitude: {min(magnitudes):.1f}")
            print(f"  - Average Magnitude: {sum(magnitudes)/len(magnitudes):.2f}")

        # Show sample raw data structure
        print(f"\n📋 Sample Record (JSON structure):")
        if earthquakes:
            sample = earthquakes[0]
            print(json.dumps({
                "type": sample.get("type"),
                "properties": {
                    "mag": sample["properties"].get("mag"),
                    "place": sample["properties"].get("place"),
                    "time": sample["properties"].get("time"),
                    "type": sample["properties"].get("type"),
                    "tsunami": sample["properties"].get("tsunami")
                },
                "geometry": sample.get("geometry")
            }, indent=2))

        return earthquakes

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching data: {e}")
        return []

if __name__ == "__main__":
    earthquakes = fetch_earthquake_data()
    print(f"\n✅ Query complete. {len(earthquakes)} records retrieved.")
