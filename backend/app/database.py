from supabase import create_client, Client
from app.config import settings


class SupabaseDB:
    """Supabase database client wrapper"""
    
    _client: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        if cls._client is None:
            cls._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return cls._client
    
    @classmethod
    def get_service_client(cls) -> Client:
        """Get Supabase client with service role key for admin operations"""
        return create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )


# Convenience function to get database client
def get_db() -> Client:
    """Get Supabase database client"""
    return SupabaseDB.get_client()

