"""
Database Setup Script for AI Research Deck

This script provides the SQL commands needed to set up the database tables in Supabase.
Run these commands in your Supabase SQL editor.
"""

def get_database_schema():
    """Return the SQL commands to create the necessary tables"""
    return """
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create summaries table (updated to include user_id)
CREATE TABLE IF NOT EXISTS summaries (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_summaries_user_id ON summaries(user_id);
CREATE INDEX IF NOT EXISTS idx_summaries_created_at ON summaries(created_at);

-- Enable Row Level Security (RLS) for better security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE summaries ENABLE ROW LEVEL SECURITY;

-- Create policies for users table
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update their own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Create policies for summaries table
CREATE POLICY "Users can view their own summaries" ON summaries
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own summaries" ON summaries
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own summaries" ON summaries
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own summaries" ON summaries
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Insert test user (password: testpass123)
-- Note: This is a hashed version of 'testpass123' using bcrypt
INSERT INTO users (username, email, password_hash, is_active) 
VALUES (
    'testuser', 
    'test@example.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.e',
    TRUE
) ON CONFLICT (username) DO NOTHING;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
"""

def print_setup_instructions():
    """Print setup instructions for the user"""
    print("🚀 AI Research Deck - Database Setup")
    print("=" * 50)
    print()
    print("To set up your Supabase database:")
    print()
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to the SQL Editor")
    print("3. Create a new query")
    print("4. Copy and paste the SQL commands below")
    print("5. Run the query")
    print()
    print("SQL Commands:")
    print("-" * 20)
    print(get_database_schema())
    print()
    print("✅ After running these commands, your database will be ready!")
    print("🧪 Test user credentials:")
    print("   Username: testuser")
    print("   Password: testpass123")

if __name__ == "__main__":
    print_setup_instructions() 