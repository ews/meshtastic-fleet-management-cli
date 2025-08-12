#!/usr/bin/env python3

import subprocess
import re
import sys

def find_nodes():
    """
    Runs 'meshtastic --nodes' and extracts all node IDs,
    then prints them as a comma-separated string.
    """
    print("Querying the mesh for a list of all nodes...")
    print("This can take a few moments...\n")
    
    try:
        # The command to run to get the list of nodes
        command = ["meshtastic", "--nodes"]
        
        # Execute the command
        # Using text=True to get stdout/stderr as strings
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True  # This will raise an exception for non-zero exit codes
        )

        output = result.stdout
        
        # In the standard table output of 'meshtastic --nodes', node IDs are
        # typically prefixed with '!' and are hexadecimal strings.
        # This regex looks for a '!' followed by one or more hex characters (0-9, a-f).
        # It's a robust way to find node IDs in the output.
        node_id_pattern = re.compile(r'(![0-9a-fA-F]+)')
        
        # Find all matches in the command's output
        node_ids = node_id_pattern.findall(output)

        if not node_ids:
            print("No remote node IDs found in the output of 'meshtastic --nodes'.")
            print("Ensure your device is connected and can see other nodes on the mesh.")
            sys.exit(1)
            
        # Join the found node IDs with a comma
        nodes_str = ",".join(node_ids)

        print("Found the following remote node IDs:")
        print(nodes_str)
        print("\nTo use these with the meshtastic_all.py script, run:")
        print(f'export MESHTASTIC_REMOTE_NODES="{nodes_str}"')

    except FileNotFoundError:
        print("Error: The 'meshtastic' command was not found.", file=sys.stderr)
        print("Please ensure the Meshtastic Python CLI is installed and in your system's PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'meshtastic --nodes':", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    find_nodes()

