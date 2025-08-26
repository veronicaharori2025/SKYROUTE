;
; SkyRoute Flight Knowledge Base
; ==============================
; MeTTa knowledge base for optimal flight route finding
; Contains facts about airports, flights, and routing logic
;

;;
;; Airport Knowledge Base
;;

; Airport facts: (airport <code> <name> <city> <country> <timezone>)
(airport "JFK" "John F. Kennedy International" "New York" "USA" "-5")
(airport "LHR" "Heathrow Airport" "London" "UK" "0")
(airport "CDG" "Charles de Gaulle Airport" "Paris" "France" "+1")
(airport "AMS" "Amsterdam Airport Schiphol" "Amsterdam" "Netherlands" "+1")
(airport "DXB" "Dubai International" "Dubai" "UAE" "+4")
(airport "LAX" "Los Angeles International" "Los Angeles" "USA" "-8")
(airport "SFO" "San Francisco International" "San Francisco" "USA" "-8")

;;
;; Flight Connection Knowledge Base
;;

; Flight facts: (flight <number> <airline> <from> <to> <duration> <cost> <departure-time>)
(flight "DL123" "Delta" "JFK" "AMS" 420 500 "08:00")
(flight "KL601" "KLM" "JFK" "AMS" 400 550 "14:00")
(flight "AF123" "Air France" "JFK" "CDG" 420 600 "09:30")

(flight "KL100" "KLM" "AMS" "LHR" 60 150 "12:00")
(flight "BA200" "British Airways" "AMS" "LHR" 70 120 "18:00")
(flight "AF300" "Air France" "CDG" "LHR" 80 130 "16:00")

(flight "EK202" "Emirates" "DXB" "LHR" 420 700 "22:00")
(flight "UA500" "United" "SFO" "DXB" 900 1100 "13:00")
(flight "DL800" "Delta" "LAX" "CDG" 660 900 "11:00")

;;
;; Routing Rules and Logic
;;

; Rule: Direct flight connection
(direct-flight ?from ?to ?flight ?duration ?cost)
    :- (flight ?flight ?airline ?from ?to ?duration ?cost ?time)

; Rule: Connecting flight (one layover)
(connecting-flight ?from ?to ?flight1 ?flight2 ?total-duration ?total-cost)
    :- (flight ?flight1 ?airline1 ?from ?layover ?duration1 ?cost1 ?time1)
       (flight ?flight2 ?airline2 ?layover ?to ?duration2 ?cost2 ?time2)
       (= ?total-duration (+ ?duration1 ?duration2 120)) ; Add 2h for layover
       (= ?total-cost (+ ?cost1 ?cost2))

; Rule: Find all possible routes between two airports
(get-all-routes ?from ?to ?routes)
    :- (find-all ?route (or (direct-flight ?from ?to ?flight ?dur ?cost)
                            (connecting-flight ?from ?to ?f1 ?f2 ?dur ?cost))
                 ?routes)

; Rule: Find optimal route based on priority
(find-optimal-route ?from ?to "speed" ?optimal-route)
    :- (get-all-routes ?from ?to ?routes)
       (find-min ?route (get-duration ?route) ?routes ?optimal-route)

(find-optimal-route ?from ?to "cost" ?optimal-route)
    :- (get-all-routes ?from ?to ?routes)
       (find-min ?route (get-cost ?route) ?routes ?optimal-route)

(find-optimal-route ?from ?to "comfort" ?optimal-route)
    :- (get-all-routes ?from ?to ?routes)
       (find-min ?route (get-layovers ?route) ?routes ?optimal-route)

; Helper functions
(get-duration ((direct-flight ?from ?to ?flight ?duration ?cost)) ?duration)
(get-duration ((connecting-flight ?from ?to ?f1 ?f2 ?duration ?cost)) ?duration)

(get-cost ((direct-flight ?from ?to ?flight ?duration ?cost)) ?cost)
(get-cost ((connecting-flight ?from ?to ?f1 ?f2 ?duration ?cost)) ?cost)

(get-layovers ((direct-flight ?from ?to ?flight ?duration ?cost)) 0)
(get-layovers ((connecting-flight ?from ?to ?f1 ?f2 ?duration ?cost)) 1)

;;
;; Utility Functions
;;

; Convert minutes to hours and minutes
(minutes-to-hm ?minutes ?hours ?remaining-mins)
    :- (= ?hours (div ?minutes 60))
       (= ?remaining-mins (mod ?minutes 60))

; Format duration as string
(format-duration ?minutes $str)
    :- (minutes-to-hm ?minutes ?hours ?mins)
       (= ?str (concat (str ?hours) "h " (str ?mins) "m"))

;;
;; Example Queries for Testing
;;

; Uncomment to test specific queries
; !(find-optimal-route "JFK" "LHR" "speed")
; !(get-all-routes "JFK" "LHR")
; !(direct-flight "JFK" "AMS" ?flight ?duration ?cost)