import React from 'react';
import './home.css';
import mainImage from './media/miningrevo2.png'; // Import the image

function HomePage() {
  return (
    <div className="home-page">
      <div className="home-container">
        <img src={mainImage} alt="Main" className="image-bg" />
        <div className="content">
          <h1>Welcome to our cryptocurrency mining platform!</h1>
          <p>Welcome to our cutting-edge cryptocurrency mining platform, designed to make mining accessible and rewarding for everyone. Contribute your computing power, join mining pools, and increase your chances of earning rewards. Our platform is user-friendly, secure, and scalable, offering real-time updates and educational resources to enhance your mining experience. Whether you're a beginner or a seasoned miner, we equip you with the tools you need to succeed in cryptocurrency mining.</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;

