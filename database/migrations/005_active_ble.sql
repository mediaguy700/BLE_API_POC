-- Active BLE table: id, mac, active, lname, fname, parent_id, duration
CREATE TABLE IF NOT EXISTS active_ble (
  id BIGSERIAL PRIMARY KEY,
  mac VARCHAR(17),
  active BOOLEAN,
  lname VARCHAR(17),
  fname VARCHAR(17),
  parent_id BIGINT REFERENCES active_ble(id) ON DELETE SET NULL,
  duration INTEGER
);

CREATE INDEX IF NOT EXISTS idx_active_ble_mac ON active_ble(mac);
CREATE INDEX IF NOT EXISTS idx_active_ble_parent_id ON active_ble(parent_id);
CREATE INDEX IF NOT EXISTS idx_active_ble_active ON active_ble(active);
