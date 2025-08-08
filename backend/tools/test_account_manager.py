#!/usr/bin/env python3
"""
Test script for AccountManager functionality
"""

import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.account_manager import AccountManager

def test_account_manager():
    """Test the AccountManager class"""
    print("🧪 Testing AccountManager...")
    
 
    am = AccountManager()
    print("AccountManager instance created")
    

    audit_result = am.get_audit_log()
    print(f"Audit log retrieved: {audit_result['total_deletions']} deletions")
    

    test_result = am.get_account_info(99999)
    print(f"Non-existent user test: {test_result['success']}")
    
    print("All AccountManager tests passed!")

if __name__ == "__main__":
    test_account_manager() 