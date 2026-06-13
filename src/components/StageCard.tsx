import type { Stage } from '../core/types'

interface StageCardProps {
  stage: Stage
  index: number
}

export function StageCard({ stage, index }: StageCardProps) {
  return (
    <div className={`stage-card stage-card--${stage.status}`}>
      <span className="stage-card__index">{index + 1}</span>
      <span className="stage-card__name">{stage.name}</span>
      <span className="stage-card__status">{stage.status}</span>
    </div>
  )
}
