-- Supabase SQL Schema for Pachena Eco-Tourism Resort
-- Run this SQL in your Supabase SQL Editor to create the enquiries table

-- Create the enquiries table
CREATE TABLE IF NOT EXISTS enquiries (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    booking_date DATE NOT NULL,
    num_adults INTEGER NOT NULL DEFAULT 0,
    num_children INTEGER NOT NULL DEFAULT 0,
    package VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    follow_up_notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on created_at for faster sorting
CREATE INDEX idx_enquiries_created_at ON enquiries(created_at DESC);

-- Create an index on status for filtering
CREATE INDEX idx_enquiries_status ON enquiries(status);

-- Create an index on booking_date
CREATE INDEX idx_enquiries_booking_date ON enquiries(booking_date);

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE enquiries ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow all operations (adjust based on your security needs)
-- For public access (booking form submission)
CREATE POLICY "Allow public insert" ON enquiries
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- For authenticated users (admin dashboard)
CREATE POLICY "Allow authenticated full access" ON enquiries
    FOR ALL
    TO authenticated
    USING (true);

-- If you want to allow anonymous read access (for public viewing)
CREATE POLICY "Allow public read" ON enquiries
    FOR SELECT
    TO anon
    USING (true);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to call the function before any update
CREATE TRIGGER update_enquiries_updated_at
    BEFORE UPDATE ON enquiries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data (optional - remove in production)
INSERT INTO enquiries (name, phone, booking_date, num_adults, num_children, package, status)
VALUES 
    ('John Doe', '+1-555-0101', '2026-02-15', 2, 1, 'Adventure Package', 'pending'),
    ('Jane Smith', '+1-555-0102', '2026-02-20', 1, 0, 'Wellness Day', 'confirmed'),
    ('Bob Johnson', '+1-555-0103', '2026-03-01', 4, 2, 'Ultimate Package', 'pending');
