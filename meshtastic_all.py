#!/usr/bin/env python3

import os
import subprocess
import sys

# Name of the environment variable that holds the comma-separated list of node IDs
REMOTE_NODES_ENV_VAR = "MESHTASTIC_REMOTE_NODES"

def load_dotenv(filepath='.env'):
    """
    Loads environment variables from a .env file.
    Gives precedence to already-set environment variables.
    """
    if not os.path.exists(filepath):
        return # No .env file found, do nothing

    try:
        with open(filepath) as f:
            for line in f:
                # Ignore comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Split on the first equals sign
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove surrounding quotes from value if present
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                        
                    # Set the environment variable only if it's not already set
                    os.environ.setdefault(key, value)
    except Exception as e:
        print(f"Warning: Could not parse .env file: {e}", file=sys.stderr)


def main():
    """
    Main function to execute Meshtastic commands on multiple remote nodes.
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Get the list of remote node IDs from the environment variable
    nodes_str = os.environ.get(REMOTE_NODES_ENV_VAR)

    if not nodes_str:
        print(f"Error: Environment variable {REMOTE_NODES_ENV_VAR} is not set or is empty.", file=sys.stderr)
        print(f"Please set it in your shell or create a .env file with the following format:", file=sys.stderr)
        print(f"Example .env file content:", file=sys.stderr)
        print(f"MESHTASTIC_REMOTE_NODES=!node1id,!node2id,node3id", file=sys.stderr)
        sys.exit(1)

    # Split the string into a list of node IDs and strip any whitespace
    raw_node_ids = [node.strip() for node in nodes_str.split(',') if node.strip()]

    if not raw_node_ids:
        print(f"Error: No node IDs found in {REMOTE_NODES_ENV_VAR} after parsing.", file=sys.stderr)
        sys.exit(1)

    # Process node IDs to ensure they start with '!'
    node_ids = []
    for node_id in raw_node_ids:
        if not node_id.startswith('!'):
            node_ids.append(f"!{node_id}")
        else:
            node_ids.append(node_id)
    
    print(f"Found {len(node_ids)} remote node(s) to target: {', '.join(node_ids)}")

    # Get the arguments passed to this script, which will be forwarded to meshtastic
    script_args = sys.argv[1:]

    if not script_args:
        print("Usage: ./meshtastic_all.py <meshtastic_arguments>")
        print("Example: ./meshtastic_all.py --set lora.modem_preset 'MEDIUM_FAST' --set lora.region 'US'")
        print("This script requires arguments to pass to the meshtastic CLI.")
        sys.exit(1)

    print(f"Will attempt to send arguments: {' '.join(script_args)}\n")

    success_count = 0
    failure_count = 0

    for node_id in node_ids:
        # Construct the command
        base_command = ["meshtastic", "--dest", node_id, "--remoteadmin"]
        full_command = base_command + script_args

        print(f"--------------------------------------------------")
        print(f"Executing for node: {node_id}")
        print(f"Command: {' '.join(full_command)}")
        print(f"--------------------------------------------------")

        try:
            # Execute the command
            result = subprocess.run(full_command, capture_output=True, text=True, check=False)

            if result.stdout:
                print("Output:\n" + result.stdout.strip())
            
            if result.stderr:
                print("Errors/Warnings:\n" + result.stderr.strip(), file=sys.stderr)

            if result.returncode == 0:
                print(f"\nSuccessfully executed command for node {node_id}.")
                success_count += 1
            else:
                print(f"\nCommand for node {node_id} failed with exit code {result.returncode}.", file=sys.stderr)
                failure_count += 1

        except FileNotFoundError:
            print(f"Error: The 'meshtastic' command was not found. Is it installed and in your PATH?", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while processing node {node_id}: {e}", file=sys.stderr)
            failure_count += 1
        
        print("\n")

    print("==================================================")
    print("Summary:")
    print(f"Successfully executed commands for {success_count} node(s).")
    print(f"Failed to execute commands for {failure_count} node(s).")
    print("==================================================")

    if failure_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

