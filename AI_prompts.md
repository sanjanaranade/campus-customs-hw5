# AI Prompts

## Problem 1: Vibe coder prompts

### Prompt 1

> Problem 1: Vibe coder prompts. Please create AI_prompts.md now and keep it thoroughly updated as we work! this should be a log of what i'm typing to you, my vibe coder. there should be 1 section per problem, each containing the problem # & title, as well as all the prompts i typed and any follow up prompts as well along with a brief explanation for why each follow up was needed. got it? go.

**Follow-up prompts:** None.

**Follow-up rationale:** No follow-up prompt was needed for Problem 1.

## Problem 2: Study the Campus Customs database

### Prompt 1

> Perfect! On to problem 2, which is called: Study the Campus Customs database

### Follow-up Prompt 1

> please open the og database and carefully study each table and fields. make sure that original file is coped to that new database, which will be used by later probelsm that will udpate this working copy

**Why this follow-up was needed:** This directs the database-study work, establishes that every table and field must be reviewed, and confirms that later problems must use a verified working copy rather than modifying the original database.

### Follow-up Prompt 2

> ok, now d you see 3 open tickets in the working db?

**Why this follow-up was needed:** This asks for direct confirmation that the working database contains the expected three open tickets before proceeding with later work.

### Follow-up Prompt 3

> awesome. study those open tickets thoroughly so you have a grasp of howthey link to other tables. ok

**Why this follow-up was needed:** This requires tracing each open ticket’s relationships to the operational tables so later agent decisions and database updates use the correct linked records.

### Follow-up Prompt 4

> you understand how they link?

**Why this follow-up was needed:** This checks that the relationships among the open tickets and their linked operational records were correctly understood before moving on.

### Follow-up Prompt 5

> cool. so, please start output/harness.md. here, for each table, please create a list of the fields as well as a brief explanation for why that table matters for the agents. keep in mind we will continue to grow this harness throughout this assignment later too

**Why this follow-up was needed:** This begins the persistent assignment harness and establishes the required documentation for every database table and field, which will be expanded as the agent tools and workflows are built.

## Problem 3: Build the MCP server

### Prompt 1

> Great. on to problem 3 ,called Build the MCP server

### Follow-up Prompt 1

> Here, please write an mcp server in mcp_server/ using fastmcp. this shodl talk to the new database data_campus_customs_new.db. please do not connect or run it yet. keep in midn that all agents for this assignment will use the tools in this mcp server and we will add more tools later, rifght now please just write 3 toools that you KNOW you will require for the open tickets in the database. make sure their names are very clear. pelase do not fabricate ANY data, and use only information availabel in the database!!!!! got it go!

**Why this follow-up was needed:** This defines the first implementation scope: a FastMCP server with exactly three clearly named, database-grounded tools, using the working database while remaining unstarted and extensible for later tools.

### Follow-up Prompt 2

> amazing. continuing problem 3, please thoroughly update the harness output/harness.md with a list of the 3 mcp tools, as well as for each tool write which table it reads, which of the 3 open tickets it helps to unlock (101-103), and a brief explanation of 1 sentence long for which each tool is right for that ticket. keep in mind this needs to be specific and NOT vague in order to get full points! then, please create a brief mcp_server/README.md file that briefly explains the purpose of the mcp server as well as the database it uses and also the 3 tools u created. ok go!

**Why this follow-up was needed:** This requires ticket-specific harness documentation and a concise README so the MCP server’s scope, data sources, and usefulness for tickets 101–103 are explicit and gradeable.

## Problem 4: Add the MCP server to vibe coder and test each tool

### Prompt 1

> Great. Problem 4 is called Add the MCP server to vibe coder and test each tool

### Follow-up Prompt 1

> In my vibe coder, which is you, please add my mcp server u made to this project. save te connection json text in .mcp.json at the root, or if u have another way to save local mcp server lists do it that way. when the vibe coder is connected, pls test all 3 mcp tools. you need to save the detailed evidence of the testss within output/mcp_smoke.json. for each of the 3 tools, pls be sure to include the prompt that i asked the vibe coder, the tool's name, and also the output of the tool that perfectly matches whats in the 'new' database in terms of values. got it go!

**Why this follow-up was needed:** This requests local MCP registration, execution of all three tools, and a detailed evidence artifact proving that each tool’s output matches the working database.

## Problem 5: Build the agent team and grow the MCP tools

### Prompt 1

> It's called Build the agent team and grow the MCP tools

### Follow-up Prompt 1

