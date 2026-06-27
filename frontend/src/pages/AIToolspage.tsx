import { AssistantChat } from '../components/ai/AssistantChat'
import { BudgetInsights } from '../components/ai/BudgetInsights'
import { EmailGenerator } from '../components/ai/EmailGenerator'
import { NoteSummarizer } from '../components/ai/NoteSummarizer'
import { TaskBreakdown } from '../components/ai/TaskBreakdown'
import { Link } from 'react-router-dom'

export function AIToolsPage() {
  return (
    <>
      <div className="page-header ai-page-header">
        <div>
          <h1>AI Tools</h1>
          <p>Work with note summaries, email drafts, task plans, budget analysis, and study planning.</p>
        </div>
        <Link className="ghost-button ai-header-action" to="/study-planner">
          Open Study Planner
        </Link>
      </div>

      <section className="ai-workspace">
        <div className="ai-chat-section">
          <AssistantChat />
        </div>

        <div className="ai-tools-grid">
          <NoteSummarizer />
          <EmailGenerator />
          <TaskBreakdown />
          <BudgetInsights />
        </div>
      </section>
    </>
  )
}
