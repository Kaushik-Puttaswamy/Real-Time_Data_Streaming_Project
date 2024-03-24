#!/bin/bash

# Define functions
usage() {
    echo "Usage: $0 [-h host] [-p port] [-t timeout] [-c command] [-s]"
    echo "  -h: Hostname or IP address (default: localhost)"
    echo "  -p: Port number (default: 9092)"
    echo "  -t: Timeout in seconds (default: 60)"
    echo "  -c: Command to execute if the test succeeds (optional)"
    echo "  -s: Strict mode - do not execute command if the test fails"
    exit 1
}

wait_for_port() {
    local host="$1"
    local port="$2"
    local timeout="$3"
    local start_time=$(date +%s)
    local end_time=$((start_time + timeout))
    while true; do
        if nc -z "$host" "$port"; then
            echo "Port $port on host $host is available"
            return 0
        fi
        if [ "$(date +%s)" -ge "$end_time" ]; then
            echo "Timeout exceeded while waiting for port $port on host $host"
            return 1
        fi
        sleep 1
    done
}

# Set default values
host="localhost"
port="9092"
timeout="60"
strict_mode=false

# Parse command-line arguments
while getopts ":h:p:t:c:s" opt; do
    case ${opt} in
        h )
            host="$OPTARG"
            ;;
        p )
            port="$OPTARG"
            ;;
        t )
            timeout="$OPTARG"
            ;;
        c )
            command_to_execute="$OPTARG"
            ;;
        s )
            strict_mode=true
            ;;
        \? )
            usage
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            usage
            ;;
    esac
done
shift $((OPTIND -1))

# Validate arguments
if ! [[ "$port" =~ ^[0-9]+$ ]]; then
    echo "Invalid port number: $port"
    usage
fi
if ! [[ "$timeout" =~ ^[0-9]+$ ]]; then
    echo "Invalid timeout: $timeout"
    usage
fi

# Wait for port to become available
if ! wait_for_port "$host" "$port" "$timeout"; then
    if [ "$strict_mode" = true ]; then
        echo "Exiting due to failure in strict mode"
        exit 1
    else
        echo "Continuing execution despite failure"
    fi
fi

# Execute command if provided
if [ -n "$command_to_execute" ]; then
    echo "Executing command: $command_to_execute"
    eval "$command_to_execute"
fi

exit 0
