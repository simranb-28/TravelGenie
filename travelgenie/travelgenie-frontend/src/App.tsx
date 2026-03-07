import { useState, useEffect } from "react";
import "./App.css";

import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./mapFix";

// Helper component to set map view
function SetMapView({ lat, lng, zoom }: { lat: number; lng: number; zoom: number }) {
  const map = useMap();
  
  useEffect(() => {
    map.setView([lat, lng], zoom);
  }, [map, lat, lng, zoom]);
  
  return null;
}

function App() {

  const [destination,setDestination] = useState("");
  const [duration,setDuration] = useState("");
  const [budget,setBudget] = useState("");
  const [preferences,setPreferences] = useState("");

  const [trip,setTrip] = useState<any>(null);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState("");
  const [mapCoords,setMapCoords] = useState<{lat:number, lng:number} | null>(null);
  const [selectedDayIndex,setSelectedDayIndex] = useState<number | null>(null);
  const [showRecommendedExperiences,setShowRecommendedExperiences] = useState(false);

  const getCoordinates = async (city: string) => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(city)}&format=json&limit=1`
      );
      const data = await response.json();
      if (data.length > 0) {
        return {
          lat: parseFloat(data[0].lat),
          lng: parseFloat(data[0].lon)
        };
      }
    } catch (err) {
      console.error("Geocoding error:", err);
    }
    return null;
  };

  // Function to get weather emoji
  const getWeatherEmoji = (weather: string): string => {
    const weatherLower = weather.toLowerCase();
    if (weatherLower.includes("rain")) return "🌧️";
    if (weatherLower.includes("cloud")) return "☁️";
    if (weatherLower.includes("clear") || weatherLower.includes("sunny")) return "☀️";
    if (weatherLower.includes("snow")) return "❄️";
    if (weatherLower.includes("thunder")) return "⛈️";
    if (weatherLower.includes("wind")) return "💨";
    if (weatherLower.includes("fog")) return "🌫️";
    return "🌤️"; // Default
  };

  const generateTrip = async () => {

    if(!destination || !duration || !budget){
      setError("Please fill destination, days and budget.");
      return;
    }

    setLoading(true);
    setError("");
    setTrip(null);
    setMapCoords(null);

    try{

      const res = await fetch("http://localhost:8000/generate-trip",{
        method:"POST",
        headers:{
          "Content-Type":"application/json"
        },
        body:JSON.stringify({
          destination,
          duration:Number(duration),
          budget,
          preferences: preferences
        })
      });

      const data = await res.json();

      if(!res.ok){
        throw new Error("Backend error");
      }

      console.log("Trip data received:", data);

      setTrip(data);

      // Get coordinates for the destination
      const coords = await getCoordinates(destination);
      if (coords) {
        setMapCoords(coords);
      }

    }catch(err){

      console.error(err);
      setError("Something went wrong while generating the trip.");

    }

    setLoading(false);

  };

  const clearSearch = () => {
    setDestination("");
    setDuration("");
    setBudget("");
    setPreferences("");
    setTrip(null);
    setError("");
    setMapCoords(null);
    setSelectedDayIndex(null);
    setShowRecommendedExperiences(false);
  };

  return(

    <div className="app">

      <h1 className="main-title">✈️ Welcome to TravelGenie</h1>

      <p className="subtitle">
        Plan smart trips instantly. Enter destination, budget and preferences to generate itinerary.
      </p>

      <div className="search">

        <input
          placeholder="Destination city"
          value={destination}
          onChange={(e)=>setDestination(e.target.value)}
        />

        <input
          placeholder="Days of travel"
          value={duration}
          onChange={(e)=>setDuration(e.target.value)}
        />

        <input
          placeholder="Budget eg 50K or 1L"
          value={budget}
          onChange={(e)=>setBudget(e.target.value)}
        />

        <input
          placeholder="Preferences (food, culture)"
          value={preferences}
          onChange={(e)=>setPreferences(e.target.value)}
        />

        <button onClick={generateTrip}>
          {loading ? "Generating..." : "Generate Trip"}
        </button>

        {trip && (
          <button onClick={clearSearch} className="clear-button">
            🔄 New Search
          </button>
        )}

      </div>

      {error && (
        <p className="error-msg">{error}</p>
      )}

      {trip && (

        <div className="results">

          <div className="title-with-weather">
            <h2 className="trip-title">
              {trip.destination} Travel Plan
            </h2>

            {/* Weather Section - Inline with Title */}
            <div className="weather-badge">
              {trip.weather ? (
                <span>{getWeatherEmoji(trip.weather)} {trip.weather}</span>
              ) : (
                <span>🌤️ Loading...</span>
              )}
            </div>
          </div>

          {/* Budget allocation */}

          {trip.budget_allocation && (

            <div className="budget-horizontal">

              <span>🛏️ Stay ₹{trip.budget_allocation.stay}</span>
              <span>🍽️ Food ₹{trip.budget_allocation.food}</span>
              <span>🚕 Transport ₹{trip.budget_allocation.transport}</span>
              <span>🎟️ Activities ₹{trip.budget_allocation.activities}</span>

            </div>

          )}

          {/* Recommended Experiences Button */}
          {trip.recommended_experiences && trip.recommended_experiences.length > 0 && (
            <div style={{marginBottom: "15px"}}>
              <button 
                onClick={() => setShowRecommendedExperiences(!showRecommendedExperiences)}
                className="recommended-exp-button"
              >
                ✨ {showRecommendedExperiences ? "Hide" : "Show"} Recommended Experiences
              </button>
            </div>
          )}

          {/* Main content with itinerary and recommended experiences panel */}
          <div className="itinerary-with-panel">

            {/* Itinerary */}
            <div className="itinerary-section">

              <h3 className="trip-itinerary-title">
                Trip Itinerary
              </h3>

              <div className="section-divider"></div>

              {trip.itinerary?.map((day:any,index:number)=>{

                const parts = day.split(":");

                return(

                  <div 
                    key={index} 
                    className="itinerary-card"
                    onClick={() => setSelectedDayIndex(selectedDayIndex === index ? null : index)}
                    style={{cursor:"pointer"}}
                  >

                    <span className="day-label">
                      {parts[0]}:
                    </span>

                    {parts.slice(1).join(":")}

                  </div>

                )

              })}

            </div>

            {/* Recommended Experiences Panel - appears when button is clicked */}
            {showRecommendedExperiences && trip.recommended_experiences && trip.recommended_experiences.length > 0 && (
              <div className="experiences-panel">
                <h3 className="panel-title">
                  ✨ Recommended Experiences
                </h3>
                <div className="experiences-list">
                  {trip.recommended_experiences.map((exp:any, idx:number) => (
                    <div key={idx} className="experience-item">
                      <h4>{exp.name}</h4>
                      {exp.description && <p>{exp.description}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>

          {/* Map Section */}

          <div className="map-section">

            <h3 className="trip-itinerary-title">
              Destination Map
            </h3>

            {mapCoords && (
              <MapContainer
                style={{height:"250px",width:"80%",borderRadius:"12px",margin:"0 auto"}}
                className="map-container"
              >
                <SetMapView lat={mapCoords.lat} lng={mapCoords.lng} zoom={8} />

                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                <Marker position={[mapCoords.lat, mapCoords.lng]}>
                  <Popup>
                    {trip.destination}
                  </Popup>
                </Marker>

              </MapContainer>
            )}

            {!mapCoords && (
              <p style={{color:"#6b7280", marginTop:"10px"}}>
                Map loading...
              </p>
            )}

          </div>

        </div>

      )}

    </div>

  )

}

export default App;