# Campus Customs MCP Server

This FastMCP server gives the Campus Customs PydanticAI agent team a shared, database-grounded way to inspect and safely update the shop’s ticket board. It does not make payments, place orders, send messages, or contact real people; payment requests remain proposals requiring human approval.

## Database

The server uses the verified working copy at `../data/campus_customs_new.db` relative to this directory. The original database is not used for mutations and remains untouched. Set `CAMPUS_CUSTOMS_DB` to override the working-copy path when configuring the server.

The database is opened only when a tool is called. Read tools use SQLite read-only mode; the narrowly scoped `append_ticket_note` tool writes only to `tickets.notes` so findings and drafts remain on the board.

## Tools

### `list_open_tickets()`

Returns all tickets whose `status` is exactly `open`, including their identifiers, types, requesters, subjects, product references, linked lease or invoice IDs, notes, and creation timestamps.

### `get_ticket_full_context(ticket_id)`

Returns the requested ticket and any related inventory, pricing, lease, invoice, and vendor rows that actually exist in the database; missing relationships are returned as `null` rather than invented.

### `get_ticket_restock_and_financial_context(ticket_id)`

Reports database-grounded shortage and unit-margin calculations together with the shop date, linked vendor-invoice status, and cash-account balances; it performs no database writes.

### `get_lease_rent_context(ticket_id)`

Returns the ticket’s actual linked lease, if present, together with the authoritative `desk.date_today` value for due-date decisions.

### `list_restock_vendor_options(sku, size)`

Returns the recorded product and vendor records, including specialty matches, lead days, unpaid-invoice counts, and whether the database facts permit a shipment recommendation.

### `prepare_payment_request(kind, ref_id, amount, account)`

Checks that the account exists and has enough recorded cash, then returns a proposal for human review without moving money or writing a payment.

### `get_payment_status_context(ticket_id)`

Returns the ticket’s linked invoice, actual payment records, and cash-account balances so Accounting can verify payment status before a rent or invoice decision.

### `append_ticket_note(ticket_id, note)`

Appends a finding or draft to `tickets.notes`; it never sends the note externally.

## Agent team

- Boss reads tickets, delegates to any specialist, and makes final calls.
- Inventory checks SKU/size stock, shortages, vendor specialties, lead times, and unpaid-invoice blocks.
- Accounting monitors cash, invoices, margins, and approval-bound payment or purchase-order proposals.
- Facilities handles lease and rent facts using `desk.date_today`.
- Customer Service drafts messages and never sends them.

The backend stores one detailed prompt per role in `backend/prompts/`, typed contracts in `backend/models.py`, and agent modules under `backend/`. The bounded team loop appends each step to `output/audit_trail.json` without erasing earlier runs. It permits at most 24 steps, 12 delegations, 12 model calls, and 1,200 output tokens per call, using only `gpt-6-luna` through Portkey.
