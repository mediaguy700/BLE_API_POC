"""Active BLE API: insert into active_ble; error if mac already exists."""
import json
from src.db import get_conn, api_response

ACTIVE_BLE_RETURNING = "id, mac, active, lname, fname, parent_id, duration, parent_fname, parent_lname, parent_phone"


def _parse_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return None


def create_active_ble(event, context):
    """POST /active-ble - Insert row. Returns 409 with 'User Exists' if mac already in table."""
    body = _parse_body(event)
    if not body:
        return api_response({"error": "Invalid JSON"}, 400)
    mac = (body.get("mac") or "").strip()
    if not mac:
        return api_response({"error": "mac required"}, 400)
    if len(mac) > 17:
        return api_response({"error": "mac max length 17"}, 400)
    active = body.get("active")
    if active is None:
        active = True
    lname = (body.get("lname") or "").strip() or None
    fname = (body.get("fname") or "").strip() or None
    if lname and len(lname) > 17:
        lname = lname[:17]
    if fname and len(fname) > 17:
        fname = fname[:17]
    parent_id = body.get("parent_id")
    if parent_id is not None and parent_id != "":
        try:
            parent_id = int(parent_id)
        except (TypeError, ValueError):
            parent_id = None
    else:
        parent_id = None
    duration = body.get("duration")
    if duration is not None and duration != "":
        try:
            duration = int(duration)
        except (TypeError, ValueError):
            duration = None
    else:
        duration = None
    parent_fname = (body.get("parent_fname") or "").strip() or None
    parent_lname = (body.get("parent_lname") or "").strip() or None
    if parent_fname and len(parent_fname) > 17:
        parent_fname = parent_fname[:17]
    if parent_lname and len(parent_lname) > 17:
        parent_lname = parent_lname[:17]
    parent_phone = (body.get("parent_phone") or "").strip() or None
    if parent_phone and len(parent_phone) > 20:
        parent_phone = parent_phone[:20]

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM active_ble WHERE mac = %s", (mac,))
            existing = cur.fetchone()
        if existing:
            return api_response({"error": "User Exists"}, 409)
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO active_ble (mac, active, lname, fname, parent_id, duration, parent_fname, parent_lname, parent_phone)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                   RETURNING """ + ACTIVE_BLE_RETURNING,
                (mac, bool(active), lname, fname, parent_id, duration, parent_fname, parent_lname, parent_phone),
            )
            row = cur.fetchone()
        conn.commit()
        out = dict(row) if row else {}
        for k, v in list(out.items()):
            if hasattr(v, "isoformat"):
                out[k] = v.isoformat()
            elif hasattr(v, "hex"):
                out[k] = str(v)
        return api_response(out, 201)
    except Exception as e:
        conn.rollback()
        return api_response({"error": str(e)}, 500)
    finally:
        conn.close()


def _serialize_row(row):
    if not row:
        return None
    out = dict(row)
    for k, v in list(out.items()):
        if hasattr(v, "isoformat"):
            out[k] = v.isoformat()
        elif hasattr(v, "hex"):
            out[k] = str(v)
    return out


def list_active_ble(event, context):
    """GET /active-ble - List all active_ble rows."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT " + ACTIVE_BLE_RETURNING + " FROM active_ble ORDER BY id")
            rows = cur.fetchall()
        return api_response({"active_ble": [_serialize_row(r) for r in rows]})
    finally:
        conn.close()


def get_active_ble(event, context):
    """GET /active-ble/{id} - Get one active_ble row by id."""
    pid = (event.get("pathParameters") or {}).get("id")
    if not pid:
        return api_response({"error": "id required"}, 400)
    try:
        row_id = int(pid)
    except (TypeError, ValueError):
        return api_response({"error": "id must be an integer"}, 400)
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT " + ACTIVE_BLE_RETURNING + " FROM active_ble WHERE id = %s", (row_id,))
            row = cur.fetchone()
        if not row:
            return api_response({"error": "Not found"}, 404)
        return api_response(_serialize_row(row))
    finally:
        conn.close()


def update_active_ble(event, context):
    """PATCH /active-ble/{id} - Update row by id. Returns 409 'User Exists' if new mac already in table."""
    pid = (event.get("pathParameters") or {}).get("id")
    if not pid:
        return api_response({"error": "id required"}, 400)
    try:
        row_id = int(pid)
    except (TypeError, ValueError):
        return api_response({"error": "id must be an integer"}, 400)
    body = _parse_body(event)
    if not body:
        return api_response({"error": "Invalid JSON"}, 400)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, mac FROM active_ble WHERE id = %s", (row_id,))
            existing = cur.fetchone()
        if not existing:
            return api_response({"error": "Not found"}, 404)
        updates = []
        params = []
        if "mac" in body:
            mac = (body.get("mac") or "").strip()
            if len(mac) > 17:
                return api_response({"error": "mac max length 17"}, 400)
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM active_ble WHERE mac = %s AND id != %s", (mac, row_id))
                if cur.fetchone():
                    return api_response({"error": "User Exists"}, 409)
            updates.append("mac = %s")
            params.append(mac)
        if "active" in body:
            updates.append("active = %s")
            params.append(bool(body["active"]))
        if "lname" in body:
            lname = (body.get("lname") or "").strip() or None
            if lname and len(lname) > 17:
                lname = lname[:17]
            updates.append("lname = %s")
            params.append(lname)
        if "fname" in body:
            fname = (body.get("fname") or "").strip() or None
            if fname and len(fname) > 17:
                fname = fname[:17]
            updates.append("fname = %s")
            params.append(fname)
        if "parent_id" in body:
            v = body["parent_id"]
            if v is None or v == "":
                parent_id = None
            else:
                try:
                    parent_id = int(v)
                except (TypeError, ValueError):
                    parent_id = None
            updates.append("parent_id = %s")
            params.append(parent_id)
        if "duration" in body:
            v = body["duration"]
            if v is None or v == "":
                duration = None
            else:
                try:
                    duration = int(v)
                except (TypeError, ValueError):
                    duration = None
            updates.append("duration = %s")
            params.append(duration)
        if "parent_fname" in body:
            v = (body.get("parent_fname") or "").strip() or None
            if v and len(v) > 17:
                v = v[:17]
            updates.append("parent_fname = %s")
            params.append(v)
        if "parent_lname" in body:
            v = (body.get("parent_lname") or "").strip() or None
            if v and len(v) > 17:
                v = v[:17]
            updates.append("parent_lname = %s")
            params.append(v)
        if "parent_phone" in body:
            v = (body.get("parent_phone") or "").strip() or None
            if v and len(v) > 20:
                v = v[:20]
            updates.append("parent_phone = %s")
            params.append(v)
        if not updates:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT " + ACTIVE_BLE_RETURNING + " FROM active_ble WHERE id = %s",
                    (row_id,),
                )
                row = cur.fetchone()
            return api_response(_serialize_row(row), 200)
        params.append(row_id)
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE active_ble SET " + ", ".join(updates) + " WHERE id = %s RETURNING " + ACTIVE_BLE_RETURNING,
                params,
            )
            row = cur.fetchone()
        conn.commit()
        return api_response(_serialize_row(row), 200)
    except Exception as e:
        conn.rollback()
        return api_response({"error": str(e)}, 500)
    finally:
        conn.close()