> Here, i would like for u to help build the agentic team for CC -- campus customs remeber -- using the following agents -- pydantic ai boss inventory accounting facilties customer service. we must have prompts, models, and agent loops to ensure connectivity and that they can delegate tasks to each other!!!!!! i would like for u to please place the prompts in backend/prompts/, limiting to only one file for each of the agents. also put data types in backend/models.py, and the agent files under backend/. remember to use my portkey api key and gpt luna 6 only!!!!! no other model. each prompt must describe the rules of the agents. the more detail in the prompts, the better! the boss must be able to read each ticket, decide who will work on it, and make the ultimate call. inventory must be able to check by sku/size the stock, flag shortfalls and also figure out which vendors can restock the merchandise. accounting neesds to monitor cash/invoices/margins/prepare payments/purchase orders, faciltiies has to oversee things like leases and rent, and customer service must write up messages. got it? good. then, please add the tools those agents need to the mcp server we already created. facts for the shop are found in that 'new' database, so do not fabricate anything that will override mcp. please connect the agents so they append successfully to output/audit_trail.json throughout their running. each step in the agentic loop must have enough info recorded that can be audited afterwards. aka, do NOT erase the info between runs! then, please also list all of the agents and mcp tools, included those added in problem 5, to the harness output/harness.md also paired with the table that each tool uses from the working db! then, write up a brief and concise section for safety in the harness that describes briefly the guardrails that a business would need in place when agents are interacting with actual ppl and actual monies, and create firm limits that will not execcsively use tokens and include those limits in the harness too. also, please be sure to update the read me file mcp_server/README.md file so it all matches all thsi info. got it? go!

**Why this follow-up was needed:** This defines the full Problem 5 implementation: a PydanticAI multi-agent team, detailed role prompts, typed models, delegating loops, database-grounded MCP tools, durable audit logging, safety and token guardrails, and synchronized harness/README documentation.

## Problem 6: Plan the three tickets

### Prompt 1

> terffic! on to #6: PLan the three tickets

**Follow-up prompts:** None yet.

**Follow-up rationale:** No follow-up prompt has been needed so far.

### Follow-up Prompt 1

> can you remind me of the 3 tickets?

**Why this follow-up was needed:** This asks for a concise recap of the three tickets that Problem 6 will plan.

### Follow-up Prompt 2

> and remind me of the agents and tools i have available

**Why this follow-up was needed:** This requests a recap of the available agent roles and MCP tools before planning ticket execution.

### Follow-up Prompt 3

> **Okay working on 6 now... in my own words im describing what i expect the team to do on each open ticket: Ticket 101:** Boss calls Inventory, which hands off to Customer Service. Expected tools: `get_ticket_restock_and_financial_context`, `list_restock_vendor_options`. Determine restocking options for the out-of-stock T-shirt and draft a customer update.
> **Ticket 102:** Boss calls Facilities, which hands off to Accounting. Expected tools: `get_lease_rent_context`, `get_ticket_full_context`. Verify rent terms, due date, and payment status before deciding next steps.
> **Ticket 103:** Boss calls Inventory, which hands off to Accounting. Expected tools: `get_ticket_restock_and_financial_context`, `list_restock_vendor_options`. Check hoodie replenishment options and financial constraints before deciding on the bulk discount and order.

**Why this follow-up was needed:** This defines the expected agent delegation sequence, MCP tools, and decision objectives for each of the three open tickets.

### Follow-up Prompt 4

> i fear i told u slightly prematurely lol because u need to fist build output/desk_tickets.html, that a user can double click that has 1 tab per ticket. u need to also add empty cash and reflection tabs that we will add to later on, for now just leave those tabs black. for each ticket tab (there are 3 remember), please fill out the expected section with the info i gave u about what i expect for each, and leave room for a different Actual section that we will fill post-run. i earlier told u for each of the 3 expected sections who the boss will call first, all the agents that will be invplved, and the mcp tools i expect will be usedf. ensure that i did not recommend sending multiple specialists on eeach ticket for the same task, and be super detailed in creating the tabs and stuff!

**Why this follow-up was needed:** This adds the pre-run planning dashboard requirement, including one tab per ticket, blank Cash and Reflection tabs, detailed expected delegation/tool sections, and separate empty Actual sections for post-run comparison.

### Follow-up Prompt 5

> great. and the directions i gave u in my own words meet the project guidelines?

**Why this follow-up was needed:** This asks for a rubric-oriented review of the pre-run delegation and tool plan before execution.

