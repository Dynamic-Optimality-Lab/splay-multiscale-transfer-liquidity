# Audit format correction with the failed artifacts preserved

The first producer completed the new fixed witness calculations, then stopped while comparing the regenerated inherited SC rows with their saved JSON. Tuple-valued source events were being compared directly with JSON arrays. This was a serialization-type mismatch in the preservation check, not a failed mathematical witness or an altered charging condition.

The initial `audit_delayed_shallow.py` and `entry_source_pins.json` are preserved. The exclusive new version `audit_delayed_shallow_v002.py` changes only the entry output filename to `entry_source_pins_v002.json` and normalizes the compared row through JSON before equality checking. It changes no source request, tree, threshold, count, scan rule or allocation.

The independent verifier checks this exact two-change relationship between the scripts, replays all old and new rows through the pointer source, and passes. The final seal checks both entry pin inventories and includes both script versions and this correction record in the delivery manifest. No old file was overwritten, and the four-rule gate and fixed audit scope remain unchanged.
