import os
import sys
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.models.user import User, db

class AccountManager:
    def __init__(self):
        self.audit_log = []
    
    def delete_user_account(self, user_id):
        """Delete a user account and all associated data"""
        try:
 
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found',
                    'message': 'No user found with the provided ID'
                }
            
  
            user_info = {
                'id': user.id,
                'email': user.email,
                'full_name': user.get_full_name(),
                'deleted_at': datetime.now().isoformat()
            }
            
         
            if hasattr(user, 'watchlist') and user.watchlist:
                user.watchlist = []
            
            db.session.delete(user)
            db.session.commit()
            
   
            self.audit_log.append({
                'action': 'account_deleted',
                'user_info': user_info,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'success': True,
                'message': 'Account successfully deleted',
                'user_info': {
                    'email': user_info['email'],
                    'full_name': user_info['full_name']
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to delete account. Please try again.'
            }
    
    def get_account_info(self, user_id):
        """Get user account information"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            return {
                'success': True,
                'user_info': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': user.get_full_name(),
                    'created_at': user.created_at.isoformat() if user.created_at else None,
                    'watchlist_count': len(user.get_watchlist()) if user.get_watchlist() else 0
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve account information'
            }
    
    def export_user_data(self, user_id):
        """Export user data before deletion"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            user_data = {
                'account_info': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                },
                'watchlist': user.get_watchlist() if user.get_watchlist() else [],
                'exported_at': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'user_data': user_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to export user data'
            }
    
    def get_audit_log(self):
        """Get audit log of account deletions"""
        return {
            'success': True,
            'audit_log': self.audit_log,
            'total_deletions': len(self.audit_log)
        } 