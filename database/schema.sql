
CREATE TABLE IF NOT EXISTS leads (

    lead_id TEXT PRIMARY KEY,

    company TEXT NOT NULL,
    industry TEXT,

    contact_name TEXT,
    contact_role TEXT,
    contact_email TEXT,
    contact_phone TEXT,

    source TEXT,

    stage TEXT NOT NULL
        CHECK (
            stage IN (
                'New',
                'Contacted',
                'Meeting',
                'Proposal',
                'Invoice sent',
                'Paid',
                'Lost'
            )
        ),

    deal_value REAL NOT NULL DEFAULT 0
        CHECK (deal_value >= 0),

    last_contact TEXT,
    next_followup TEXT,

    notes TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Improve search and filtering performance

CREATE INDEX IF NOT EXISTS idx_leads_company
ON leads(company);

CREATE INDEX IF NOT EXISTS idx_leads_stage
ON leads(stage);

CREATE INDEX IF NOT EXISTS idx_leads_email
ON leads(contact_email);

CREATE INDEX IF NOT EXISTS idx_leads_followup
ON leads(next_followup);
