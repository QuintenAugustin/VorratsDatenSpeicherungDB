CREATE VIEW ViewForR2 AS
SELECT
PLAAR.stationName,
PLAAR.uniqueTrainTripId,
PLAAR.arrivalPlannedLine,
PLAAR.arrivalPlannedPlatform,
PLAAR.arrivalPlannedTime,
PLADEP.departurePlannedLine,
PLADEP.departurePlannedPlatform,
PLADEP.departurePlannedTime,
PLATR.TrainCategory,
PLATR.TrainNumber,
CHAAR.arrivalCancellationStatus,
CHAAR.arrivalChangesPlannedStatus,
CHAAR.arrivalCancellationTime,
CHAAR.arrivalChangeTime,
CHAAR.arrivalChangePlatform,
CHAAR.arrivalChangesLine,
CHADEP.departureCancellationStatus,
CHADEP.departureCancellationTime,
CHADEP.departureChangesPlannedStatus,
CHADEP.departureChangeTime,
CHADEP.departureChangePlatform,
CHADEP.departureChangesLine,
PLAAR.stationLatitude,
PLAAR.stationLongitude,
PLAAR.plannedDataUniqueId,
CHAAR.uniqueId AS changedArrivalsUniqueId,
CHADEP.uniqueId AS changedDeparturesUniqueId
FROM [test].[dbo].[PlannedArrivalsVIEW3] PLAAR
FULL OUTER JOIN [test].[dbo].PlannedDepartures AS PLADEP ON PLAAR.uniqueId = PLADEP.uniqueId
LEFT OUTER JOIN [test].[dbo].PlannedTrainInformation AS PLATR ON PLAAR.uniqueId = PLATR.uniqueId
LEFT OUTER JOIN [test].[dbo].ChangedArrivals AS CHAAR ON PLAAR.plannedDataUniqueId = CHAAR.uniqueId
/* This last join works just fine because Planned Arrivals always ends up containing all entries (by ID) that departure data contains and i was stupid to split the two in two Tables */
LEFT OUTER JOIN [test].dbo.ChangedDepartures AS CHADEP ON PLAAR.plannedDataUniqueId = CHADEP.uniqueId