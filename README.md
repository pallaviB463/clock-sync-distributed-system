# Clock Sync

A Python-based distributed clock synchronization system that uses client-server architecture with cryptographic security. This project implements a network time synchronization protocol where clients request accurate time from a central server, using encrypted messages to ensure data integrity and confidentiality.

## Overview

Clock synchronization is critical in distributed systems where multiple machines need to maintain consistent timestamps. This implementation uses the Berkeley Algorithm approach combined with end-to-end encryption to synchronize client clocks with a master server.

## Features

- **Distributed Time Synchronization** - Synchronize clocks across multiple networked clients
- **Cryptographic Security** - All communications encrypted using Fernet (symmetric encryption)
- **UDP-based Communication** - Efficient, lightweight protocol for time exchange
- **Auto-generated Client IDs** - Unique identification for each client connection
- **Round-trip Time Calculation** - Accounts for network latency in time synchronization
- **Load Testing** - Built-in load testing tool to stress-test the synchronization system

## Architecture

### Protocol Flow

1. **Client** sends a `REQUEST_TIME` message with its timestamp (t1) and client ID
2. **Server** receives message at time t2, decrypts it, and generates response
3. **Server** sends back encrypted response with t2 and t3 (server's current time)
4. **Client** receives response at time t4 and calculates synchronized time

### Time Calculation

The client uses the formula to estimate clock offset:
```
offset = ((t2 - t1) + (t3 - t4)) / 2
synchronized_time = local_time + offset
```

### Components

- **server.py** - Listens on UDP port 5000 for client time requests
- **client.py** - Connects to server and synchronizes local clock
- **security.py** - Handles Fernet encryption/decryption using a shared secret key
- **load_test.py** - Tests system performance under concurrent client load

## Requirements

- Python 3.7+
- cryptography >= 41.0.0

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### Server
- **Port**: 5000 (UDP)
- **Bind Address**: 0.0.0.0 (all interfaces)
- **Encryption**: Fernet symmetric key (generated in security.py)

### Client
- **Target Server**: 127.0.0.1:5000 (localhost by default, modify SERVER_IP in client.py to connect remotely)
- **Client ID**: Randomly generated (1000-9999) on startup
- **Timeout**: 2 seconds for server response

## Usage

### Start the Server

```bash
python clock_sync/server.py
```

Expected output:
```
Server started... Waiting for clients
[SYNCHRONIZED] Client XXX offset: ±0.XXX seconds
```

### Run a Single Client

```bash
python clock_sync/client.py
```

Expected output:
```
[CLIENT STARTED] ID = XXXX
[TIME SYNC] Server time received, offset: ±0.XXX seconds
```

### Run Load Test

```bash
python clock_sync/load_test.py
```

This spawns multiple concurrent clients to test server performance and synchronization accuracy under load.

## Project Structure

```
clock-sync/
├── README.md
├── requirements.txt
├── .gitignore
└── clock_sync/
    ├── server.py        # UDP server for time synchronization
    ├── client.py        # UDP client for requesting synchronized time
    ├── security.py      # Encryption/decryption utilities
    └── load_test.py     # Load testing and stress testing
```

## Security Considerations

- The encryption key is hardcoded in security.py for development purposes
- For production use, securely manage encryption keys (environment variables, key management service)
- Uses Fernet (symmetric encryption) - ensure secure key distribution to all clients
- UDP is connectionless - consider adding sequence numbers for additional security in high-adversity environments

## Future Enhancements

- Asymmetric encryption (RSA) for secure key exchange
- NTP-like hierarchical time server architecture
- Persistent client state and synchronization history
- Configurable encryption algorithms
- Web dashboard for monitoring synchronized clients

## License

MIT License
