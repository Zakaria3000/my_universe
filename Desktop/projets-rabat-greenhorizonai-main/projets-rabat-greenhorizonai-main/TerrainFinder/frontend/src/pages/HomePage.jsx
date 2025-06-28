import React from 'react';
import Navbar from '../components/specific/HomePage/Navbar';
import Hero from '../components/specific/HomePage/Hero';
import Stats from '../components/specific/HomePage/Stats';
import Features from '../components/specific/HomePage/Features';
import Pricing from '../components/specific/HomePage/Pricing';
import Footer from '../components/specific/HomePage/Footer';
import CTA from '../components/specific/HomePage/CTA';

const HomePage = () => {
  return (
    <div className="home-page">
      <Navbar />
      <Hero />
      <Stats />
      <Features />
      <Pricing />
      <CTA />
      <Footer />
    </div>
  );
};

export default HomePage;