### Follow-up Prompt 6

> ok add it then briefly

**Why this follow-up was needed:** This authorizes adding the missing payment-status tool and updating the related planning documentation.

## Problem 7: Backend routes

### Prompt 1

> nice thanks! now on to #7, called Backend routes

**Follow-up prompts:** None yet.

**Follow-up rationale:** No follow-up prompt has been needed so far.

### Follow-up Prompt 1

> problem 8 is gonna be making the react frontend dashboard, but before we do that, we need to do 7. we are creating the backend that probem 8 can then call. in backend/main.py, please use fastapi and add routes that can return the tickets and state if they are open/closed, run an agent team on a ticket ocne given the ticket, return recent agents events so that board can refresh, including what they agents said and tools utilized, approve payment/purchase after a human clicks approve, return the current checking balance obtained from cash_accounts, and reset the database to og varlues btw runs. got it? start the server with uvicorn main:app --reload --port 8000 from the backend/ folder, which should turn on the backend at http://localhost:8000 so that the frontend will work. please list these routes -- url and function, thoroughly -- in the harness output/harness.md! go!

**Why this follow-up was needed:** This defines the FastAPI route surface needed by the future React dashboard, including ticket state, agent execution, audit refresh, human-approved payments, cash balance, database reset, server startup, and route documentation.

## Problem 8: Agent dashboard

### Prompt 1

> awesome! problem 8 is called: agent dashboard

**Follow-up prompts:** None yet.

**Follow-up rationale:** No follow-up prompt has been needed so far.

### Follow-up Prompt 1

> this is the frontend bit. pls go ahead and create the frontend dashboard in frontend/ using react, vite, and typescript. make sure that the page calls the routes from the previous problem. the board u make needs to list all 3 tickets, let u pick one ticket and have the agent team start on it, show each agent and waht they are up to (saying and doing) whilethe ticket runs, mark a ticket resolved when the run finishes, show a short summary of what each agent did on that ticket, and let a human approve a pay or purchase when asked, and show the checking balance which ensure that it drops after a pyament is approved. i want the dashboard to look really good looking --- think yale esque colors, bold lettering, a confident vibe, embellishments and curly graphics and just create an awesome user experience. please have the front and backends be able to talk at the local host 8000 link u made, http://localhost:8000 . then, on the backend, please allow the vite page -- i think it's http://localhost:5173 -- so the browser can cal on those routes. the terminal command npm run dev must start the board, meaning the react desk is open inb rowser and able to work. once the dashboard looks really creative and visually appealing and on theme and beautiful and professional, please write output/design.md that describes briefly the elemtns i chose for the dashboard look, including layout, how agents read, how resolved tickets/cash appear, etc. also include here the reasoning , including for my creative choices and why a customer woudl enjoy using! go!!!!!

**Why this follow-up was needed:** This defines the React/Vite/TypeScript dashboard scope, backend integration, agent-run interaction, payment approval and cash refresh behavior, visual direction, local dev command, and required design documentation.

### Follow-up Prompt 2

> why does it say load failed

**Why this follow-up was needed:** This reports a visible dashboard loading error and asks for diagnosis.

### Follow-up Prompt 3

> see it literally says load failed

**Why this follow-up was needed:** This provides direct visual evidence confirming that the dashboard still displayed the loading error.

### Follow-up Prompt 4

> amazing. and did u do my design features tho i dont see the yale esque colors or anything

**Why this follow-up was needed:** This asks for verification that the requested Yale-inspired visual direction and dashboard embellishments are visible in the implemented frontend.

### Follow-up Prompt 5

> update teh design md file too

**Why this follow-up was needed:** This requests that the design documentation stay synchronized with the revised Yale-blue color treatment.

### Follow-up Prompt 6

> make sure those follow ups ar ewell recorded tho

**Why this follow-up was needed:** This requests an audit of Problem 8’s prompt placement and confirmation that all dashboard follow-ups are recorded in the correct section and order.

### Follow-up Prompt 7

> and remove the pink and darkness all together and make the page look collegiate and cute

**Why this follow-up was needed:** This revises the dashboard visual direction to a light, collegiate, friendly style without pink or dark-mode surfaces.

### Follow-up Prompt 8

> and remove the random curly star graphics and make the whole thing look futuristic vibes

**Why this follow-up was needed:** This removes the remaining decorative ornaments and revises the visual direction toward a cleaner futuristic interface.

### Follow-up Prompt 9

> make it look super art deco

