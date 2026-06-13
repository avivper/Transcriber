import type { Stage } from '../core/types'
import { StageCard } from './StageCard'

interface PipelinePanelProps {
  stages: Stage[]
}

export function PipelinePanel({ stages }: PipelinePanelProps) {
  return (
    <section className="panel">
      <div className="panel__title">Pipeline</div>
      <div className="pipeline">
        {stages.map((stage, i) => (
          <StageCard key={stage.id} stage={stage} index={i} />
        ))}
      </div>
    </section>
  )
}
