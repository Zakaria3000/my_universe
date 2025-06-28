import React from 'react';
import { Map } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-logo">
          <Map className="icon icon-lg" /> TerrainFinder
        </div>
        <p className="footer-text">
          La plateforme de référence pour la recherche de terrains au Maroc
        </p>
        <div className="footer-bottom">
          <p>&copy; 2025 TerrainFinder. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;