import React, { useState, useEffect } from 'react';
import { Map, Layers, CreditCard, Mail, Rocket, Menu, X } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="nav-container">
        <Link to="/" className="logo">
          <Map className="icon icon-lg" />
          TerrainFinder
        </Link>
        
        <ul className={`nav-links ${mobileMenuOpen ? 'active' : ''}`}>
          <li>
            <Link to="#features">
              <Layers className="icon" />
              Fonctionnalités
            </Link>
          </li>
          <li>
            <Link to="#pricing">
              <CreditCard className="icon" />
              Tarifs
            </Link>
          </li>
          <li>
            <Link to="#contact">
              <Mail className="icon" />
              Contact
            </Link>
          </li>
          <li>
            <Link to="/app" className="cta-button">
              <Rocket className="icon" />
              Essayer Gratuitement
            </Link>
          </li>
        </ul>
        
        <button 
          className="mobile-menu-toggle" 
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X className="icon" /> : <Menu className="icon" />}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;