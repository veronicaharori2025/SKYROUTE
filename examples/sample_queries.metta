;
; Sample MeTTa Queries for SkyRoute Flight System
; Example queries to test the flight route knowledge base
;

; Find fastest route from JFK to LHR
!(find-optimal-route "JFK" "LHR" "speed")

; Find cheapest route from LAX to CDG
!(find-optimal-route "LAX" "CDG" "cost")

; Find most comfortable route from SFO to DXB
!(find-optimal-route "SFO" "DXB" "comfort")

; Get all available routes from JFK to LHR
!(get-all-routes "JFK" "LHR")

; Get flight information for specific route
!(get-flight-details "JFK" "AMS" "DL123")

; Check airport information
!(get-airport-info "JFK")

; Get airlines operating between two airports
!(get-airlines-between "JFK" "LHR")

; Find routes with specific constraints
!(find-routes-with-constraints 
  "JFK" 
  "LHR" 
  (max-layovers 1) 
  (max-duration 10)
  (max-cost 800))