**Why this follow-up was needed:** This revises the dashboard’s visual direction again, adding a pronounced Art Deco system while preserving the light Yale collegiate base.

### Follow-up Prompt 10

> even more art deco energy please. like strong gatsby energy

**Why this follow-up was needed:** This requests a stronger Gatsby-era Art Deco expression with richer ornament, brass, emerald, and geometric symmetry.

### Follow-up Prompt 11

> make it even more gatsby esque. reallyyyyyyyy pump it up

**Why this follow-up was needed:** This asks for a substantially more theatrical Gatsby-era treatment rather than a restrained Art Deco interpretation.

### Follow-up Prompt 12

> gorg but i don't like the art deco fan make the whole hero look gatsby instead

**Why this follow-up was needed:** This keeps the Gatsby direction while replacing the unwanted fan motif with a complete Gatsby-style hero treatment.

### Follow-up Prompt 13

> looks perf thank u so much. that completes #8.

**Why this follow-up was needed:** This confirms that the Problem 8 dashboard work is complete.

## Problem 9: Resolve the tickets

### Prompt 1

> Now on to #9, which is called Resolve the tickets

**Follow-up prompts:** None yet.

**Follow-up rationale:** No follow-up prompt has been needed so far.

### Follow-up Prompt 1

> Please reset the working database -- the 'new' one -- so we start clean. make note of the strting checking balance. run all 3 tickets on the board until resolution is reached. please open output/desk_tickets.html from #6, and on each ticket tab, please fill out the actual section that was kept blank back then from this run, including: the agents that worked, what they delegated, which tools they used. maintain the expected section so that the expected and actual can be compared.

**Why this follow-up was needed:** This requests a clean baseline, a recorded starting cash balance, execution of all three ticket workflows, and post-run Actual sections that can be compared against the preserved Expected plans.

### Follow-up Prompt 2

> wait what but my homework says to resolve it im so confused

**Why this follow-up was needed:** This flags the mismatch between the homework requirement to resolve tickets and the current scaffold’s delegation-only run behavior.

### Follow-up Prompt 3

> also i am human and i give u approval to do what u need for this assignment

**Why this follow-up was needed:** This provides the human approval required to execute the pending assignment payment and complete the remaining ticket workflow.

### Follow-up Prompt 4

> slay thx so much continuing with #9, now on the cash tab of the same html page please itemize the money with the starting checking balance post-reset, for each ticket put how the cash changed upon resolution with info on why (which pay, purchase, dolalr amount), ending checking balance that perfectly matches cash_accounts in the working db. note that i will lose points for wrong cash math, so please ensure accuracy.

**Why this follow-up was needed:** This requires an exact post-run cash reconciliation tied to each ticket, payment record, starting reset balance, and final `cash_accounts` balance.

### Follow-up Prompt 5

> slayyy

**Why this follow-up was needed:** This acknowledges the completed cash reconciliation while continuing Problem 9.

### Follow-up Prompt 6

> please do the following this is still problem 9 btws. create output/resolved_tickets.json for each ticket and put the id, final status, short outcome, what each agent contributed, and any human approvals needed. also make output/resolved_board.html, a page that the user can double click that has a screenshot of the react board for EACH resolved tickets aka 3 screenshots. please append all the real runs to output/audit_trail.json. finish the harness output/harness.md so that info on tables, mcp tools, 5 agents, api routes, the dashboard, and safety rule sare all included. go!

**Why this follow-up was needed:** This requests final Problem 9 evidence artifacts for resolved tickets, real audit events, a visual resolved-board record, and completion of the assignment harness.

### Follow-up Prompt 7

> where are the screenshot stho lol

**Why this follow-up was needed:** This asks for the promised visual evidence as actual image files rather than only static HTML panels.

## Problem 10 — Reflection

### Prompt 1

> now on to problem 10, the reflection

**Why this prompt was logged:** This begins the reflection portion of the assignment and signals the transition from ticket-resolution evidence to reflection work.

### Follow-up Prompt 1

> please plwase please open output/desk_tickets.html, and fill out the reflection tab. please be super super detailed and thorough, using evidence as geneeric verbiage will not be appreciated by me, ok? please write there how you evaluate the performance of the agents on each ticket with thorough reasoning and evidence, how the actual compared to expected for each ticket, what could have been simpler if it had been done as just one agent that had tools and why you are thinking this, 3 new problems campus customs has the potential of incurring in the future that this agent team has teh capacity to solve, and 3 new rpoblems they coudl NOT solve, on the flip side. for that last one, also thoroughlu include what tools and agents WOULD help to solve them. please make sure each answer heavily heavily references the app we made and the 3 specific tickets, and are not generalizale/generic! this is very important. pelase reference the ticket tabkes and cash tab. be very detailed and hyper specific

