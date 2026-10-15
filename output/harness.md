# Campus Customs Agent Harness

This harness documents the Campus Customs database contract for the multi-agent operations team. It is intentionally expandable and should be updated as tools, approval workflows, tests, and ticket-resolution behavior are added.

## Database and operating rules

- The working database is `data/campus_customs_new.db`.
- The original database must remain untouched.
- `desk.date_today` is the shop’s authoritative date for overdue and due-date decisions.
- Vendor lead times come from `vendors.lead_days`.
- A vendor must not receive a new product shipment request while that vendor has an unpaid invoice.
- Actual payments require human approval.
- A payment must be refused if it would make an account balance negative.
- When an approved payment is made, the relevant payment and source-record state must be updated.
- Cash only decreases for this assignment; no incoming cash should be assumed.
- Customer and vendor drafts remain on the board. The system must not send emails, make calls, or contact real people.

## Tables and fields

### `desk`

Why it matters: Provides the shop’s operating context. Agents use the authoritative shop date to determine whether invoices, leases, and other obligations are due or overdue.

- `date_today` (`TEXT`, required): The shop’s current date; use this instead of the computer’s clock for all date logic.
- `notes` (`TEXT`): Optional shop-wide notes or operating context.

### `tickets`

Why it matters: The shared work queue and agent coordination surface. Boss reads each ticket, delegates work, and tracks resolution; specialist agents add findings, decisions, drafts, and approval requests here.

- `id` (`INTEGER`, primary key): Unique ticket identifier.
- `type` (`TEXT`, required): Ticket category, such as `customer_order`, `rent_notice`, or `price_override`.
- `requester` (`TEXT`, required): Person or organization that submitted the ticket.
- `subject` (`TEXT`, required): Short description of the issue.
- `sku` (`TEXT`, optional): Product identifier for product-related tickets; joins to `inventory.sku` and `pricing.sku`.
- `size` (`TEXT`, optional): Product size for product-related tickets; combines with `sku` to identify an inventory record.
- `qty` (`INTEGER`, optional): Requested or affected quantity.
- `lease_id` (`INTEGER`, optional foreign key): Related lease; joins to `leases.id`.
- `invoice_id` (`INTEGER`, optional foreign key): Related vendor invoice; joins to `invoices.id`.
- `status` (`TEXT`, required): Workflow state, including whether the ticket remains open, pending approval, or resolved.
- `notes` (`TEXT`, optional): Agent findings, decisions, draft messages, and resolution context; drafts must remain here or on the board.
- `created_at` (`TEXT`, required): Ticket creation timestamp.

### `inventory`

Why it matters: Lets Inventory determine availability and shortages for customer orders and bulk requests, and provides the stock state that resolution tools may update.

- `sku` (`TEXT`, required; composite primary key with `size`): Product identifier.
- `name` (`TEXT`, required): Product name.
- `size` (`TEXT`, required; composite primary key with `sku`): Size or variant identifier.
- `qty` (`INTEGER`, required): Current quantity available.
- `location` (`TEXT`, required): Physical shop location of the stock.

### `pricing`

Why it matters: Supports margin checks, price overrides, and purchase decisions. Accounting and Boss can compare unit cost with list price before approving discounts or restocking.

- `sku` (`TEXT`, primary key): Product identifier; joins to `inventory.sku`.
- `unit_cost` (`REAL`, required): Cost per unit.
- `list_price` (`REAL`, required): Standard selling price per unit.

### `vendors`

Why it matters: Provides restocking options and delivery timing. Inventory uses vendor specialties and lead times, while Accounting checks unpaid invoices before allowing new shipment requests.

- `id` (`INTEGER`, primary key): Unique vendor identifier.
- `name` (`TEXT`, required): Vendor name.
- `specialty` (`TEXT`, required): Product or service category handled by the vendor.
- `lead_days` (`INTEGER`, required): Vendor shipping or fulfillment lead time in days.

### `leases`

Why it matters: Facilities uses lease records to handle shop-space obligations, calculate due or overdue rent using `desk.date_today`, and prepare payment requests for human approval.

