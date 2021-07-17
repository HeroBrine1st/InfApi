-- upgrade --
ALTER TABLE `task` ADD `solution` LONGTEXT NOT NULL;
-- downgrade --
ALTER TABLE `task` DROP COLUMN `solution`;