**Why this follow-up was needed:** This requires the blank Reflection tab to become a detailed, evidence-based evaluation tied directly to Tickets 101–103, their Expected and Actual sections, the Cash tab, audit trail, agent handoffs, MCP tools, and concrete limits of the current system.

### Follow-up Prompt 2

> add even more detail and more thoroughness and more evidence from our work. and also make the page matchthe gatsby vibe!

**Why this follow-up was needed:** This requests a deeper evidence ledger grounded in the project artifacts and a visual restyle consistent with the Gatsby/Yale design established for the other evidence pages.

## Problem 11 — Submit to GitHub

### Prompt 1

> problem 11: submit to github.

**Why this prompt was logged:** This begins the GitHub submission portion of the assignment; no submission action was taken because the user subsequently instructed me to wait.

### Follow-up Prompt 1

> no dont do anything yet log the prompt and info

**Why this follow-up was needed:** This explicitly pauses all GitHub, commit, and submission actions while requiring only that the prompt be recorded in the Problem 11 section.

### Follow-up Prompt 2

> awesome lets do #11 now

**Why this follow-up was needed:** This indicates readiness to begin Problem 11, but the next instruction immediately pauses all action while the user provides step-by-step directions.

### Follow-up Prompt 3

> no dont do anything im giving steps

**Why this follow-up was needed:** This explicitly instructs me to wait and prohibits inspection, committing, or submission until further directions are provided.

### Follow-up Prompt 4

> aweosme here are the steps we will now push the code to a public github repository so that the ppl grading me will be able to clone it! i need the repo url that i will be able to submit. please also put it within output/github_url.txt ok?make sure to NOT push my real .env to the github repo and make sure to YES include both databases under data/ (both og and the 'new' working copy) so graders can run the app. please follow the following file tree layout. note that README needs to fully explain tht the user must copy the original DB to the working DB when needing a clean run, start mcp server, start FastAPI backend, start react board, reset the db before a full 3 ticket run. [requested file tree follows]

**Why this follow-up was needed:** This authorizes the public GitHub submission and specifies the required repository contents, secret exclusion, database inclusion, README runbook, repository URL artifact, and grader-facing file layout.

### Follow-up Prompt 5

> can u confirm the file tree and confirm accuracy and confirm the log and everything please

**Why this follow-up was needed:** This requests a read-only quality audit of the submission tree, evidence, database files, Git state, and prompt log before public submission.

### Follow-up Prompt 6

> structure the filetree for me how u have it so i can ensure

**Why this follow-up was needed:** This asks for a clear representation of the current repository structure so the user can verify the submission contents before pushing.

### Follow-up Prompt 7

> ehh i actually want hw5/ within that AI_prompts.md, requirements.txt, .env.example, .gitignore, .mcp.json, README.md, data/ (within that i want campus_customs.db and campus_customs_new.db), mcp_server/ (within that i want server.py and README.md), frontend/, backend/ (within that i want main.py, models.py, prompts/ [within that i want boss.md, inventory.md, accounting.md, facilities.md, customer_service.md]), and output/ (within that i want harness.md, mcp_smoke.json, desk_tickets.html, design.md, resolved_tickets.json, resolved_board.html, audit_trail.json, and github_url.text)

**Why this follow-up was needed:** This corrects the required package root and specifies the exact grader-facing nested structure, including the lowercase `hw5/` folder and URL artifact.

### Follow-up Prompt 8

> ok thank u . give me steps for how to do the github thing so i can complete #11

**Why this follow-up was needed:** This requests practical instructions for creating the public repository, pushing the prepared local commit, recording the repository URL, and completing Problem 11.

### Follow-up Prompt 9

> wait i did step 1 and 2. can u do whats after that for me

**Why this follow-up was needed:** This authorizes me to perform the local staging, commit, remote setup, push, and URL-recording steps after the user created the public GitHub repository.

### Follow-up Prompt 10

> is this what u r looking for [https://github.com/sanjanaranade/campus-customs-hw5.git](https://github.com/sanjanaranade/campus-customs-hw5.git)

**Why this follow-up was needed:** This supplies the exact public GitHub HTTPS remote required to complete the Problem 11 push.
