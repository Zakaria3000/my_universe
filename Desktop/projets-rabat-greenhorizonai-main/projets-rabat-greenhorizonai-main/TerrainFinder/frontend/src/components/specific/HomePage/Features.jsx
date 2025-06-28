import React from 'react';
import { 
  Search, Map, BarChart3, Smartphone, Bell, ShieldCheck 
} from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: <Search className="icon icon-xl" style={{ color: 'white' }} />,
      title: "Recherche intelligente",
      description: "Filtres avancés par superficie, prix, région, statut foncier et proximité des infrastructures."
    },
    {
      icon: <Map className="icon icon-xl" style={{ color: 'white' }} />,
      title: "Cartographie interactive",
      description: "Visualisez tous les terrains sur une carte interactive avec détails et photos."
    },
    {
      icon: <BarChart3 className="icon icon-xl" style={{ color: 'white' }} />,
      title: "Analyses de marché",
      description: "Statistiques en temps réel, tendances des prix et projections d'investissement."
    },
    {
      icon: <Smartphone className="icon icon-xl" style={{ color: 'white' }} />,
      title: "Application mobile",
      description: "Interface responsive optimisée pour tous les appareils et navigation tactile."
    },
    {
      icon: <Bell className="icon icon-xl" style={{ color: 'white' }} />,
      title: "Alertes personnalisées",
      description: "Recevez des notifications pour les nouveaux terrains correspondant à vos critères."
    },
    {
      icon: <ShieldCheck className="icon icon-xl" style={{ color: 'white' }} />,
      title: "Données vérifiées",
      description: "Informations juridiques et techniques vérifiées par nos experts immobiliers."
    }
  ];

  return (
    <section className="features-section" id="features">
      <div className="features-container">
        <div className="section-header">
          <h2>Fonctionnalités avancées</h2>
          <p>Tous les outils dont vous avez besoin pour trouver et analyser les terrains</p>
        </div>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card animate-fade-in-up">
              <div className="feature-icon">
                {feature.icon}
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;