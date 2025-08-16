'use client'

import { useState } from 'react'
import { format } from 'date-fns'
import RatingInput from './RatingInput'

interface DailyRecordFormProps {
  onRecordCreated: () => void
}

export default function DailyRecordForm({ onRecordCreated }: DailyRecordFormProps) {
  const [formData, setFormData] = useState({
    wake_up_time: '',
    sleep_time: '',
    sleep_quality: 0,
    overall_mood: 0,
    physical_wellness: 0,
    mental_wellness: 0,
    notes: ''
  })
  
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await fetch('/api/daily-records/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          wake_up_time: formData.wake_up_time ? new Date(formData.wake_up_time).toISOString() : null,
          sleep_time: formData.sleep_time ? new Date(formData.sleep_time).toISOString() : null,
        }),
      })

      if (response.ok) {
        setMessage('Запись успешно создана!')
        setFormData({
          wake_up_time: '',
          sleep_time: '',
          sleep_quality: 0,
          overall_mood: 0,
          physical_wellness: 0,
          mental_wellness: 0,
          notes: ''
        })
        onRecordCreated()
      } else {
        const error = await response.json()
        setMessage(`Ошибка: ${error.detail || 'Неизвестная ошибка'}`)
      }
    } catch (error) {
      setMessage('Ошибка при отправке данных')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Sleep Section */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">Сон</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Время пробуждения
            </label>
            <input
              type="datetime-local"
              value={formData.wake_up_time}
              onChange={(e) => handleInputChange('wake_up_time', e.target.value)}
              className="input-field"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Время отхода ко сну
            </label>
            <input
              type="datetime-local"
              value={formData.sleep_time}
              onChange={(e) => handleInputChange('sleep_time', e.target.value)}
              className="input-field"
            />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Качество сна (1-10)
          </label>
          <RatingInput
            value={formData.sleep_quality}
            onChange={(value) => handleInputChange('sleep_quality', value)}
          />
        </div>
      </div>

      {/* Wellness Section */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">Самочувствие</h3>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Общее настроение (1-10)
          </label>
          <RatingInput
            value={formData.overall_mood}
            onChange={(value) => handleInputChange('overall_mood', value)}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Физическое самочувствие (1-10)
          </label>
          <RatingInput
            value={formData.physical_wellness}
            onChange={(value) => handleInputChange('physical_wellness', value)}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ментальное самочувствие (1-10)
          </label>
          <RatingInput
            value={formData.mental_wellness}
            onChange={(value) => handleInputChange('mental_wellness', value)}
          />
        </div>
      </div>

      {/* Notes Section */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Заметки о дне
        </label>
        <textarea
          value={formData.notes}
          onChange={(e) => handleInputChange('notes', e.target.value)}
          rows={4}
          className="input-field"
          placeholder="Опишите, как прошел ваш день, что было хорошего и что можно улучшить..."
        />
      </div>

      {/* Message */}
      {message && (
        <div className={`p-3 rounded-md ${
          message.includes('Ошибка') 
            ? 'bg-red-50 text-red-700 border border-red-200' 
            : 'bg-green-50 text-green-700 border border-green-200'
        }`}>
          {message}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Сохранение...' : 'Сохранить запись'}
      </button>
    </form>
  )
}
