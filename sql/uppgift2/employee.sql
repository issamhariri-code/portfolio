SELECT * FROM employeetimestamps

INSERT INTO EmployeeTimeStamps (
TimeStampID, EmployeeID, TimeStampType, TimeStamp,
CardID, MachineID, MachineName
) VALUES
(1, 101, 'In', '2023-11-01 07:30:00', 'C101', 1, 'Office Entrance'),
(2, 101, 'Out', '2023-11-01 17:00:00', 'C101', 1, 'Office Entrance'),
(3, 102, 'In', '2023-11-01 08:15:00', 'C102', 1, 'Office Entrance'),
(4, 102, 'Out', '2023-11-01 16:45:00', 'C102', 1, 'Office Entrance'),
(5, 103, 'In', '2023-11-02 08:05:00', 'C103', 1, 'Office Entrance'),
(6, 103, 'Out', '2023-11-02 17:10:00', 'C103', 1, 'Office Entrance'),
(7, 104, 'In', '2023-11-02 08:20:00', 'C104', 1, 'Office Entrance'),
(8, 104, 'Out', '2023-11-02 16:50:00', 'C104', 1, 'Office Entrance'),
(9, 105, 'In', '2023-11-03 08:30:00', 'C105', 1, 'Office Entrance'),
(10, 105, 'Out', '2023-11-03 17:15:00', 'C105', 1, 'Office Entrance'),
(11, 106, 'In', '2023-11-03 08:35:00', 'C106', 1, 'Office Entrance'),
(12, 106, 'Out', '2023-11-03 17:20:00', 'C106', 1, 'Office Entrance'),
(13, 107, 'In', '2023-11-04 08:40:00', 'C107', 1, 'Office Entrance'),
(14, 101, 'In', '2023-11-04 08:45:00', 'C101', 1, 'Office Entrance'),
(15, 102, 'In', '2023-11-04 08:50:00', 'C102', 1, 'Office Entrance'),
(16, 103, 'In', '2023-11-04 08:55:00', 'C103', 1, 'Office Entrance'),
(17, 104, 'In', '2023-11-04 09:00:00', 'C104', 1, 'Office Entrance'),
(18, 105, 'In', '2023-11-04 09:05:00', 'C105', 1, 'Office Entrance'),
(19, 101, 'Out', '2023-11-04 17:30:00', 'C101', 2, 'Loading Dock'),
(20, 102, 'Out', '2023-11-04 17:45:00', 'C102', 2, 'Loading Dock');

-- 1. Lista alla instämplingar

SELECT * FROM EmployeeTimeStamps
WHERE TimeStampType = 'In'

-- 2. Visa instämplingar för en viss anställd
SELECT * FROM EmployeeTimeStamps
WHERE EmployeeID = 101
AND TimeStampType = 'In';

-- 3. Lista unika anställda som stämplat in
SELECT DISTINCT EmployeeID
FROM EmployeeTimeStamps
WHERE TimeStampType = 'In';

-- 4. Visa alla utstämplingar
SELECT * FROM EmployeeTimeStamps
WHERE TimeStampType = 'Out';

-- 5. Visa instämplingar efter ett visst datum
SELECT * FROM EmployeeTimeStamps
WHERE TimeStampType = 'In'
AND TimeStamp > '2023-11-01';

-- 6. Instämplingar före klockan 9
SELECT *
FROM EmployeeTimeStamps
WHERE TimeStampType = 'In'
AND TIME(TimeStamp) < '09:00:00';

-- 7. Alla stämplingar från ett specifikt datum
SELECT * FROM EmployeeTimeStamps
WHERE DATE(TimeStamp) = '2023-11-03';

-- 8. Instämplingar från en viss plats (MachineName)
SELECT * FROM employeetimestamps
WHERE TimeStampType = 'In' AND MachineName = 'Office Entrance';

-- 9. Instämplingar under en viss veckodag
SELECT * FROM EmployeeTimeStamps
WHERE TimeStampType = 'In' AND DAYNAME(TimeStamp) = 'Friday';

-- 10. Utstämplingar från ett specifikt datum
SELECT * FROM employeetimestamps
WHERE TimeStampType = 'Out' AND DATE(TimeStamp) = '2023-11-04';