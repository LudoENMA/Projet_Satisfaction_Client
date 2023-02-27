use customer_satisfaction;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/inf_company.csv'
IGNORE INTO TABLE info_company
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
select * from info_company;
SELECT name_company, nombre_avis,  localisation_company FROM info_company WHERE localisation_company="Paris";