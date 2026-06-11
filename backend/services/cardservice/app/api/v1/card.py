from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from app.core.security import get_current_user
from app.db.database import SessionLocal
from app.schemas.card import CardCreate, CardResponse
from app.services.card_service import CardService

card_blueprint = Blueprint("cards", __name__, url_prefix="/api/v1/cards")


def _json_body():
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequest("Request body must be valid JSON")
    return data


def _validation_error_response(exc: ValidationError):
    return jsonify({"detail": exc.errors()}), 422


@card_blueprint.get("")
async def list_cards():
    user = get_current_user()

    async with SessionLocal() as session:
        service = CardService(session)
        cards = await service.list_cards(user.id)

    return jsonify({"cards": [CardResponse.model_validate(card).model_dump(mode="json") for card in cards]})


@card_blueprint.post("")
async def create_card():
    user = get_current_user()

    try:
        card_data = CardCreate.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        service = CardService(session)
        card = await service.create_card(user.id, **card_data.model_dump())

    return jsonify({"card": CardResponse.model_validate(card).model_dump(mode="json")}), 201


@card_blueprint.delete("/<card_id>")
async def delete_card(card_id: str):
    user = get_current_user()

    async with SessionLocal() as session:
        service = CardService(session)
        result = await service.delete_card(user.id, card_id)

    return jsonify(result)