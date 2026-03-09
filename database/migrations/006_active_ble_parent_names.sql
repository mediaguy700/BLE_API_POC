-- Add parent_fname and parent_lname to active_ble
ALTER TABLE active_ble ADD COLUMN IF NOT EXISTS parent_fname VARCHAR(17);
ALTER TABLE active_ble ADD COLUMN IF NOT EXISTS parent_lname VARCHAR(17);