- `id` (`INTEGER`, primary key): Unique lease identifier; joins from `tickets.lease_id`.
- `space_name` (`TEXT`, required): Shop space covered by the lease.
- `landlord` (`TEXT`, required): Lease counterparty.
- `monthly_rent` (`REAL`, required): Rent amount due for the lease period.
- `next_due` (`TEXT`, required): Next rent due date.
- `notes` (`TEXT`, optional): Lease-specific context.

### `cash_accounts`

Why it matters: Accounting uses account balances to determine whether an approved payment is affordable. Payment tools must reject any transaction that would create a negative balance.

- `name` (`TEXT`, primary key): Account identifier, such as `checking`.
- `balance` (`REAL`, required): Current available cash balance.
- `date` (`TEXT`, required): Date associated with the recorded balance.

### `payments`

Why it matters: Records actual approved payments and provides an audit trail. It must only be written after human approval and a sufficient-cash check succeeds.

- `id` (`INTEGER`, primary key): Unique payment identifier.
- `kind` (`TEXT`, required): Payment category, such as rent or invoice payment.
- `ref_id` (`INTEGER`, optional): Identifier of the related lease, invoice, or other source record.
- `amount` (`REAL`, required): Amount paid.
- `account` (`TEXT`, required): Cash account used; joins to `cash_accounts.name`.
- `paid_at` (`TEXT`, required): Payment date.
- `approved_by` (`TEXT`, required): Human approver identity or approval record; actual payments require this approval.

### `invoices`

Why it matters: Accounting uses invoices to monitor vendor obligations, determine overdue status, prepare payment requests, and block new vendor shipment requests while an invoice remains unpaid.

- `id` (`INTEGER`, primary key): Unique invoice identifier; may be referenced by `tickets.invoice_id`.
- `vendor_id` (`INTEGER`, required foreign key): Vendor owed; joins to `vendors.id`.
- `amount` (`REAL`, required): Invoice amount.
- `due_date` (`TEXT`, required): Invoice due date, evaluated against `desk.date_today`.
- `status` (`TEXT`, required): Payment state, such as open or paid.
- `description` (`TEXT`, optional): Description of the purchase or obligation.

## Relationship map

- `tickets.sku` + `tickets.size` → `inventory.sku` + `inventory.size`
- `tickets.sku` → `pricing.sku`
- `tickets.lease_id` → `leases.id`
- `tickets.invoice_id` → `invoices.id`
- `invoices.vendor_id` → `vendors.id`
- `payments.account` → `cash_accounts.name`

## Harness expansion area

Add tool contracts, agent handoff tests, approval tests, database mutation tests, reset instructions, and end-to-end ticket-resolution results here as the assignment progresses.

## Initial MCP tool contracts

The initial server is read-only and defines exactly three tools. Each tool reads only from the working database and performs no external communication or database mutation.

### `list_open_tickets`

- Purpose: Return all tickets whose `status` is `open`, ordered by ticket ID.
- Used by: Boss for initial triage and by the dashboard for the active board.
- Data sources: `tickets`.

### `get_ticket_full_context(ticket_id)`

- Purpose: Return one ticket plus any directly linked inventory, pricing, lease, invoice, and vendor records that exist.
- Used by: Boss and specialist agents before deciding what work is needed.
- Data sources: `tickets`, `inventory`, `pricing`, `leases`, `invoices`, and `vendors`.
- Missing links: Returned as `null`; the tool does not invent related data.

### `get_ticket_restock_and_financial_context(ticket_id)`

- Purpose: Report database-grounded stock shortage, unit margin, linked invoice/vendor status, shop date, and cash-account facts.
- Used by: Inventory and Accounting for the current open tickets.
- Data sources: `desk`, `tickets`, `inventory`, `pricing`, `invoices`, `vendors`, and `cash_accounts`.
- Side effects: None. It does not place orders, create payments, change balances, or contact anyone.

## Tool-to-ticket coverage

This mapping is specific to the three open tickets currently in the working database.

### `list_open_tickets`

- Reads: `tickets` (`id`, `type`, `requester`, `subject`, `sku`, `size`, `qty`, `lease_id`, `invoice_id`, `status`, `notes`, `created_at`).
- Ticket 101: Unlocks Boss’s triage of Tauhid Zaman’s Bulldog tee order by exposing that ticket 101 is open and requests one `CC-TEE-WHITE` in size `S`.
- Ticket 102: Unlocks Boss’s triage of Elm City Properties’ rent notice by exposing that ticket 102 is open and is the rent-related work item.
- Ticket 103: Unlocks Boss’s triage of Yale AI Club’s bulk hoodie request by exposing that ticket 103 is open and requests 20 `CC-HOOD-NAVY` hoodies in size `M`.

