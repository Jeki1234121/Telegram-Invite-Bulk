#!/usr/bin/env python3
"""
Test script to verify the Telegram Bulk Invite Tool GUI can be initialized properly.
This test will create the GUI components without actually showing the window.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui_initialization():
    """Test that the GUI can be initialized without errors."""
    try:
        import tkinter as tk
        from telegram_bulk_invite import TelegramInviteTool
        
        # Create a root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Initialize the application
        app = TelegramInviteTool(root)
        
        # Verify that key components exist
        assert hasattr(app, 'notebook'), "Notebook widget not created"
        assert hasattr(app, 'file_tab'), "File tab not created"
        assert hasattr(app, 'invite_tab'), "Invite tab not created"
        assert hasattr(app, 'extract_tab'), "Extract tab not created"
        
        # Verify that key variables are initialized
        assert hasattr(app, 'api_id'), "API ID not set"
        assert hasattr(app, 'api_hash'), "API Hash not set"
        assert hasattr(app, 'processed_usernames'), "Processed usernames list not initialized"
        assert hasattr(app, 'is_inviting'), "Inviting flag not initialized"
        
        # Verify key methods exist
        assert hasattr(app, 'process_file'), "process_file method not found"
        assert hasattr(app, 'start_inviting'), "start_inviting method not found"
        assert hasattr(app, 'extract_members'), "extract_members method not found"
        
        # Clean up
        root.destroy()
        
        print("✓ GUI initialization test passed successfully!")
        print("✓ All required components are present")
        print("✓ All key methods are accessible")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install telethon pyrogram pandas tgcrypto")
        return False
        
    except Exception as e:
        print(f"✗ GUI initialization failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available."""
    try:
        import tkinter
        print("✓ tkinter available")
    except ImportError:
        print("✗ tkinter not available")
        return False
        
    try:
        import pandas
        print("✓ pandas available")
    except ImportError:
        print("✗ pandas not available - run: pip install pandas")
        return False
        
    try:
        import telethon
        print("✓ telethon available")
    except ImportError:
        print("✗ telethon not available - run: pip install telethon")
        return False
        
    try:
        import pyrogram
        print("✓ pyrogram available")
    except ImportError:
        print("✗ pyrogram not available - run: pip install pyrogram")
        return False
        
    return True

if __name__ == "__main__":
    print("Testing Telegram Bulk Invite Tool...")
    print("=" * 50)
    
    print("\n1. Testing dependencies...")
    deps_ok = test_dependencies()
    
    if deps_ok:
        print("\n2. Testing GUI initialization...")
        gui_ok = test_gui_initialization()
        
        if gui_ok:
            print("\n" + "=" * 50)
            print("🎉 All tests passed! The application is ready to use.")
            print("\nTo run the application:")
            print("python3 telegram_bulk_invite.py")
        else:
            print("\n" + "=" * 50)
            print("❌ GUI initialization failed. Check the error messages above.")
            sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("❌ Missing dependencies. Install them first:")
        print("pip install -r requirements.txt")
        sys.exit(1)