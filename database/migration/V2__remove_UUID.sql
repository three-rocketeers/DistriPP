ALTER TABLE `stories` DROP FOREIGN KEY `FK_stories_planning`;
ALTER TABLE `planning` MODIFY `ID` BIGINT NOT NULL AUTO_INCREMENT;
ALTER TABLE `planning` ADD CONSTRAINT `PlanningName_unique` UNIQUE (Title);
ALTER TABLE `stories` MODIFY `PlanningID` BIGINT NOT NULL ;
ALTER TABLE `stories` ADD CONSTRAINT `FK_stories_planning` FOREIGN KEY (`PlanningID`) REFERENCES `planning` (`ID`);