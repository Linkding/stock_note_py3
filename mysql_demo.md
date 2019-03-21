```
CREATE TABLE `gov_bond_yield` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `date` DATE NULL,
  `10y` FLOAT NULL,
  PRIMARY KEY (`id`)
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;
;
```
```
select * from  gov_bond_yield order by date  limit 5;  
select * from  gov_bond_yield order by date desc limit 5; 
```