CREATE TABLE `passwordsm` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(50) NOT NULL,
	`password` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`ID`)
)
COMMENT='This contains the password for the SM for the time being'
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

INSERT INTO `distripp`.`passwordsm` (`username`, `password`) VALUES ('sm', 'test');