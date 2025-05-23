from flask import Blueprint, request, jsonify
from app.services.listing_service import ListingService

listing_bp = Blueprint("listings", __name__)


@listing_bp.route("/listings", methods=["POST"])
def create_listing():
    # capture the data from request
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Data as JSON not provided"
            }
        ), 400

    if "owner_id" not in data or not data.get("owner_id"):
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Required field 'owner_id' is missing"
            }
        ), 400

    if "title" not in data or not data.get("title"):
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Required field 'title' is missing"
            }
        ), 400

    if "price" not in data or not data.get("price"):
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Required field 'price' is missing"
            }
        ), 400

    listing = ListingService.create_listing(
        owner_id=data.get("owner_id"),
        title=data.get("title"),
        price=data.get("price"),
        data=data
    )

    if listing:
        return jsonify({
            "message": "Successfully created a new listing",
            "listing": listing.serialize()
        }), 201
    else:
        return jsonify({
            "message": "Something went wrond while creating the listing"
        }), 400


@listing_bp.route("/listings", methods=["GET"])
def get_all_listings():
    listings = ListingService.get_all_listings()
    if listings:
        return jsonify([l.serialize() for l in listings])
    else:
        return jsonify({
            "message": "Seems like there is an issue"
        }), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing_by_id(listing_id: int):
    listing = ListingService.get_listing_by_id(listing_id)
    if listing:
        return jsonify(listing.serialize())
    else:
        return jsonify({
            "message": "Listing not found"
        }), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id: int):
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Data as JSON not provided"
            }
        ), 400

    listing = ListingService.get_listing_by_id(listing_id)

    if not listing:
        return jsonify(
            {
                "error": "404 Not Found",
                "message": f"Listing with id: {listing_id} not found."
            }
        ), 404

    # update data
    for key, value in data.items():
        if hasattr(listing, key):
            setattr(listing, key, value)

    updated_listing = ListingService.update_listing(listing)

    if updated_listing:
        return jsonify({
            "message": "Listing successfully updated.",
            "listing": updated_listing.serialize()
        })
    else:
        return jsonify({"error": "Something went wrong"})


@listing_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id: int):
    listing = ListingService.get_listing_by_id(listing_id)

    if not listing:
        return jsonify(
            {
                "error": "404 Not Found",
                "message": f"Listing with id: {listing_id} not found."
            }
        ), 404

    deleted = ListingService.delete_listing(listing)

    if deleted:
        return jsonify({
            "message": "Listing successfully deleted."
        })
    else:
        return jsonify({"error": "Something went wrong"})
