import React, { useState, useEffect, useRef } from 'react';
import { ArrowUp, ArrowDown, ArrowLeft, ArrowRight, Brain, Code, Server, Award, Book, Briefcase, BadgeCheck, ChevronDown, ChevronUp, Zap, Terminal, Globe } from 'lucide-react';

const ZakariaJourney = () => {
  const [activeNode, setActiveNode] = useState(null);
  const [expandedSections, setExpandedSections] = useState({
    skills: true,
    projects: false,
    education: false,
    experience: false
  });
  const [animationProgress, setAnimationProgress] = useState(0);
  const [skillPoints, setSkillPoints] = useState({
    programming: 0,
    ai: 0,
    web: 0,
    soft: 0
  });
  const [achievements, setAchievements] = useState([]);
  const galaxyRef = useRef(null);

  const nodes = [
    { id: 'bac', name: 'BAC Sciences Math B', year: '2020', type: 'education', position: { x: 25, y: 80 }, color: '#4DA6FF' },
    { id: 'cpge', name: 'Classes Préparatoires', year: '2020-2022', type: 'education', position: { x: 35, y: 40 }, color: '#4DA6FF' },
    { id: 'emsi', name: 'EMSI - Génie Informatique', year: '2022-2025', type: 'education', position: { x: 55, y: 25 }, color: '#4DA6FF' },
    { id: 'uca', name: 'Master IA - Université Côte d\'Azur', year: '2024-2025', type: 'education', position: { x: 75, y: 40 }, color: '#4DA6FF' },
    { id: 'lear', name: 'Stage - Lear Corporation', year: '2023', type: 'experience', position: { x: 45, y: 60 }, color: '#FF7C4D' },
    { id: 'intelcom', name: 'Stage - Intelcom', year: '2024', type: 'experience', position: { x: 65, y: 60 }, color: '#FF7C4D' },
    { id: 'sonic', name: 'Jeu Pygame - Sonic', year: '2023', type: 'project', position: { x: 40, y: 75 }, color: '#4DFF88' },
    { id: 'fakenews', name: 'Détection Fake News', year: '2024', type: 'project', position: { x: 60, y: 80 }, color: '#4DFF88' },
    { id: 'hrm', name: 'Gestion RH Java', year: '2023', type: 'project', position: { x: 50, y: 85 }, color: '#4DFF88' },
    { id: 'music', name: 'App Musicale Flutter', year: '2024', type: 'project', position: { x: 70, y: 70 }, color: '#4DFF88' },
    { id: 'chatbot', name: 'Chatbot DevOps', year: '2024', type: 'project', position: { x: 80, y: 60 }, color: '#4DFF88' }
  ];

  const nodeDetails = {
    bac: {
      description: "Obtention du Baccalauréat Sciences Math B à l'École Bennis & Terrab à Kenitra avec mention.",
      skills: { programming: 5, ai: 0, web: 5, soft: 10 },
      achievements: ["Premier pas vers l'ingénierie informatique"]
    },
    cpge: {
      description: "Études intensives en mathématiques et physique aux Classes Préparatoires Ibn Ghazi à Rabat.",
      skills: { programming: 15, ai: 5, web: 10, soft: 30 },
      achievements: ["Développement de rigueur analytique", "Fondations mathématiques solides"]
    },
    emsi: {
      description: "Formation en génie informatique avec spécialisation en réseaux et intelligence artificielle.",
      skills: { programming: 60, ai: 40, web: 55, soft: 60 },
      achievements: ["Maîtrise des langages de programmation", "Conception de systèmes d'information"]
    },
    uca: {
      description: "Master spécialisé en Intelligence Artificielle à l'Université Côte d'Azur.",
      skills: { programming: 80, ai: 90, web: 70, soft: 85 },
      achievements: ["Spécialisation en Deep Learning", "Expertise en NLP"]
    },
    lear: {
      description: "Développement d'une application pour vérifier la conformité des combinaisons de câbles électriques.",
      skills: { programming: 65, ai: 40, web: 60, soft: 70 },
      achievements: ["Application industrielle", "Expérience en environnement professionnel"]
    },
    intelcom: {
      description: "Conception d'un chatbot spécialisé dans les technologies Cloud, DevOps et DevSecOps.",
      skills: { programming: 75, ai: 80, web: 70, soft: 80 },
      achievements: ["Implémentation NLP", "Solutions Cloud"]
    },
    sonic: {
      description: "Développement d'un jeu inspiré de Sonic utilisant Pygame, avec animations fluides et expérience utilisateur immersive.",
      skills: { programming: 70, ai: 30, web: 20, soft: 60 },
      achievements: ["Game Development", "Interface interactive"]
    },
    fakenews: {
      description: "Solution automatisée de fact-checking exploitant NewsAPI, FuzzyWuzzy et NLTK pour analyser la crédibilité des actualités.",
      skills: { programming: 75, ai: 85, web: 50, soft: 70 },
      achievements: ["NLP avancé", "Analyse sémantique"]
    },
    hrm: {
      description: "Plateforme de gestion des employés, congés et recrutements avec Spring MVC et JPA.",
      skills: { programming: 75, ai: 30, web: 80, soft: 65 },
      achievements: ["Architecture MVC", "Gestion de données complexes"]
    },
    music: {
      description: "Application musicale développée avec Flutter et Firebase, intégrant streaming en temps réel et authentification.",
      skills: { programming: 70, ai: 20, web: 85, soft: 75 },
      achievements: ["Développement mobile", "Intégration API"]
    },
    chatbot: {
      description: "Chatbot intelligent spécialisé pour les professionnels DevOps, offrant support et conseils techniques.",
      skills: { programming: 80, ai: 85, web: 60, soft: 80 },
      achievements: ["IA conversationnelle", "Knowledge Base technique"]
    }
  };

  const certifications = [
    { name: "Java SE 17 Developer", issuer: "Oracle University", year: "2023" },
    { name: "Oracle Database Administration I", issuer: "Oracle University", year: "2023" },
    { name: "Software Engineering: UML", issuer: "Hong Kong University of Science and Technology", year: "2022" },
    { name: "Python", issuer: "University of Michigan", year: "2022" },
    { name: "Leadership", issuer: "HEC Paris", year: "2023" },
    { name: "Unix System", issuer: "Codio", year: "2022" },
    { name: "Java and OOP", issuer: "University of Pennsylvania", year: "2023" },
    { name: "React", issuer: "Meta", year: "2024" }
  ];

  const skills = {
    programming: {
      title: "Programmation",
      items: ["Python", "Java", "C++", "Spring Boot", "Spring MVC", "Flutter"]
    },
    web: {
      title: "Développement Web",
      items: ["HTML/CSS", "JavaScript", "React", "Angular", "Thymeleaf"]
    },
    ai: {
      title: "Intelligence Artificielle",
      items: ["Machine Learning", "Deep Learning", "NLP", "Traitement de données", "Analyse prédictive"]
    },
    databases: {
      title: "Bases de données",
      items: ["Oracle", "SQL Server", "Firebase", "JPA/Hibernate"]
    },
    soft: {
      title: "Soft Skills",
      items: ["Travail d'équipe", "Résolution de problèmes", "Gestion de projet", "Communication", "Autonomie"]
    }
  };

  useEffect(() => {
    // Animation d'entrée
    const timer = setInterval(() => {
      setAnimationProgress(prev => {
        if (prev >= 100) {
          clearInterval(timer);
          return 100;
        }
        return prev + 1;
      });
    }, 30);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (activeNode) {
      const details = nodeDetails[activeNode];
      setSkillPoints(details.skills);
      setAchievements(details.achievements);
    } else {
      setSkillPoints({
        programming: 0,
        ai: 0,
        web: 0,
        soft: 0
      });
      setAchievements([]);
    }
  }, [activeNode]);

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleNodeClick = (nodeId) => {
    setActiveNode(nodeId === activeNode ? null : nodeId);
  };

  const moveGalaxy = (direction) => {
    if (!galaxyRef.current) return;

    const currentLeft = parseInt(galaxyRef.current.style.left || '0', 10);
    const currentTop = parseInt(galaxyRef.current.style.top || '0', 10);

    switch(direction) {
      case 'up':
        galaxyRef.current.style.top = `${currentTop + 50}px`;
        break;
      case 'down':
        galaxyRef.current.style.top = `${currentTop - 50}px`;
        break;
      case 'left':
        galaxyRef.current.style.left = `${currentLeft + 50}px`;
        break;
      case 'right':
        galaxyRef.current.style.left = `${currentLeft - 50}px`;
        break;
      default:
        break;
    }
  };

  return (
    <div className="relative w-full h-screen bg-gray-900 overflow-hidden text-white font-sans">
      {/* Galaxy navigation */}
      <div className="absolute bottom-6 right-6 flex flex-col items-center gap-2 z-30">
        <div className="grid grid-cols-3 gap-1">
          <div></div>
          <button
            className="w-10 h-10 bg-indigo-800 rounded-full flex items-center justify-center hover:bg-indigo-700"
            onClick={() => moveGalaxy('up')}
          >
            <ArrowUp size={20} />
          </button>
          <div></div>
          <button
            className="w-10 h-10 bg-indigo-800 rounded-full flex items-center justify-center hover:bg-indigo-700"
            onClick={() => moveGalaxy('left')}
          >
            <ArrowLeft size={20} />
          </button>
          <div className="w-10 h-10 bg-indigo-900 rounded-full flex items-center justify-center">
            <Zap size={20} className="text-yellow-400" />
          </div>
          <button
            className="w-10 h-10 bg-indigo-800 rounded-full flex items-center justify-center hover:bg-indigo-700"
            onClick={() => moveGalaxy('right')}
          >
            <ArrowRight size={20} />
          </button>
          <div></div>
          <button
            className="w-10 h-10 bg-indigo-800 rounded-full flex items-center justify-center hover:bg-indigo-700"
            onClick={() => moveGalaxy('down')}
          >
            <ArrowDown size={20} />
          </button>
          <div></div>
        </div>
        <div className="text-xs text-indigo-300 mt-1">Explorer la galaxie</div>
      </div>

      {/* Header */}
      <div className="absolute top-0 left-0 w-full bg-gradient-to-b from-indigo-900 to-transparent p-4 z-20">
        <h1 className="text-2xl font-bold text-center text-indigo-300 tracking-wider">
          L'UNIVERS DE ZAKARIA AKKAOUI
        </h1>
        <div className="text-center text-indigo-400 text-sm mt-1">
          Ingénieur en Génie Informatique · Spécialiste en IA · Développeur Full-Stack
        </div>
      </div>

      {/* Galaxy with nodes */}
      <div
        ref={galaxyRef}
        className="absolute inset-0 transition-all duration-500 ease-out"
        style={{ left: '0px', top: '0px' }}
      >
        {/* Star background */}
        {Array.from({ length: 100 }).map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-white"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              width: `${Math.random() * 3}px`,
              height: `${Math.random() * 3}px`,
              opacity: Math.random() * 0.8 + 0.2,
              animation: `twinkle ${Math.random() * 5 + 2}s ease-in-out infinite`
            }}
          ></div>
        ))}

        {/* Nodes */}
        {animationProgress === 100 && nodes.map((node, index) => (
          <div
            key={node.id}
            className="absolute cursor-pointer transition-all duration-500 ease-out"
            style={{
              left: `${node.position.x}%`,
              top: `${node.position.y}%`,
              transform: `scale(${activeNode === node.id ? 1.2 : 1})`,
              zIndex: activeNode === node.id ? 10 : 5,
              opacity: activeNode && activeNode !== node.id ? 0.4 : 1
            }}
            onClick={() => handleNodeClick(node.id)}
          >
            <div
              className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 ease-out ${activeNode === node.id ? 'animate-pulse' : ''}`}
              style={{
                backgroundColor: node.color,
                boxShadow: `0 0 15px ${node.color}`,
              }}
            >
              {node.type === 'education' && <Book size={24} />}
              {node.type === 'experience' && <Briefcase size={24} />}
              {node.type === 'project' && <Code size={24} />}
            </div>
            <div className="absolute w-40 text-center -left-14 mt-2 text-xs font-medium">
              {node.name}
              <div className="text-gray-400 text-xs mt-1">{node.year}</div>
            </div>

            {/* Connection lines */}
            {index > 0 && (
              <svg
                className="absolute"
                width="200"
                height="200"
                style={{
                  left: '-100px',
                  top: '-100px',
                  zIndex: -1,
                  opacity: activeNode && (activeNode !== node.id && activeNode !== nodes[index-1].id) ? 0.2 : 0.5
                }}
              >
                <line
                  x1="100"
                  y1="100"
                  x2={100 + (nodes[index-1].position.x - node.position.x) * 5}
                  y2={100 + (nodes[index-1].position.y - node.position.y) * 5}
                  stroke={`url(#gradient-${node.id})`}
                  strokeWidth="2"
                  strokeDasharray="5,5"
                />
                <defs>
                  <linearGradient id={`gradient-${node.id}`} x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor={node.color} />
                    <stop offset="100%" stopColor={nodes[index-1].color} />
                  </linearGradient>
                </defs>
              </svg>
            )}
          </div>
        ))}
      </div>

      {/* Detail panel */}
      <div
        className="fixed right-0 top-0 bottom-0 bg-gray-900 border-l border-indigo-900 p-4 overflow-y-auto transition-all duration-500 ease-out"
        style={{
          width: '350px',
          transform: `translateX(${activeNode ? '0' : '100%'})`,
          boxShadow: '-10px 0 30px rgba(76, 29, 149, 0.3)'
        }}
      >
        {activeNode && (
          <>
            <div className="flex items-center mb-4">
              <div
                className="w-8 h-8 rounded-full mr-3 flex items-center justify-center"
                style={{
                  backgroundColor: nodes.find(n => n.id === activeNode)?.color,
                  boxShadow: `0 0 10px ${nodes.find(n => n.id === activeNode)?.color}`
                }}
              >
                {nodes.find(n => n.id === activeNode)?.type === 'education' && <Book size={16} />}
                {nodes.find(n => n.id === activeNode)?.type === 'experience' && <Briefcase size={16} />}
                {nodes.find(n => n.id === activeNode)?.type === 'project' && <Code size={16} />}
              </div>
              <div>
                <h2 className="text-lg font-bold">{nodes.find(n => n.id === activeNode)?.name}</h2>
                <div className="text-indigo-400 text-sm">{nodes.find(n => n.id === activeNode)?.year}</div>
              </div>
            </div>

            <p className="text-gray-300 mb-6">{nodeDetails[activeNode].description}</p>

            {/* Skill points */}
            <div className="mb-6">
              <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-400 mb-2">Compétences développées</h3>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="flex items-center"><Terminal size={14} className="mr-1" /> Programmation</span>
                    <span>{skillPoints.programming}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500 rounded-full"
                      style={{ width: `${skillPoints.programming}%` }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="flex items-center"><Brain size={14} className="mr-1" /> Intelligence Artificielle</span>
                    <span>{skillPoints.ai}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-purple-500 rounded-full"
                      style={{ width: `${skillPoints.ai}%` }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="flex items-center"><Globe size={14} className="mr-1" /> Développement Web</span>
                    <span>{skillPoints.web}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500 rounded-full"
                      style={{ width: `${skillPoints.web}%` }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="flex items-center"><Server size={14} className="mr-1" /> Soft Skills</span>
                    <span>{skillPoints.soft}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-yellow-500 rounded-full"
                      style={{ width: `${skillPoints.soft}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Achievements */}
            <div className="mb-6">
              <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-400 mb-2">Réalisations</h3>
              <ul className="space-y-2">
                {achievements.map((achievement, index) => (
                  <li key={index} className="flex items-start">
                    <BadgeCheck size={18} className="text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-300 text-sm">{achievement}</span>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </div>

      {/* Skills & Info Panel */}
      <div className="fixed left-0 bottom-0 top-16 w-64 bg-gray-900 border-r border-indigo-900 overflow-y-auto z-10 transition-opacity duration-500" style={{ opacity: activeNode ? 0.7 : 1 }}>
        <div className="p-4 space-y-4">
          {/* Profile Summary */}
          <div className="text-center mb-6">
            <div className="w-20 h-20 rounded-full bg-indigo-800 flex items-center justify-center mx-auto mb-3">
              <span className="text-2xl font-bold">ZA</span>
            </div>
            <h2 className="text-lg font-bold">Zakaria Akkaoui</h2>
            <p className="text-indigo-400 text-sm">Élève Ingénieur en Génie Informatique</p>
            <div className="flex justify-center gap-3 mt-2 text-indigo-300">
              <Terminal size={18} />
              <Brain size={18} />
              <Server size={18} />
              <Globe size={18} />
            </div>
          </div>

          {/* Skills Section */}
          <div className="border-t border-indigo-900 pt-4">
            <div
              className="flex justify-between items-center cursor-pointer"
              onClick={() => toggleSection('skills')}
            >
              <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-400">Compétences</h3>
              {expandedSections.skills ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>
            {expandedSections.skills && (
              <div className="mt-3 space-y-4">
                {Object.entries(skills).map(([key, skill]) => (
                  <div key={key}>
                    <h4 className="text-sm font-semibold text-indigo-300 mb-2">{skill.title}</h4>
                    <div className="flex flex-wrap gap-2">
                      {skill.items.map((item, i) => (
                        <span key={i} className="text-xs bg-indigo-900 text-indigo-300 px-2 py-1 rounded">
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Certifications Section */}
          <div className="border-t border-indigo-900 pt-4">
            <div
              className="flex justify-between items-center cursor-pointer"
              onClick={() => toggleSection('education')}
            >
              <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-400">Certifications</h3>
              {expandedSections.education ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>
            {expandedSections.education && (
              <div className="mt-3 space-y-3">
                {certifications.map((cert, i) => (
                  <div key={i} className="flex items-start">
                    <Award size={16} className="text-yellow-500 mr-2 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="text-sm font-medium">{cert.name}</div>
                      <div className="text-xs text-gray-400">{cert.issuer} • {cert.year}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Contact Section */}
          <div className="border-t border-indigo-900 pt-4 text-sm">
            <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-400 mb-3">Contact</h3>
            <div className="space-y-2 text-gray-300">
              <div>zakariakkaoui@gmail.com</div>
              <div>+212 771648181</div>
              <div>3ème Base Aérienne Force Royale Air, KENITRA</div>
            </div>
          </div>
        </div>
      </div>

      {/* Hint */}
      <div className="fixed left-1/2 transform -translate-x-1/2 bottom-6 bg-indigo-900 bg-opacity-60 px-4 py-2 rounded-full text-sm z-20">
        Cliquez sur les planètes pour explorer mon univers professionnel
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes twinkle {
          0%, 100% { opacity: 0.2; }
          50% { opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default ZakariaJourney;