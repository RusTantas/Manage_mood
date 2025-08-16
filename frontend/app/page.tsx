'use client'

import { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import DailyRecordForm from '../components/DailyRecordForm'
import Analytics from '../components/Analytics'
import Navigation from '../components/Navigation'

export default function Home() {
  const [activeTab, setActiveTab] = useState('today')
  const [dailyRecords, setDailyRecords] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDailyRecords()
  }, [])

  const fetchDailyRecords = async () => {
    try {
      const response = await fetch('/api/daily-records/')
      const data = await response.json()
      setDailyRecords(data)
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRecordCreated = () => {
    fetchDailyRecords()
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Загрузка...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Добро пожаловать в Day Tracker
          </h1>
          <p className="text-gray-600">
            Отслеживайте свой день и получайте персонализированные рекомендации
          </p>
        </div>

        {activeTab === 'today' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">
                Запись на {format(new Date(), 'EEEE, d MMMM', { locale: ru })}
              </h2>
              <DailyRecordForm onRecordCreated={handleRecordCreated} />
            </div>
            
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Сегодняшняя статистика</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                  <span className="text-blue-700 font-medium">Записей за сегодня:</span>
                  <span className="text-blue-900 font-bold">
                    {dailyRecords.filter(record => 
                      format(new Date(record.date), 'yyyy-MM-dd') === format(new Date(), 'yyyy-MM-dd')
                    ).length}
                  </span>
                </div>
                
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                  <span className="text-green-700 font-medium">Всего записей:</span>
                  <span className="text-green-900 font-bold">{dailyRecords.length}</span>
                </div>
                
                <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                  <span className="text-purple-700 font-medium">Дней отслеживания:</span>
                  <span className="text-purple-900 font-bold">
                    {new Set(dailyRecords.map(record => 
                      format(new Date(record.date), 'yyyy-MM-dd')
                    )).size}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <Analytics dailyRecords={dailyRecords} />
        )}

        {activeTab === 'history' && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">История записей</h2>
            {dailyRecords.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                Пока нет записей. Начните отслеживать свой день!
              </p>
            ) : (
              <div className="space-y-4">
                {dailyRecords
                  .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                  .map((record) => (
                    <div key={record.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-medium text-gray-900">
                            {format(new Date(record.date), 'EEEE, d MMMM yyyy', { locale: ru })}
                          </h3>
                          <div className="mt-2 space-y-1 text-sm text-gray-600">
                            {record.sleep_quality && (
                              <p>Качество сна: {record.sleep_quality}/10</p>
                            )}
                            {record.overall_mood && (
                              <p>Настроение: {record.overall_mood}/10</p>
                            )}
                            {record.physical_wellness && (
                              <p>Физическое самочувствие: {record.physical_wellness}/10</p>
                            )}
                            {record.mental_wellness && (
                              <p>Ментальное самочувствие: {record.mental_wellness}/10</p>
                            )}
                          </div>
                        </div>
                        <div className="text-right text-sm text-gray-500">
                          {format(new Date(record.date), 'HH:mm')}
                        </div>
                      </div>
                      {record.notes && (
                        <p className="mt-3 text-sm text-gray-700 bg-gray-50 p-3 rounded">
                          {record.notes}
                        </p>
                      )}
                    </div>
                  ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
