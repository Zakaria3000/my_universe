import React from 'react';
import { Check, X } from 'lucide-react';

const Pricing = () => {
  const plans = [
    {
      name: "Gratuit",
      price: "0",
      period: "/mois",
      featured: false,
      features: [
        { text: "10 recherches par jour", included: true },
        { text: "Accès à la carte interactive", included: true },
        { text: "Filtres de base", included: true },
        { text: "Support communautaire", included: true },
        { text: "Analyses avancées", included: false },
        { text: "Alertes personnalisées", included: false }
      ],
      cta: {
        text: "Commencer gratuitement",
        link: "/app",
        variant: "secondary"
      }
    },
    {
      name: "Premium",
      price: "299",
      period: "/mois",
      featured: true,
      features: [
        { text: "Recherches illimitées", included: true },
        { text: "Tous les filtres avancés", included: true },
        { text: "Analyses de marché", included: true },
        { text: "Alertes personnalisées", included: true },
        { text: "Export des données", included: true },
        { text: "Support prioritaire", included: true }
      ],
      cta: {
        text: "Passer au Premium",
        link: "/premium",
        variant: "primary"
      }
    },
    {
      name: "Entreprise",
      price: "999",
      period: "/mois",
      featured: false,
      features: [
        { text: "Tout du plan Premium", included: true },
        { text: "API d'intégration", included: true },
        { text: "Rapports personnalisés", included: true },
        { text: "Comptes multiples", included: true },
        { text: "Formation dédiée", included: true },
        { text: "Support 24/7", included: true }
      ],
      cta: {
        text: "Nous contacter",
        link: "/premium?plan=enterprise",
        variant: "secondary"
      }
    }
  ];

  return (
    <section className="pricing-section" id="pricing">
      <div className="features-container">
        <div className="section-header2">
          <h2>Choisissez votre plan</h2>
          <p>Des solutions adaptées à tous les besoins, du particulier au professionnel</p>
        </div>
        <div className="pricing-grid">
          {plans.map((plan, index) => (
            <div 
              key={index} 
              className={`pricing-card ${plan.featured ? 'featured' : ''} animate-fade-in-up`}
            >
              <div className="pricing-header">
                <h3>{plan.name}</h3>
                <div className="pricing-price">
                  {plan.price}<span style={{ fontSize: "1rem" }}>MAD</span>
                </div>
                <div className="pricing-period">{plan.period}</div>
              </div>
              <ul className="pricing-features">
                {plan.features.map((feature, i) => (
                  <li key={i}>
                    {feature.included ? (
                      <Check className="icon" style={{ color: "var(--success-color)" }} />
                    ) : (
                      <X className="icon" style={{ color: "var(--text-muted)" }} />
                    )}
                    {feature.text}
                  </li>
                ))}
              </ul>
              <a 
                href={plan.cta.link} 
                className={`btn btn-${plan.cta.variant}`} 
                style={{ width: "100%" }}
              >
                {plan.cta.text}
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Pricing;