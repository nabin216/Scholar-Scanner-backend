from rest_framework import throttling
import os


class LoginRateThrottle(throttling.AnonRateThrottle):
    """
    Throttle class specifically for login attempts.
    Limits the number of login attempts per IP address.
    """
    scope = 'login'
    
    def get_cache_key(self, request, view):
        # Use the client's IP address as the cache key
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    
    
class EmailVerificationRateThrottle(throttling.AnonRateThrottle):
    """
    Throttle class for email verification requests.
    Limits the number of verification emails sent based on a combination of IP and email.
    This provides better protection against abuse while being less restrictive for legitimate users.
    """
    scope = 'email_verification'
    
    def get_cache_key(self, request, view):
        # Get the client's IP address
        ident = self.get_ident(request)
        
        # Try to get email from request data
        email = None
        if request.data and 'email' in request.data:
            email = request.data.get('email', '').lower()
        
        # If we have an email, use a combination of IP and email hash as cache key
        # This allows legitimate users from shared IPs (coffee shops, universities, etc.)
        # to still use the system while preventing abuse
        if email:
            # Use only domain part of email to be less restrictive
            # This allows users to make multiple attempts with different email addresses
            # but prevents spamming a specific domain
            email_domain = email.split('@')[-1] if '@' in email else email
            return self.cache_format % {
                'scope': self.scope,
                'ident': f"{ident}:{email_domain}"
            }
        
        # Fallback to IP-only throttling if no email provided
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class RegistrationRateThrottle(throttling.AnonRateThrottle):
    """
    Throttle class for registration attempts.
    Limits the number of registration attempts per IP address.
    """
    scope = 'registration'
    
    def get_cache_key(self, request, view):
        # Use the client's IP address as the cache key
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
