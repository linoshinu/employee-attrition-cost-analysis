# LinkedIn post drafts

Review each draft before publishing. Replace the repository link after the GitHub repository is populated. Keep the disclosure that the IBM sample is fictional.

## Post 1 — concise project launch

I turned an employee attrition analysis into a reproducible portfolio project using Python, SQL, and a Tableau-ready dashboard.

The project explores attrition by department, tenure, overtime, and job role, then adds a replacement-cost sensitivity model. One design choice I focused on: separating what the data shows from what the model assumes. The underlying IBM sample is fictional, and the cost estimates are scenarios—not actual company losses or proof that a retention program will work.

The repository includes the data notes, SQL queries, interactive dashboard, and an interview walkthrough: https://github.com/linoshinu/employee-attrition-cost-analysis

I also used AI-assisted development to speed up the first draft, then made the definitions and assumptions explicit so the analysis is reviewable.

I’d welcome feedback on how you communicate uncertainty in people analytics.

#PeopleAnalytics #DataAnalytics #SQL #Python #Tableau #PortfolioProject

## Post 2 — analytical design

An attrition percentage can look decisive until you ask how many records sit behind it—and what it costs to lose someone.

For my employee attrition portfolio project, I built a small end-to-end workflow with Python, SQL, and an interactive dashboard. It lets a reader compare group rates with their denominators and explore cost ranges under explicit assumptions.

The cost model is deliberately modest: the dataset does not contain recruiting invoices, vacancy duration, or replacement outcomes, so the dashboard uses 25% / 50% / 75% of annualized income as illustrative proxies. A separate what-if page compares budget allocations only under user-selected cost and effect assumptions. It does not claim causal impact or predict individual employees.

The source is IBM’s fictional HR analytics sample, not real workforce data. I’m using it to practice careful analysis and stakeholder communication—not to make HR decisions.

Code and walkthrough: https://github.com/linoshinu/employee-attrition-cost-analysis

I used AI-assisted development in the workflow and kept the project reproducible so others can inspect the analysis.

#PeopleAnalytics #ResponsibleAI #BusinessAnalytics #Python #SQL #Tableau
