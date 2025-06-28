from flask import Blueprint, jsonify, request
from app.models import Terrain
from datetime import datetime

terrain_bp = Blueprint('terrain', __name__)

@terrain_bp.route('/terrains', methods=['GET'])
def get_terrains():
    """Récupérer tous les terrains avec filtrage"""
    try:
        # Paramètres de filtrage
        superficie_min = request.args.get('superficie_min', type=int)
        superficie_max = request.args.get('superficie_max', type=int)
        prix_m2_min = request.args.get('prix_m2_min', type=int)
        prix_m2_max = request.args.get('prix_m2_max', type=int)
        type_terrain = request.args.get('type')
        ville = request.args.get('ville')
        region = request.args.get('region')
        statut_foncier = request.args.get('statut_foncier')
        sort_by = request.args.get('sort_by', 'id')
        sort_order = request.args.get('sort_order', 'asc')

        # Construction de la requête
        query = Terrain.query

        if superficie_min:
            query = query.filter(Terrain.superficie_m2 >= superficie_min)
        if superficie_max:
            query = query.filter(Terrain.superficie_m2 <= superficie_max)
        if prix_m2_min:
            query = query.filter(Terrain.prix_m2 >= prix_m2_min)
        if prix_m2_max:
            query = query.filter(Terrain.prix_m2 <= prix_m2_max)
        if type_terrain and type_terrain != 'tous':
            query = query.filter(Terrain.type.ilike(f'%{type_terrain}%'))
        if ville:
            query = query.filter(Terrain.ville.ilike(f'%{ville}%'))
        if region and region != 'toutes':
            query = query.filter(Terrain.region.ilike(f'%{region}%'))
        if statut_foncier and statut_foncier != 'tous':
            query = query.filter(Terrain.statut_foncier.ilike(f'%{statut_foncier}%'))

        # Tri des résultats
        if hasattr(Terrain, sort_by):
            if sort_order == 'desc':
                query = query.order_by(getattr(Terrain, sort_by).desc())
            else:
                query = query.order_by(getattr(Terrain, sort_by))

        terrains = query.all()

        # Calcul du prix moyen
        prix_moyen = sum(t.prix_m2 for t in terrains) / len(terrains) if terrains else 0

        return jsonify({
            'success': True,
            'data': [terrain.to_dict() for terrain in terrains],
            'count': len(terrains),
            'prix_moyen': round(prix_moyen, 2)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@terrain_bp.route('/terrains/<int:terrain_id>', methods=['GET'])
def get_terrain(terrain_id):
    """Récupérer un terrain spécifique"""
    try:
        terrain = Terrain.query.get_or_404(terrain_id)
        return jsonify({
            'success': True,
            'data': terrain.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500