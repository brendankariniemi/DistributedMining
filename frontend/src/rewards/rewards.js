import React, { useEffect, useState } from 'react';
import './rewards.css';
import rewardService from '../services/rewardService';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import { enUS } from 'date-fns/locale';
import 'chartjs-adapter-date-fns';


function RewardsPage() {
    const [rewards, setRewards] = useState(null);
    const [cumulativeRewards, setCumulativeRewards] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        rewardService.getRewards()
            .then(response => {
                const responseData = response.data;
                setRewards(responseData.rewards_per_hardware);
                setCumulativeRewards(responseData.cumulative_rewards);
            })
            .catch(err => {
                setError('Failed to fetch rewards. Please try again later.');
                console.error(err);
            });
    }, []);

    // Prepare data for the chart
    const data = {
        labels: cumulativeRewards ? cumulativeRewards.map(data => data.timestamp) : [],
        datasets: [
            {
                label: 'Cumulative Rewards',
                data: cumulativeRewards ? cumulativeRewards.map(data => parseFloat(data.cumulative_rewards)) : [],
                fill: false,
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgba(75, 192, 192, 0.2)',
            },
        ],
    };

    const options = {
        scales: {
            x: {
                type: 'time',
                adapters: {
                    date: {
                        locale: enUS
                    }
                },
                time: {
                    tooltipFormat: 'MMMM dd, yyyy HH:mm',
                    unit: 'minute'
                },
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        }
    };

    return (
        <div className="rewards-page">
            <h1>Rewards Page</h1>
            {error && <p className="error">{error}</p>}
            <h2>Rewards Per Hardware</h2>
            {rewards ? (
                <ul>
                    {rewards.map(reward => (
                        <li key={reward.hardware_id}>
                            Hardware ID: {reward.hardware_id}, Total Rewards: {reward.total_rewards}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Loading rewards per hardware...</p>
            )}
            <h2>Cumulative Rewards</h2>
            {cumulativeRewards ? (
                <Line data={data} options={options} />
            ) : (
                <p>Loading cumulative rewards...</p>
            )}
        </div>
    );
}

export default RewardsPage;
