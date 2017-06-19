USE e32;
// I ] MODELE SQL en étoile 

// Dimension taxi réferencant tous les taxis de la compagnie:
// id : identifiant unique
// CREATE TABLE DIM_TAXI (id int, primary key(id)); 

// Dimension Date referencant toutes les dates depuis 2001
// timestamp : identifiant de la date UNIX
// CREATE TABLE DIM_DATE (timestamp int, primary key(timestamp));

// Dimension Stand referencant tous les stands de la ville
// id : identifiant du stand
// CREATE TABLE DIM_STAND (id int, primary key(id));

// Dimension Client referencant tous les clients de la compagnie
// id : identifiant du client
// CREATE TABLE DIM_CLIENT (id int, primary key(id));


// Table des faits : à evoluer
	// fkdate : foreign key sur table date
	// fktaxi : foreign key sur table taxi
	// fkclient : foreign key sur table client
	// fkstand : foreign key sur table stand
	// trip : id du trajet / faits 
	// distance : somme des distances entre points de la polyline
	// o : premier points de la polyline
	// d : dernier point de la polyline

// AREA est un cluster de la ville (zone d'approximation gps) : la ville sera donc quadrillé en carré : 
	// 9 digits is too detailed for any but a long term geodetic app.
	// 6 digits is in centimeter range, and usually the most accurate what makes sense for a GPS device.
	// At equator 4 digits after decimal point is 11.11m.
	// 3 digits are 111.11m
	// (Calculated by earthCircumference / 360.0)
	//This would normally result a raster, but since Earth is a sphere, the distance between two longitudes shrinks when moving away from the equator (with a factor of cos(latitude)) the distance between two latitudes does not change.


// II ] MODELE CASSANDRA NOSQL // mettre tous en string

	//  BY_TIME
	//  permet une partition pour un jour d'un mois d'une année particulier
	//  ajoute un clustering par heure et minute pour une finesse au trip près 
	
	CREATE TABLE IF NOT EXISTS TRIP_BY_TIME (annee text, mois text, jour text, dayOWeek text, heure text, minute text, trip text, distance text, o_lon text, o_lat text, d_lon text, d_lat text, primary key((annee, mois, jour), heure, minute, trip));

	//  BY_TAXI
	//  permet une partition sur chaque id de taxi (avoir distance parcourue / dayOWeek pour chaque taxi)
	//  permet une partition sur chaque id de taxi (avoir distance parcourue / h pour chaque taxi)
	//  zones de départs (trouver moyenne / taxi par exemple)
	//  zones d'arrivée (trouver moyenne / taxi par exemple)
	//  clustering au trip près et au dayOWeek / heure	
	
	CREATE TABLE IF NOT EXISTS TRIP_BY_TAXI (taxi text, trip text, dayOWeek text, heure text, distance text, o_lon text, o_lat text, d_lon text, d_lat text, primary key((taxi), dayOWeek, heure, trip));


	//  BY_ORIGIN_AREA
	//  permet une partition par zone de départ
	//  clustering sur heure de la journée (utile pour prévenir le traffic dans les zones de la ville / jour de la semaine)
	//  clustering sur heure de la journée (utile pour prévenir le traffic dans les zones de la ville / h)

	CREATE TABLE IF NOT EXISTS TRIP_BY_ORIGIN_AREA (o_lon text, o_lat text, trip text, dayOWeek text, heure text, distance text, primary key((o_lon, o_lat), dayOWeek, heure, trip));


	//  BY_DISTANCE_AREA
	//  permet une partition par zone d'arrivée
	//  clustering sur heure de la journée (utile pour prévenir le traffic dans les zones de la ville / jour de la semaine)
	//  clustering sur heure de la journée (utile pour prévenir le traffic dans les zones de la ville / h)
	
	CREATE TABLE IF NOT EXISTS TRIP_BY_DESTINATION_AREA (d_lon text, d_lat text, trip text, dayOWeek text, heure text, distance text, primary key((d_lon, d_lat), dayOWeek, heure, trip));



	//  BY_o_AND_d_AREA
	//  permet une partition par zone d'o et d'arrivée
 	//  permettra d'effectuer Kmeans et tirer les trajets types contenus
	
	CREATE TABLE IF NOT EXISTS TRIP_BY_ORIGIN_AND_DESTINATION ( o_lon text, o_lat text, d_lon text, d_lat text, trip text, dayOWeek text, heure text, distance text, primary key((o_lon, o_lat, d_lon, d_lat), dayOWeek, heure, trip));




