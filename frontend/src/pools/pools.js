import React, { useEffect, useState, useMemo } from 'react';
import PoolService from '../services/poolService';
import { Line } from 'react-chartjs-2';
import PoolPopUp from "./pool-popup";
import './pools.css';

function PoolsPage() {
    const [pools, setPools] = useState([]);
    const [prices, setPrices] = useState({});
    const [loading, setLoading] = useState(true);
    const [errors, setErrors] = useState({});
    const [activeModal, setActiveModal] = useState(null);

    useEffect(() => {
        setLoading(true);
        PoolService.getPools()
            .then(response => {
                setPools(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Failed to fetch pools', error);
                setErrors(prev => ({ ...prev, load: 'Failed to load pools' }));
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        pools.forEach(pool => {
            PoolService.getPricingData(pool.cryptocurrency.name)
                .then(pricingData => {
                    setPrices(prevPrices => ({
                        ...prevPrices,
                        [pool.cryptocurrency.name]: pricingData
                    }));
                })
                .catch(error => {
                    console.error('Failed to fetch pricing data for ' + pool.cryptocurrency.name, error);
                    setErrors(prev => ({ ...prev, [pool.cryptocurrency.name]: 'Failed to load pricing data' }));
                });
        });
    }, [pools]);

    const chartData = useMemo(() => {
        return Object.keys(prices).reduce((acc, key) => {
            acc[key] = {
                labels: prices[key].map(item => new Date(item[0]).toLocaleDateString()),
                datasets: [{
                    label: 'Price Over Last 30 Days',
                    data: prices[key].map(item => item[1]),
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false,
                    tension: 0.1
                }]
            };
            return acc;
        }, {});
    }, [prices]);

    const toggleModal = (poolId) => {
        setActiveModal(activeModal === poolId ? null : poolId);
    };

    if (loading) return <p>Loading...</p>;
    if (errors.load) return <p>Error: {errors.load}</p>;

    return (
        <div>
            <h1>Pools Page</h1>
            <div className="pool-list">
                {pools.map(pool => (
                    <div key={pool.pool_id} className="pool">
                        <h2>{pool.cryptocurrency.name}</h2>
                        <p>Created: {new Date(pool.creation_timestamp).toLocaleDateString()}</p>
                        <p>Total Earnings: {pool.total_earnings}</p>
                        <p>Client Count: {pool.hardware_count}</p>
                        <div className="chart-container">
                            {chartData[pool.cryptocurrency.name] && (
                                <Line data={chartData[pool.cryptocurrency.name]}/>
                            )}
                        </div>
                        <div className="pool-join-button">
                            <button onClick={() => toggleModal(pool.pool_id)}>
                                Join this Pool!
                            </button>
                        </div>
                        {activeModal === pool.pool_id && (
                            <PoolPopUp toggle={() => toggleModal(pool.pool_id)} pool_id={pool.pool_id} />
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default PoolsPage;

