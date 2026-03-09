-- Add parent_phone to active_ble
ALTER TABLE active_ble ADD COLUMN IF NOT EXISTS parent_phone VARCHAR(20);
