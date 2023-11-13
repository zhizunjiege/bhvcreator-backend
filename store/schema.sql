PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for ruleset
-- ----------------------------
DROP TABLE IF EXISTS "ruleset";
CREATE TABLE "ruleset" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" text NOT NULL,
  "version" text NOT NULL,
  "description" text NOT NULL,
  "create_time" text,
  "update_time" text,
  "xml" text NOT NULL
);

-- ----------------------------
-- Triggers structure for table ruleset
-- ----------------------------
CREATE TRIGGER "on_insert_ruleset"
AFTER INSERT
ON "ruleset"
BEGIN
	UPDATE ruleset SET create_time=DATETIME('now','localtime') WHERE id=new.id;
END;
CREATE TRIGGER "on_update_ruleset"
AFTER UPDATE OF "id", "name", "version", "description", "create_time", "xml"
ON "ruleset"
BEGIN
	UPDATE ruleset SET update_time=DATETIME('now','localtime') WHERE id=new.id;
END;

PRAGMA foreign_keys = true;
