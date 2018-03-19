CREATE TABLE `planning` (
	`ID` VARCHAR(50) NOT NULL,
	`Title` VARCHAR(200) NOT NULL,
	`Password` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`ID`)
)
COMMENT='This table holds all the planning entities, which is the main entity of the schema'
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;


CREATE TABLE `stories` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(50) NOT NULL,
	`PlanningID` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`ID`),
	INDEX `FK_stories_planning` (`PlanningID`),
	CONSTRAINT `FK_stories_planning` FOREIGN KEY (`PlanningID`) REFERENCES `planning` (`ID`)
)
COMMENT='This tables contains all the Stories for the planning.'
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

CREATE TABLE `estimates` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`User` VARCHAR(50) NOT NULL DEFAULT '0',
	`Estimate` TINYINT(4) NOT NULL DEFAULT '0',
	`Comment` VARCHAR(500) NULL DEFAULT '0',
	`StoryID` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`ID`),
	INDEX `FK_estimates_stories` (`StoryID`),
	CONSTRAINT `FK_estimates_stories` FOREIGN KEY (`StoryID`) REFERENCES `stories` (`ID`)
)
COMMENT='This contains all the estimates for stories'
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;


