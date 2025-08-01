import subprocess
import sys
import os
from typing import Optional

def install_package(package: str, upgrade: bool = False, dev: bool = False, user: bool = False) -> str:
    """Install Python packages using pip."""
    try:
        # Validate parameters
        if not package:
            raise ValueError("Package name cannot be empty")
        
        # Prepare command
        cmd = [sys.executable, "-m", "pip", "install"]
        
        if upgrade:
            cmd.append("--upgrade")
        
        if dev:
            cmd.append("--editable")
        
        if user:
            cmd.append("--user")
        
        cmd.append(package)
        
        # Execute installation
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes timeout for package installation
            cwd=os.getcwd()
        )
        
        # Format output
        output = []
        output.append(f"📦 Installing package: {package}")
        output.append(f"🔧 Upgrade: {upgrade}")
        output.append(f"🔧 Dev mode: {dev}")
        output.append(f"🔧 User install: {user}")
        output.append(f"📊 Exit Code: {result.returncode}")
        
        if result.stdout:
            output.append(f"\n📤 STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output.append(f"\n⚠️  STDERR:\n{result.stderr}")
        
        # Interpret results
        if result.returncode == 0:
            output.append(f"\n✅ Successfully installed {package}")
        elif result.returncode == 1:
            output.append(f"\n❌ Failed to install {package}")
        else:
            output.append(f"\n❓ Unexpected exit code: {result.returncode}")
        
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        raise Exception(f"Package installation timed out after 5 minutes")
    except Exception as e:
        raise Exception(f"Error installing package {package}: {str(e)}")

# Tool definition
INSTALL_PACKAGE_DEFINITION = {
    "name": "install_package",
    "description": "Install Python packages using pip.",
    "input_schema": {
        "type": "object",
        "properties": {
            "package": {
                "type": "string",
                "description": "The package name to install (e.g., 'requests', 'pytest')."
            },
            "upgrade": {
                "type": "boolean",
                "description": "Whether to upgrade the package if already installed. Defaults to False.",
                "default": False
            },
            "dev": {
                "type": "boolean",
                "description": "Whether to install in development mode (--editable). Defaults to False.",
                "default": False
            },
            "user": {
                "type": "boolean",
                "description": "Whether to install for current user only (--user). Defaults to False.",
                "default": False
            }
        },
        "required": ["package"],
        "additionalProperties": False
    },
    "tool_function": install_package
} 