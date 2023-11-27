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
/*This is needed because for some reason DB thought it incredibly clever not to include the same information in Planned Data and Changed Data APIs so I had to construct my key.*/
CONCAT([test].[dbo].StationData.EVA_NR, [test].[dbo].PlannedArrivals.uniqueTrainTripId) as plannedDataUniqueId FROM [test].[dbo].PlannedArrivals
	INNER JOIN [test].[dbo].StationData
	ON PlannedArrivals.station = StationData.NAME