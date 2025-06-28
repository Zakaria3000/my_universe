from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import secrets
from app.models import PremiumUser
from app.exts import db

premium_bp = Blueprint('premium', __name__)

@premium_bp.route('/subscribe', methods=['POST'])
def subscribe_premium():
    """Souscrire à un abonnement premium"""
    try:
        data = request.get_json()

        if not data or not data.get('email') or not data.get('plan'):
            return jsonify({
                'success': False,
                'message': 'Email et plan requis'
            }), 400

        email = data['email']
        plan = data['plan']

        # Vérifier si l'utilisateur existe déjà
        existing_user = PremiumUser.query.filter_by(email=email).first()
        if existing_user and existing_user.actif:
            return jsonify({
                'success': False,
                'message': 'Un abonnement actif existe déjà pour cet email'
            }), 400

        # Générer un token unique
        token = secrets.token_urlsafe(32)

        # Calculer la date d'expiration (30 jours)
        date_expiration = datetime.utcnow() + timedelta(days=30)

        # Créer ou mettre à jour l'utilisateur premium
        if existing_user:
            existing_user.plan = plan
            existing_user.token = token
            existing_user.date_souscription = datetime.utcnow()
            existing_user.date_expiration = date_expiration
            existing_user.actif = True
            premium_user = existing_user
        else:
            premium_user = PremiumUser(
                email=email,
                plan=plan,
                token=token,
                date_expiration=date_expiration
            )
            db.session.add(premium_user)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Abonnement premium activé avec succès!',
            'token': token,
            'plan': plan,
            'expires': date_expiration.isoformat()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@premium_bp.route('/verify', methods=['POST'])
def verify_premium():
    """Vérifier le statut premium d'un utilisateur"""
    try:
        data = request.get_json()
        token = data.get('token') if data else None

        if not token:
            return jsonify({
                'success': True,
                'is_premium': False,
                'message': 'Token manquant'
            })

        premium_user = PremiumUser.query.filter_by(token=token, actif=True).first()

        if not premium_user:
            return jsonify({
                'success': True,
                'is_premium': False,
                'message': 'Token invalide'
            })

        # Vérifier si l'abonnement n'a pas expiré
        if premium_user.date_expiration < datetime.utcnow():
            premium_user.actif = False
            db.session.commit()
            return jsonify({
                'success': True,
                'is_premium': False,
                'message': 'Abonnement expiré'
            })

        return jsonify({
            'success': True,
            'is_premium': True,
            'user': premium_user.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@premium_bp.route('/analytics', methods=['POST'])
def get_premium_analytics():
    """Obtenir les analyses premium"""
    try:
        data = request.get_json()
        token = data.get('token') if data else None

        if not token:
            return jsonify({
                'success': False,
                'message': 'Token requis'
            }), 401

        premium_user = PremiumUser.query.filter_by(token=token, actif=True).first()

        if not premium_user or premium_user.date_expiration < datetime.utcnow():
            return jsonify({
                'success': False,
                'message': 'Accès premium requis'
            }), 403

        # Données d'analyse simulées mais réalistes
        analytics_data = {
            'market_trends': {
                'evolution_prix': [
                    {'mois': 'Jan 2024', 'prix_moyen': 5200},
                    {'mois': 'Fév 2024', 'prix_moyen': 5350},
                    {'mois': 'Mar 2024', 'prix_moyen': 5480},
                    {'mois': 'Avr 2024', 'prix_moyen': 5620},
                    {'mois': 'Mai 2024', 'prix_moyen': 5780},
                    {'mois': 'Juin 2024', 'prix_moyen': 5950}
                ],
                'croissance_annuelle': '+14.4%',
                'prediction_6_mois': 6400
            },
            'analyse_regionale': [
                {'region': 'Casablanca-Settat', 'prix_moyen': 8500, 'croissance': '+15.2%', 'volume': 156},
                {'region': 'Rabat-Salé-Kénitra', 'prix_moyen': 7200, 'croissance': '+8.7%', 'volume': 89},
                {'region': 'Marrakech-Safi', 'prix_moyen': 6800, 'croissance': '+10.3%', 'volume': 67},
                {'region': 'Tanger-Tétouan-Al Hoceima', 'prix_moyen': 5500, 'croissance': '+12.1%', 'volume': 45},
                {'region': 'Fès-Meknès', 'prix_moyen': 4800, 'croissance': '+6.8%', 'volume': 34}
            ],
            'opportunites_investissement': [
                {
                    'zone': 'Nouvelle ville de Tamesna',
                    'potentiel_roi': '28%',
                    'niveau_risque': 'Modéré',
                    'recommandation': 'Fortement recommandé',
                    'prix_actuel': 4200,
                    'prix_projete': 5400
                },
                {
                    'zone': 'Extension urbaine de Fès',
                    'potentiel_roi': '22%',
                    'niveau_risque': 'Faible',
                    'recommandation': 'Recommandé',
                    'prix_actuel': 3800,
                    'prix_projete': 4600
                },
                {
                    'zone': 'Zone industrielle Kenitra',
                    'potentiel_roi': '35%',
                    'niveau_risque': 'Élevé',
                    'recommandation': 'Pour investisseurs expérimentés',
                    'prix_actuel': 2900,
                    'prix_projete': 3900
                }
            ],
            'statistiques_detaillees': {
                'total_transactions': 1247,
                'volume_total': '2.8 milliards MAD',
                'superficie_moyenne': 850,
                'temps_vente_moyen': '45 jours',
                'taux_appreciation': '+12.8%'
            }
        }

        return jsonify({
            'success': True,
            'data': analytics_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500