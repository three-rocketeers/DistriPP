CREATE TABLE `planning` (
	`ID` VARCHAR(50) NOT NULL,
	`Title` VARCHAR(200) NOT NULL,
	`Password` VARCHAR(50) NOT NULL
)
COMMENT='This table holds all the planning entities, which is the main entity of the schema'
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

CREATE TABLE `stories` (
	`ID` INT(11) NOT NULL,
	`URL` INT(11) NOT NULL,
	`PlanningID` VARCHAR(50) NOT NULL
)
COMMENT='This tables contains all the Stories for the planning.'
ENGINE=InnoDB
;

ALTER TABLE `planning`
	ADD PRIMARY KEY (`ID`);

ALTER TABLE `stories`
	ADD PRIMARY KEY (`ID`);

ALTER TABLE `stories`
	ADD CONSTRAINT `FK_stories_planning` FOREIGN KEY (`PlanningID`) REFERENCES `planning` (`ID`);

CREATE TABLE `estimates` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`User` VARCHAR(50) NOT NULL DEFAULT '0',
	`Estimate` TINYINT NOT NULL DEFAULT '0',
	`Comment` VARCHAR(500) NULL DEFAULT '0',
	`StoryID` INT NOT NULL DEFAULT '0',
	PRIMARY KEY (`ID`)
)
COMMENT='This contains all the estimates for stories'
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

ALTER TABLE `estimates`
	ADD CONSTRAINT `FK_estimates_stories` FOREIGN KEY (`StoryID`) REFERENCES `stories` (`ID`);


