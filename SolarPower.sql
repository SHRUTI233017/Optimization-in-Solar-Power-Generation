create database solarPower;
use solarPower;
select * from merged_dataset;
  
#1. Average output by inverter to detect inefficiencies
SELECT
  AVG(UNIT1_INV1) AS avg_INV1,
  AVG(UNIT1_INV2) AS avg_INV2,
  AVG(UNIT2_INV1) AS avg_INV3,
  AVG(UNIT2_INV2) AS avg_INV4
FROM merged_dataset;

#2. Identify peak solar generation hours
SELECT 
  HOUR(Date_Time) AS hour,
  AVG(UNIT1_INV1 + UNIT1_INV2 + UNIT2_INV1 + UNIT2_INV2) AS avg_hourly_output
FROM merged_dataset
GROUP BY hour
ORDER BY avg_hourly_output DESC;


#3. Impact of GII (sunlight) on power generation
SELECT    
  GOBAL_IRRADIANCE_INDEX,  
  ROUND(AVG(UNIT1_INV1 + UNIT1_INV2 + UNIT2_INV1 + UNIT2_INV2), 2) AS avg_power_output
FROM merged_dataset
GROUP BY GOBAL_IRRADIANCE_INDEX
ORDER BY GOBAL_IRRADIANCE_INDEX;


#4. Effect of rain on solar output
SELECT 
  RAIN,
  AVG(UNIT1_INV1 + UNIT1_INV2 + UNIT2_INV1 + UNIT2_INV2) AS avg_power_output
FROM merged_dataset
GROUP BY RAIN
ORDER BY RAIN;

#5. Impact of module temperature on power generation
SELECT 
  MODULE_TEMP_1,
  AVG(UNIT1_INV1 + UNIT1_INV2 + UNIT2_INV1 + UNIT2_INV2) AS avg_output
FROM merged_dataset
GROUP BY MODULE_TEMP_1
ORDER BY MODULE_TEMP_1;

#6. Daily trend of total power generation
SELECT 
  DATE(Date_Time) AS date,
  SUM(UNIT1_INV1 + UNIT1_INV2 + UNIT2_INV1 + UNIT2_INV2) AS total_output
FROM merged_dataset
GROUP BY date
ORDER BY date;








 
    
    
    
    
    
    
    

