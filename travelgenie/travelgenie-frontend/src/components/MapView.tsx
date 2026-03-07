import Map, { Marker } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";

type Props = {
  locations: any[];
};

export default function MapView({ locations }: Props) {
  const mapboxToken = import.meta.env.VITE_MAPBOX_TOKEN;

  return (

    <Map
      initialViewState={{
        longitude: 12.4964,
        latitude: 41.9028,
        zoom: 12
      }}
      style={{ width: "100%", height: 400 }}
      mapStyle="mapbox://styles/mapbox/streets-v11"
      mapboxAccessToken={mapboxToken || ""}
    >

      {locations.map((loc, index) => (

        <Marker
          key={index}
          longitude={loc.lon}
          latitude={loc.lat}
        />

      ))}

    </Map>

  );
}