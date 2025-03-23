-- Drop the customers table if it exists
DROP TABLE IF EXISTS customers CASCADE;

-- Create the customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mobile_no VARCHAR(15),
    dob DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Drop the accounts table if it exists
DROP TABLE IF EXISTS accounts CASCADE;

-- Create the accounts table
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    bank_name VARCHAR(255) NOT NULL DEFAULT 'ABC Bank',  -- Fixed bank name
    ifsc_code VARCHAR(20) NOT NULL DEFAULT 'A045YT',     -- Fixed IFSC code
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Drop the transactions table if it exists
DROP TABLE IF EXISTS transactions CASCADE;

-- Create the transactions table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(account_id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('Deposit', 'Withdraw')),  -- Only allow 'Deposit' or 'Withdraw'
    transaction_date TIMESTAMPTZ DEFAULT NOW()  -- Column for transaction date
);