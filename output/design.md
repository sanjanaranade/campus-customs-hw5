# Agent Dashboard Design

## Visual direction

The dashboard now uses a light Yale collegiate palette with theatrical Gatsby-era Art Deco energy: Yale blue and sky blue are paired with cream white, richer brass-gold linework, and emerald jewel-tone approval states. Pink and dark-mode surfaces were removed, and the fan motif was removed in favor of a complete Gatsby title-card hero with cream paper, brass double framing, symmetrical rules, diamond separators, and period-inspired serif display typography.

## Layout and experience

- A compact operations header establishes the Campus Customs identity, live local status, refresh control, and safe reset action.
- The hero introduces the human-in-the-loop purpose with bold editorial typography and a small circular date stamp for a desk-like, premium feel.
- Three metric cards immediately answer the questions a human operator cares about: how many tickets are active, how much cash is available, and whether the human approval gate is on.
- The left ticket rail keeps all three tickets visible and selectable; the main workspace gives the selected ticket room for facts, status, controls, and activity.
- Diamond-patterned background texture, brass corner ornaments, a framed cream hero title card, jewel-box header framing, gold-topped metric cards, diamond separators, inset geometric borders, square-corner cards, uppercase tracking, and a formal serif display face create the pumped-up Gatsby feel while retaining a confident Yale identity.

## How agents read

The Agent Activity area gives each of the five agents a persistent card: Boss, Inventory, Accounting, Facilities, and Customer Service. Cards show whether an agent is standing by, active, or has completed an audited step. The audit stream below translates recorded event names into a chronological view of what an agent did and where work was delegated.

## Resolution, approvals, and cash

Starting a run highlights the working specialist and shows a running state; once the backend returns, the selected ticket receives a resolved state in the desk view and a concise completion notice. The human approval queue stays visible as a dedicated safety surface, ready to show an exact payment proposal before approval. The checking balance is pulled from `cash_accounts` and refreshes with the board, so a later approved payment will visibly reduce the amount.

## Why this works for customers

The interface makes operational complexity legible: customers benefit from a clear status trail, careful handoffs, and drafts that are reviewed before anyone communicates externally. Strong hierarchy reduces cognitive load for the human operator, while the bright campus palette, friendly rounded shapes, and small expressive details make a traditionally dry back-office workflow feel welcoming, memorable, and worthy of trust.
