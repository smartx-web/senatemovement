ALTER TABLE pus DROP CONSTRAINT IF EXISTS pus_lga_check;
ALTER TABLE pus ADD CONSTRAINT pus_lga_check CHECK(lga IN ('Ado','Agatu','Apa','Obi','Ogbadibo','Ohimini','Oju','Okpokwu','Otukpo'));
INSERT INTO schema_migrations(version) VALUES(3) ON CONFLICT(version) DO NOTHING;
