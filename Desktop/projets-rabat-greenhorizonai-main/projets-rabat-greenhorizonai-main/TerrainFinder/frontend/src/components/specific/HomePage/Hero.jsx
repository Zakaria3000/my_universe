import React from 'react';
import { Search, Play, MapPin, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content animate-fade-in-left">
          <h1>Trouvez le <span className="highlight">terrain parfait</span> au Maroc</h1>
          <p>
            Plateforme intelligente de recherche de terrains avec cartographie interactive, 
            filtres avancés et données en temps réel pour investisseurs et constructeurs.
          </p>
          <div className="hero-buttons">
            <Link to="/app" className="btn btn-primary">
              <Search className="icon" /> Commencer la recherche
            </Link>
            <Link to="#features" className="btn btn-secondary">
              <Play className="icon" /> Voir la démo
            </Link>
          </div>
        </div>
        
        <div className="hero-visual animate-fade-in-right">
          <div className="hero-card">
            <div className="hero-card-header">
              <div className="hero-card-icon">
                <MapPin className="icon icon-lg" style={{ color: 'white' }} />
              </div>
              <div className="hero-card-info">
                <h3>Casablanca</h3>
                <p>Prix en hausse +12%</p>
              </div>
            </div>
            <div className="hero-card-stats">
              <div className="stat">
                <span className="stat-number">8,000</span>
                <span className="stat-label">MAD/m²</span>
              </div>
              <div className="stat">
                <CheckCircle className="icon" style={{ color: 'var(--success-color)' }} />
                <span className="stat-label">Terrain titré</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;