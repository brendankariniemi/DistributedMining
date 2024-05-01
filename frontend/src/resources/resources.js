import React, { useState, useEffect } from 'react';
import ResourceService from "../services/resourceService";
import './resources.css';

function ResourcesPage() {
    const [cryptos, setCryptos] = useState([]);
    const [guides, setGuides] = useState([]);
    const [tutorials, setTutorials] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const cryptoResponse = await ResourceService.getCryptocurrencies();
                setCryptos(cryptoResponse.data);

                const guidesResponse = await ResourceService.getGuides();
                setGuides(guidesResponse.data);

                const tutorialsResponse = await ResourceService.getTutorial();
                setTutorials(tutorialsResponse.data);
            } catch (error) {
                console.error('Failed to fetch resources:', error);
            }
        }

        fetchData();
    }, []);

    return (


<div class="resources-container">
    <h1>Resources</h1>

    <div>
        <h2>Cryptocurrencies</h2>
        {cryptos.map(crypto => (
        <div key={crypto.id}>
            <h3>{crypto.name}</h3>
            <p>{crypto.details}</p>
            {crypto.link &&
                <a href={crypto.link} target="_blank" rel="noopener noreferrer">Learn More</a>}
        </div>
        ))}
    </div>

    <div>
        <h2>Guides</h2>
        {guides.map(guide => (
        <div key={guide.id}>
            <h3>{guide.title}</h3>
            <p>{guide.description}</p>
            {guide.link && <a href={guide.link} target="_blank" rel="noopener noreferrer">View Guide</a>}
        </div>
        ))}
    </div>

    <div>
        <h2>Tutorials</h2>
        {tutorials.map(tutorial => (
        <div key={tutorial.id}>
            <h3>{tutorial.title}</h3>
            <p>{tutorial.description}</p>
            {tutorial.link && <a href={tutorial.link} target="_blank" rel="noopener noreferrer">View Tutorial</a>}
        </div>
        ))}
    </div>
</div>

    );
}

export default ResourcesPage;