### `get_ticket_full_context(ticket_id)`

- Reads: `tickets`; conditionally reads the linked `inventory` row by `sku` + `size`, `pricing` row by `sku`, `leases` row by `lease_id`, `invoices` row by `invoice_id`, and `vendors` row through `invoices.vendor_id`.
- Ticket 101: Unlocks Inventory and Accounting’s analysis of the Bulldog tee shortage and its linked `$840` open Bulldog Print Co. invoice by returning ticket 101’s product, pricing, inventory, invoice, and vendor records.
- Ticket 102: Unlocks Facilities and Accounting’s rent analysis by returning ticket 102’s linked lease 1 record for the Chapel Street shop, including Elm City Properties, `$2,400` monthly rent, and the `2026-09-02` due date.
- Ticket 103: Unlocks Inventory and Accounting’s bulk-order analysis by returning ticket 103’s `CC-HOOD-NAVY` size `M` inventory and pricing records, while correctly returning no fabricated lease, invoice, or vendor link.

### `get_ticket_restock_and_financial_context(ticket_id)`

- Reads: `desk` (`date_today`), `tickets` (`qty`, `sku`, `size`, `invoice_id`), `inventory` (`qty`), `pricing` (`unit_cost`, `list_price`), linked `invoices` and `vendors`, and all `cash_accounts` balances.
- Ticket 101: Unlocks Inventory’s calculation that one size-S tee is short because stock is 0, and Accounting’s review of the linked vendor invoice, vendor unpaid-invoice block, shop date, cash balance, and `$20` unit margin.
- Ticket 102: Supports Facilities and Accounting’s rent-payment feasibility review by returning the authoritative shop date `2026-08-31` and checking available cash, while the lease amount and due date come from `get_ticket_full_context(102)`.
- Ticket 103: Unlocks Inventory’s calculation that 12 size-M hoodies are short because stock is 8 against a requested 20, and Accounting’s margin check using the `$22` unit cost and `$58` list price while reporting that no linked vendor invoice exists.

## Problem 5 agent team

All agents use the shared MCP facts and may delegate to any other agent through the bounded team context. Each role has one prompt file under `backend/prompts/` and one PydanticAI agent module under `backend/`.

- `boss`: Reads every ticket, routes work, coordinates delegation, and makes the final call.
- `inventory`: Checks exact SKU/size stock, calculates shortages, and evaluates vendor specialty, lead time, and unpaid-invoice blocks.
- `accounting`: Reviews cash, invoices, due dates, margins, and prepares payment or purchase-order proposals for human approval.
- `facilities`: Reviews leases and rent due dates using `desk.date_today` and prepares rent proposals.
- `customer_service`: Drafts customer-facing messages and keeps them on the board without sending them.

## Problem 5 MCP tools and database tables

| Tool | Tables read or written | Agent use |
|---|---|---|
| `list_open_tickets` | Reads `tickets` | Boss uses the active queue for triage. |
| `get_ticket_full_context` | Reads `tickets`, `inventory`, `pricing`, `leases`, `invoices`, `vendors` | Any agent retrieves only relationships actually present for a ticket. |
| `get_ticket_restock_and_financial_context` | Reads `desk`, `tickets`, `inventory`, `pricing`, `invoices`, `vendors`, `cash_accounts` | Inventory and Accounting use shortage, margin, vendor-invoice, date, and cash facts. |
| `get_lease_rent_context` | Reads `tickets`, `desk`, `leases` | Facilities uses the linked lease and authoritative shop date. |
| `list_restock_vendor_options` | Reads `inventory`, `pricing`, `vendors`, `invoices` | Inventory compares recorded product terms with vendor specialties, lead times, and unpaid-invoice blocks. |
| `prepare_payment_request` | Reads `cash_accounts`; writes nothing | Accounting or Facilities creates a human-review proposal and refuses insufficient cash. |
| `get_payment_status_context` | Reads `tickets`, `invoices`, `payments`, `cash_accounts` | Accounting verifies actual payment history and current cash before a rent decision. |
| `append_ticket_note` | Reads and writes `tickets.notes` | Agents keep findings and drafts on the board; it never sends external communications. |

