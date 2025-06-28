import React, { useEffect, useState } from 'react';
import '../../../styles/stats.css';

const Stats = () => {
  const [terrainsCount, setTerrainsCount] = useState(0);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setTerrainsCount(500);
    }, 1000);
  }, []);

  return (
    <section className="stats-section">
      <div className="stats-container">
        <div className="stats-item animate-fade-in-up stats-item-1">
          <span className="stats-number">{terrainsCount}</span>
          <span className="stats-label">Terrains disponibles</span>
        </div>
        <div className="stats-item animate-fade-in-up stats-item-2">
          <span className="stats-number">8</span>
          <span className="stats-label">Régions couvertes</span>
        </div>
        <div className="stats-item animate-fade-in-up stats-item-3">
          <span className="stats-number">24</span>
          <span className="stats-label">Mise à jour</span>
        </div>
        <div className="stats-item animate-fade-in-up stats-item-4">
          <span className="stats-number">95%</span>
          <span className="stats-label">Satisfaction client</span>
        </div>
      </div>
    </section>
  );
};

export default Stats;