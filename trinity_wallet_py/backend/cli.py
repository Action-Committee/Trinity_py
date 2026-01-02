#!/usr/bin/env python3
"""
Trinity Backend CLI

Command-line interface for managing Trinity backend services.
"""

import sys
import argparse
import json
from pathlib import Path

from .server import TrinityBackendServer
from .config import BackendConfig


def cmd_start(args):
    """Start the backend server."""
    config = BackendConfig(args.config)
    
    # Override config with command line arguments
    if args.host:
        config.set('server.host', args.host)
    if args.port:
        config.set('server.port', args.port)
    if args.debug:
        config.set('server.debug', True)
    
    print("Starting Trinity Backend Server...")
    print(f"Configuration: {config.config_path}")
    
    server = TrinityBackendServer(config)
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop_services()


def cmd_config(args):
    """Manage backend configuration."""
    config = BackendConfig(args.config)
    
    if args.show:
        # Show current configuration
        print(json.dumps(config.config, indent=2))
    
    elif args.init:
        # Initialize default configuration
        config.save()
        print(f"Configuration initialized at: {config.config_path}")
    
    elif args.set:
        # Set configuration value
        key, value = args.set.split('=', 1)
        
        # Try to parse value as JSON
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass  # Keep as string
        
        config.set(key, value)
        config.save()
        print(f"Set {key} = {value}")
    
    elif args.get:
        # Get configuration value
        value = config.get(args.get)
        print(f"{args.get} = {value}")


def cmd_status(args):
    """Check backend service status."""
    import requests
    
    config = BackendConfig(args.config)
    host = config.get('server.host', '127.0.0.1')
    port = config.get('server.port', 5000)
    
    base_url = f"http://{host}:{port}"
    
    try:
        # Check health
        response = requests.get(f"{base_url}/health", timeout=5)
        data = response.json()
        
        print("Trinity Backend Server Status")
        print("=" * 50)
        print(f"Status: {data.get('status', 'unknown')}")
        print("\nServices:")
        
        for service, running in data.get('services', {}).items():
            status = "Running" if running else "Stopped"
            print(f"  {service}: {status}")
        
    except requests.exceptions.ConnectionError:
        print("Error: Backend server is not running")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_test(args):
    """Test backend functionality."""
    print("Testing Trinity Backend Services...")
    
    config = BackendConfig(args.config)
    
    # Test configuration
    print("\n1. Configuration Test")
    print(f"   Config path: {config.config_path}")
    print(f"   Server host: {config.get('server.host')}")
    print(f"   Server port: {config.get('server.port')}")
    print("   ✓ Configuration loaded")
    
    # Test service initialization
    print("\n2. Service Initialization Test")
    try:
        server = TrinityBackendServer(config)
        print(f"   Initialized {len(server.services)} services")
        
        for name in server.services:
            print(f"   ✓ {name} service created")
        
    except Exception as e:
        print(f"   ✗ Error initializing services: {e}")
        return 1
    
    print("\n✓ All tests passed")
    return 0


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Trinity Backend Service Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start the backend server
  trinity-backend start
  
  # Start with custom host and port
  trinity-backend start --host 0.0.0.0 --port 8000
  
  # Initialize configuration
  trinity-backend config --init
  
  # Show configuration
  trinity-backend config --show
  
  # Set configuration value
  trinity-backend config --set server.port=8000
  
  # Check server status
  trinity-backend status
  
  # Test services
  trinity-backend test
        """
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file',
        default=None
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the backend server')
    start_parser.add_argument('--host', help='Server host')
    start_parser.add_argument('--port', type=int, help='Server port')
    start_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    start_parser.set_defaults(func=cmd_start)
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_group = config_parser.add_mutually_exclusive_group(required=True)
    config_group.add_argument('--show', action='store_true', help='Show configuration')
    config_group.add_argument('--init', action='store_true', help='Initialize configuration')
    config_group.add_argument('--set', help='Set configuration value (key=value)')
    config_group.add_argument('--get', help='Get configuration value')
    config_parser.set_defaults(func=cmd_config)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check server status')
    status_parser.set_defaults(func=cmd_status)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test backend services')
    test_parser.set_defaults(func=cmd_test)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        return args.func(args) or 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