The MCP server currently exposes eight tools total: the three Problem 3 tools plus the five Problem 5 tools above.

## Safety guardrails for real operations

- Treat all outbound customer, vendor, and landlord communication as drafts until a human reviews and sends it through an approved channel.
- Require explicit human approval and an authenticated approver before any actual payment; reject payments that would make any cash account negative.
- Use least-privilege database credentials, transaction logging, immutable audit storage, and regular backups before enabling writes against real systems.
- Validate every tool argument, linked record, amount, currency, and recipient; fail closed when a fact is missing or ambiguous.
- Keep secrets in environment variables or a secret manager; never put `PORTKEY_API_KEY` in prompts, logs, source code, or committed JSON.
- Add human escalation for unusual discounts, legal/lease changes, refunds, vendor changes, and any action affecting a real person.

## Firm token and loop limits

- Only `gpt-6-luna` may be used for model calls, through Portkey and `PORTKEY_API_KEY`.
- Maximum 24 agent-loop steps per run, maximum 12 delegations, and maximum 12 model calls.
- Maximum 1,200 output tokens per model call; prompts must request concise structured outputs.
- Agent retries are capped at one retry per call; no unbounded recursive delegation is permitted.
- Stop the run on a missing MCP fact, invalid structured output, repeated tool failure, or approval-required action.
- Append every step to `output/audit_trail.json`; never truncate or overwrite prior run events.

## Problem 9 final run evidence

- Reset source: the untouched original database was copied to `data/campus_customs_new.db` before the final run.
- Starting checking balance: `$3,400.00`.
- Ticket 101: closed with no cash movement; Boss → Inventory → Customer Service.
- Ticket 102: closed after human approval; Boss → Facilities → Accounting; Payment 1 paid `$2,400.00` rent and checking ended at `$1,000.00`.
- Ticket 103: closed with no cash movement; Boss → Inventory → Accounting.
- Final `cash_accounts.checking.balance`: `$1,000.00`.
- Final evidence files: `output/resolved_tickets.json`, `output/resolved_board.html`, and append-only `output/audit_trail.json`.
- The resolved board preserves the expected plan comparison in `output/desk_tickets.html`; the visual evidence page contains one static snapshot for each resolved ticket.

## Problem 7 FastAPI backend routes

Run from the `backend/` directory with `uvicorn main:app --reload --port 8000`. The API is then available at `http://localhost:8000` for the React dashboard.

| Method and URL | Function | Behavior and data sources |
|---|---|---|
| `GET /health` | `health` | Confirms the API is running, reports the working database path, and identifies the configured model as `gpt-6-luna`. |
| `GET /tickets` | `get_tickets` | Returns every ticket from `tickets`, ordered by ID; accepts `?status=open` or `?status=closed` for board filtering. |
| `GET /tickets/{ticket_id}` | `get_ticket` | Returns one complete ticket row, including its current open/closed state, or 404 if absent. |
| `POST /tickets/{ticket_id}/run` | `run_agent_team` | Runs the bounded team loop for one open ticket, records delegation steps in `output/audit_trail.json`, and returns the run ID, status, and step count; closed tickets are refused. |
| `GET /events?limit=50` | `get_recent_events` | Returns the newest append-only audit events, including agent, ticket, action, inputs, outputs, delegation target, and approval flag, so the board can refresh. |
| `GET /cash/checking` | `get_checking_balance` | Returns the current `cash_accounts` row for `checking`; it never estimates or fabricates cash. |
| `POST /payments/approve` | `approve_payment` | Executes only an explicitly human-approved invoice or rent payment, checks the source record and available cash, updates `payments`, decreases `cash_accounts`, and marks invoices paid; insufficient cash is refused. |
| `POST /reset` | `reset_database` | Restores `data/campus_customs_new.db` from the untouched original download so runs can start from baseline values. |

Payment approval request body: `{"kind":"invoice|rent","ref_id":501,"amount":840.0,"account":"checking","approved_by":"human-name"}`. Purchase orders remain proposals until a later workflow adds a purchase-order record and approval path.
