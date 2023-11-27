CREATE VIEW PlannedArrivalsVIEW3 AS
SELECT 
PlannedArrivals.uniqueId,
PlannedArrivals.station AS stationName, 
PlannedArrivals.uniqueTrainTripId,
PlannedArrivals.arrivalPlannedLine, 
PlannedArrivals.arrivalPlannedPlatform, 
PlannedArrivals.arrivalPlannedTime, 
PlannedArrivals.arrivalPlannedTransition, 
StationData.EVA_NR AS evaNumber,
StationData.Laenge AS stationLongitude,
StationData.Breite AS stationLatitude,
CONCAT([test].[dbo].StationData.EVA_NR, [test].[dbo].PlannedArrivals.uniqueTrainTripId) as plannedDataUniqueId FROM [test].[dbo].PlannedArrivals
	INNER JOIN [test].[dbo].StationData
	ON PlannedArrivals.station = StationData.NAME