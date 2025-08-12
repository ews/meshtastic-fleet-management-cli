# Makefile for managing meshtastic remote nodes via the meshtastic_all.py script.

# Define the script to be executed.
# Ensure meshtastic_all.py is in the same directory and is executable (chmod +x meshtastic_all.py).
MESHTASTIC_ALL_SCRIPT := ./meshtastic_all.py

# --- Arguments for 'move_to_public' target ---
# --set lora.channel_num 31: Sets the Lora channel to 31.
# --set lora.modem_preset SHORT_TURBO: Changes the modem preset for faster communication.
# --set position.gps_update_interval 300: Sets GPS position reporting to every 5 minutes (300 seconds).
PUBLIC_ARGS = \
	--set lora.channel_num 31 \
	--set lora.modem_preset SHORT_TURBO \
	--set position.gps_update_interval 300

# --- Arguments for 'move_to_kaleidoscope' target ---
# --set lora.channel_num 18: Sets the Lora channel to 18.
# --set lora.modem_preset MEDIUM_FAST: A balanced modem preset.
# --set position.gps_update_interval 30: Sets GPS position reporting to every 30 seconds.
KALEIDOSCOPE_ARGS = \
	--set lora.channel_num 18 \
	--set lora.modem_preset MEDIUM_FAST \
	--set position.gps_update_interval 30

# --- Arguments for setting only the modem preset ---
SHORT_TURBO_ARGS = --set lora.modem_preset SHORT_TURBO
MEDIUM_FAST_ARGS = --set lora.modem_preset MEDIUM_FAST

# Phony targets don't represent files. This prevents make from getting confused
# if a file with the same name as a target exists.
.PHONY: move_to_public move_to_kaleidoscope set_short_turbo set_medium_fast

# Target to move all remote nodes to a public channel configuration.
# To run this, simply type 'make move_to_public' in your terminal.
move_to_public:
	@echo ">>> Applying public channel settings to all remote nodes..."
	@echo "    - Frequency Slot: 31"
	@echo "    - Modem Preset:   SHORT_TURBO"
	@echo "    - GPS Interval:   5 minutes (300s)"
	@echo "-------------------------------------------------------------"
	@$(MESHTASTIC_ALL_SCRIPT) $(PUBLIC_ARGS)
	@echo "-------------------------------------------------------------"
	@echo ">>> Task 'move_to_public' complete."

# Target to move all remote nodes to the Kaleidoscope channel configuration.
# To run this, simply type 'make move_to_kaleidoscope' in your terminal.
move_to_kaleidoscope:
	@echo ">>> Applying Kaleidoscope channel settings to all remote nodes..."
	@echo "    - Frequency Slot: 18"
	@echo "    - Modem Preset:   MEDIUM_FAST"
	@echo "    - GPS Interval:   30 seconds"
	@echo "-------------------------------------------------------------"
	@$(MESHTASTIC_ALL_SCRIPT) $(KALEIDOSCOPE_ARGS)
	@echo "-------------------------------------------------------------"
	@echo ">>> Task 'move_to_kaleidoscope' complete."

# Target to set the modem preset to SHORT_TURBO for all remote nodes.
# To run this, simply type 'make set_short_turbo' in your terminal.
set_short_turbo:
	@echo ">>> Setting modem preset to SHORT_TURBO for all remote nodes..."
	@echo "-------------------------------------------------------------"
	@$(MESHTASTIC_ALL_SCRIPT) $(SHORT_TURBO_ARGS)
	@echo "-------------------------------------------------------------"
	@echo ">>> Task 'set_short_turbo' complete."

# Target to set the modem preset to MEDIUM_FAST for all remote nodes.
# To run this, simply type 'make set_medium_fast' in your terminal.
set_medium_fast:
	@echo ">>> Setting modem preset to MEDIUM_FAST for all remote nodes..."
	@echo "-------------------------------------------------------------"
	@$(MESHTASTIC_ALL_SCRIPT) $(MEDIUM_FAST_ARGS)
	@echo "-------------------------------------------------------------"
	@echo ">>> Task 'set_medium_fast' complete."


