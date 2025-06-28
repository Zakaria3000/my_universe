import React from 'react';

const CTA = () => {
  return (
    <section className="cta-section" id="contact">
      <div className="cta-container">
        <h2>Prêt à trouver votre terrain idéal ?</h2>
        <p>Rejoignez des milliers d'investisseurs qui font confiance à TerrainFinder</p>
        <div className="cta-buttons">
          <a href="/app" className="btn btn-white">Commencer maintenant</a>
          <a href="/premium" className="btn btn-outline">Essayer Premium</a>
        </div>
      </div>
    </section>
  );
};

export default CTA;