'use client'

import { StarIcon } from '@heroicons/react/24/solid'
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline'

interface RatingInputProps {
  value: number
  onChange: (value: number) => void
  max?: number
}

export default function RatingInput({ value, onChange, max = 10 }: RatingInputProps) {
  const stars = Array.from({ length: max }, (_, i) => i + 1)

  return (
    <div className="rating-stars">
      {stars.map((star) => (
        <button
          key={star}
          type="button"
          onClick={() => onChange(star)}
          className="star"
          aria-label={`Оценить ${star} из ${max}`}
        >
          {star <= value ? (
            <StarIcon className="star-filled h-6 w-6" />
          ) : (
            <StarOutlineIcon className="star-empty h-6 w-6" />
          )}
        </button>
      ))}
      <span className="ml-3 text-sm text-gray-600">
        {value > 0 ? `${value}/${max}` : 'Не оценено'}
      </span>
    </div>
  )
}
