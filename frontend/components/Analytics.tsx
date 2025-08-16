'use client'

import { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface AnalyticsProps {
  dailyRecords: any[]
}

export default function Analytics({ dailyRecords }: AnalyticsProps) {
  const [analyticsData, setAnalyticsData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (dailyRecords.length > 0) {
      processAnalyticsData()
    } else {
      setLoading(false)
    }
  }, [dailyRecords])

  const processAnalyticsData = () => {
    // Сортируем записи по дате
    const sortedRecords = dailyRecords
      .filter(record => record.overall_mood) // Только записи с оценкой настроения
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

    if (sortedRecords.length === 0) {
      setLoading(false)
      return
    }

    // Подготавливаем данные для графиков
    const labels = sortedRecords.map(record => 
      format(new Date(record.date), 'dd.MM', { locale: ru })
    )
    
    const moodData = sortedRecords.map(record => record.overall_mood)
    const sleepQualityData = sortedRecords.map(record => record.sleep_quality || 0)
    const physicalWellnessData = sortedRecords.map(record => record.physical_wellness || 0)
    const mentalWellnessData = sortedRecords.map(record => record.mental_wellness || 0)

    // Вычисляем средние значения
    const avgMood = moodData.reduce((a, b) => a + b, 0) / moodData.length
    const avgSleepQuality = sleepQualityData.filter(x => x > 0).length > 0 
      ? sleepQualityData.filter(x => x > 0).reduce((a, b) => a + b, 0) / sleepQualityData.filter(x => x > 0).length 
      : 0

    setAnalyticsData({
      labels,
      moodData,
      sleepQualityData,
      physicalWellnessData,
      mentalWellnessData,
      avgMood,
      avgSleepQuality,
      totalRecords: sortedRecords.length
    })
    setLoading(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Загрузка аналитики...</p>
        </div>
      </div>
    )
  }

  if (!analyticsData || analyticsData.totalRecords === 0) {
    return (
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Аналитика</h2>
        <p className="text-gray-500 text-center py-8">
          Для отображения аналитики необходимо добавить записи с оценками настроения.
        </p>
      </div>
    )
  }

  const moodChartData = {
    labels: analyticsData.labels,
    datasets: [
      {
        label: 'Настроение',
        data: analyticsData.moodData,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.1,
      },
    ],
  }

  const wellnessChartData = {
    labels: analyticsData.labels,
    datasets: [
      {
        label: 'Физическое самочувствие',
        data: analyticsData.physicalWellnessData,
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.1,
      },
      {
        label: 'Ментальное самочувствие',
        data: analyticsData.mentalWellnessData,
        borderColor: 'rgb(168, 85, 247)',
        backgroundColor: 'rgba(168, 85, 247, 0.1)',
        tension: 0.1,
      },
    ],
  }

  const sleepChartData = {
    labels: analyticsData.labels,
    datasets: [
      {
        label: 'Качество сна',
        data: analyticsData.sleepQualityData,
        backgroundColor: 'rgba(251, 191, 36, 0.8)',
        borderColor: 'rgb(251, 191, 36)',
        borderWidth: 1,
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 10,
      },
    },
  }

  return (
    <div className="space-y-8">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Среднее настроение</h3>
          <p className="text-3xl font-bold text-primary-600">
            {analyticsData.avgMood.toFixed(1)}
          </p>
          <p className="text-sm text-gray-500">из 10</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Среднее качество сна</h3>
          <p className="text-3xl font-bold text-yellow-600">
            {analyticsData.avgSleepQuality.toFixed(1)}
          </p>
          <p className="text-sm text-gray-500">из 10</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Всего записей</h3>
          <p className="text-3xl font-bold text-green-600">
            {analyticsData.totalRecords}
          </p>
          <p className="text-sm text-gray-500">дней отслеживания</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Динамика настроения</h3>
          <Line data={moodChartData} options={chartOptions} />
        </div>
        
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Самочувствие</h3>
          <Line data={wellnessChartData} options={chartOptions} />
        </div>
        
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Качество сна</h3>
          <Bar data={sleepChartData} options={chartOptions} />
        </div>
      </div>

      {/* Insights */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Инсайты</h3>
        <div className="space-y-3">
          {analyticsData.avgMood < 6 && (
            <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-yellow-800">
                <strong>Низкое настроение:</strong> Ваше среднее настроение ниже 6/10. 
                Попробуйте добавить больше приятных активностей в свой день.
              </p>
            </div>
          )}
          
          {analyticsData.avgSleepQuality > 0 && analyticsData.avgSleepQuality < 6 && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">
                <strong>Плохое качество сна:</strong> Среднее качество сна {analyticsData.avgSleepQuality.toFixed(1)}/10. 
                Рекомендуется улучшить гигиену сна.
              </p>
            </div>
          )}
          
          {analyticsData.totalRecords >= 7 && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800">
                <strong>Отличная работа!</strong> Вы отслеживаете данные уже {analyticsData.totalRecords} дней. 
                Продолжайте в том же духе!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
