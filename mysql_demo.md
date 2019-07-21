```
CREATE TABLE `gov_bond_yield` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `date` VARCHAR(100) NULL,
  `10y` FLOAT NULL,
  PRIMARY KEY (`id`)
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;

```
```
select * from  gov_bond_yield order by date  limit 5;  
select * from  gov_bond_yield order by date desc limit 5; 
```

ts_code trade_date      close       open       high        low
```
CREATE TABLE `hs300` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `ts_code` VARCHAR(100) NULL,
  `trade_date` VARCHAR(100) NULL,
  `close` FLOAT NULL,
  `open` FLOAT NULL,
  `high` FLOAT NULL,
  `low` FLOAT NULL,
  PRIMARY KEY (`id`)
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;
```