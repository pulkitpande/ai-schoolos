# AI SchoolOS Enhanced Backend Starter

This enhanced backend starter provides a comprehensive solution for managing and starting the AI SchoolOS backend services without Docker.

## Features

- ✅ **Multi-service support** - Install and start any combination of 17+ services
- ✅ **Virtual environment management** - Automatic setup and activation
- ✅ **Dependency management** - Install dependencies for specific services or all services
- ✅ **Service startup** - Start services individually or in groups
- ✅ **Error handling** - Comprehensive error reporting and recovery
- ✅ **Cross-platform** - Works on Windows, Linux, and macOS
- ✅ **Command-line interface** - Easy-to-use CLI with help system

## Available Services

| Service | Description |
|---------|-------------|
| `api-gateway` | API Gateway |
| `auth-service` | Authentication Service |
| `student-service` | Student Management Service |
| `staff-service` | Staff Management Service |
| `ai-service` | AI/ML Service |
| `analytics-service` | Analytics Service |
| `notification-service` | Notification Service |
| `communication-service` | Communication Service |
| `attendance-service` | Attendance Service |
| `timetable-service` | Timetable Service |
| `exam-service` | Exam Management Service |
| `library-service` | Library Service |
| `homework-service` | Homework Service |
| `fee-service` | Fee Management Service |
| `transport-service` | Transport Service |
| `config-service` | Configuration Service |
| `super-admin-service` | Super Admin Service |

## Quick Start

### Windows Users
```batch
# Show help
start-backend-enhanced.bat

# Install all dependencies
start-backend-enhanced.bat install

# Install specific services
start-backend-enhanced.bat install auth-service student-service

# Start services
start-backend-enhanced.bat start auth-service student-service

# Check requirements
start-backend-enhanced.bat check

# Setup virtual environment
start-backend-enhanced.bat setup
```

### Cross-platform (Python)
```bash
# Show help
python start-backend-simple.py

# Install all dependencies
python start-backend-simple.py install

# Install specific services
python start-backend-simple.py install auth-service student-service

# Start services
python start-backend-simple.py start auth-service student-service

# Check requirements
python start-backend-simple.py check

# Setup virtual environment
python start-backend-simple.py setup
```

## Commands

### `install [services]`
Install dependencies for specified services or all services if none specified.

**Examples:**
```bash
# Install all services
python start-backend-simple.py install

# Install specific services
python start-backend-simple.py install auth-service student-service ai-service
```

### `start [services]`
Start specified services. If no services specified, starts auth-service and student-service by default.

**Examples:**
```bash
# Start default services (auth-service, student-service)
python start-backend-simple.py start

# Start specific services
python start-backend-simple.py start auth-service student-service ai-service
```

### `check`
Check if all required files and directories exist.

**Example:**
```bash
python start-backend-simple.py check
```

### `setup`
Set up virtual environment if it doesn't exist.

**Example:**
```bash
python start-backend-simple.py setup
```

### `help`
Show help information and available commands.

**Example:**
```bash
python start-backend-simple.py help
```

## Directory Structure

```
ai-schoolos/
├── backend/
│   ├── api-gateway/
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── services/
│   │   ├── auth-service/
│   │   │   ├── main.py
│   │   │   └── requirements.txt
│   │   ├── student-service/
│   │   │   ├── main.py
│   │   │   └── requirements.txt
│   │   └── ... (other services)
│   └── shared/
│       └── requirements.txt
├── start-backend-simple.py
├── start-backend-enhanced.bat
└── BACKEND_STARTER_README.md
```

## Requirements

- Python 3.7 or higher
- pip (Python package installer)
- All services must have a `main.py` file in their directory
- All services must have a `requirements.txt` file in their directory

## Error Handling

The script includes comprehensive error handling:

- **Missing directories**: Warns if backend directory is missing
- **Missing requirements.txt**: Skips services without requirements files
- **Installation failures**: Reports specific errors with stdout/stderr
- **Service startup failures**: Continues with other services if one fails
- **Virtual environment issues**: Handles activation script detection

## Troubleshooting

### Common Issues

1. **"backend directory not found"**
   - Make sure you're running the script from the project root directory
   - Ensure the backend folder exists

2. **"Python is not installed"**
   - Install Python 3.7+ from python.org
   - Add Python to your system PATH

3. **"requirements.txt not found"**
   - This is a warning, not an error
   - The script will skip services without requirements files
   - Create requirements.txt files for missing services

4. **"main.py not found"**
   - Ensure each service has a main.py file
   - Check the service directory structure

5. **"Virtual environment activation script not found"**
   - The script will create a new virtual environment
   - This is normal for first-time setup

### Getting Help

```bash
# Show all available commands
python start-backend-simple.py help

# Check system requirements
python start-backend-simple.py check

# Get detailed error information
python start-backend-simple.py install 2>&1 | tee install.log
```

## Development

### Adding New Services

1. Create the service directory: `backend/services/new-service/`
2. Add `main.py` and `requirements.txt` files
3. Update the `services` dictionary in `BackendStarter.__init__()`

### Customizing the Script

The script is designed to be easily extensible:

- Add new commands by extending the argument parser
- Add new service types by modifying the `services` dictionary
- Customize error handling in the `run_command` method
- Modify startup behavior in the `start_services` method

## License

This script is part of the AI SchoolOS project and follows the same license terms. 